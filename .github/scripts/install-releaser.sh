set -eux
# Install Jupyter Releaser if it is not already installed

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if ! command -v jupyter-releaser &> /dev/null
then
    cd "${SCRIPT_DIR}/../.."
    pip install -e .
fi
