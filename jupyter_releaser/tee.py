"""tee like run implementation."""
# This file is a modified version of https://github.com/pycontribs/subprocess-tee/blob/daffcbbf49fc5a2c7f3eaf75551f08fac0b9b63d/src/subprocess_tee/__init__.py
#
# It is licensed under the following license:
#
# The MIT License
# Copyright (c) 2020 Sorin Sbarnea
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import asyncio
import atexit
import os
import platform
import subprocess
import sys
from asyncio import StreamReader
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

if TYPE_CHECKING:
    CompletedProcess = subprocess.CompletedProcess[Any]  # pylint: disable=E1136
else:
    CompletedProcess = subprocess.CompletedProcess

try:
    from shlex import join
except ImportError:
    from subprocess import list2cmdline as join  # type:ignore


STREAM_LIMIT = 2**23  # 8MB instead of default 64kb, override it if you need


async def _read_stream(stream: StreamReader, callback: Callable[..., Any]) -> None:
    while True:
        line = await stream.readline()
        if line:
            callback(line)
        else:
            break


async def _stream_subprocess(args: str, **kwargs: Any) -> CompletedProcess:
    platform_settings: Dict[str, Any] = {}
    if platform.system() == "Windows":
        platform_settings["env"] = os.environ

    # this part keeps behavior backwards compatible with subprocess.run
    tee = kwargs.get("tee", True)
    stdout = kwargs.get("stdout", sys.stdout)
    if stdout == subprocess.DEVNULL or not tee:
        stdout = open(os.devnull, "w")
    stderr = kwargs.get("stderr", sys.stderr)
    if stderr == subprocess.DEVNULL or not tee:
        stderr = open(os.devnull, "w")

    # We need to tell subprocess which shell to use when running shell-like
    # commands.
    # * SHELL is not always defined
    # * /bin/bash does not exit on alpine, /bin/sh seems bit more portable
    if "executable" not in kwargs and isinstance(args, str) and " " in args:
        platform_settings["executable"] = os.environ.get("SHELL", "/bin/sh")

    # pass kwargs we know to be supported
    for arg in ["cwd", "env"]:
        if arg in kwargs:
            platform_settings[arg] = kwargs[arg]

    # Some users are reporting that default (undocumented) limit 64k is too
    # low
    process = await asyncio.create_subprocess_shell(
        args,
        limit=STREAM_LIMIT,
        stdin=kwargs.get("stdin", False),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        **platform_settings,
    )
    out: List[str] = []
    err: List[str] = []

    def tee_func(line: bytes, sink: List[str], pipe: Optional[Any]) -> None:
        line_str = line.decode("utf-8").rstrip()
        sink.append(line_str)
        if not kwargs.get("quiet", False):
            # This is modified from the default implementation since
            # we want all output to be interleved on the same stream
            print(line_str, file=sys.stderr)

    loop = asyncio.get_running_loop()
    tasks = []
    if process.stdout:
        tasks.append(
            loop.create_task(_read_stream(process.stdout, lambda li: tee_func(li, out, stdout)))
        )
    if process.stderr:
        tasks.append(
            loop.create_task(_read_stream(process.stderr, lambda li: tee_func(li, err, stderr)))
        )

    await asyncio.wait(set(tasks))

    # We need to be sure we keep the stdout/stderr output identical with
    # the ones procued by subprocess.run(), at least when in text mode.
    check = kwargs.get("check", False)
    stdout = None if check else ""
    stderr = None if check else ""
    if out:
        stdout = os.linesep.join(out) + os.linesep
    if err:
        stderr = os.linesep.join(err) + os.linesep

    return CompletedProcess(
        args=args,
        returncode=await process.wait(),
        stdout=stdout,
        stderr=stderr,
    )


def run(args: Union[str, List[str]], **kwargs: Any) -> CompletedProcess:
    """Drop-in replacement for subprocess.run that behaves like tee.
    Extra arguments added by our version:
    echo: False - Prints command before executing it.
    quiet: False - Avoid printing output
    show_cwd: False - Prints the current working directory.
    """
    if isinstance(args, str):
        cmd = args
    else:
        # run was called with a list instead of a single item but asyncio
        # create_subprocess_shell requires command as a single string, so
        # we need to convert it to string
        cmd = join(args)

    check = kwargs.get("check", False)

    try:
        loop = asyncio.get_event_loop()
    except Exception:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    result = loop.run_until_complete(_stream_subprocess(cmd, **kwargs))
    atexit.register(loop.close)

    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd, output=result.stdout, stderr=result.stderr
        )
    return result
