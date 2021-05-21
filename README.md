# Welcome

This book is built with a template from the [Executable Book Project](https://executablebooks.org).

## Install Requirements

The Python environments for building the eBook locally are stored in ROOT/requirements.txt (for Linux) and ROOT/window_environment.yml (for Windows).

On Linux install:
 * If Python2 and Python3 are installed, install requirements with
   * `pip3 install -r requirements.txt`
 * If only Python3 is installed, install the requirements with
   * `pip install -r requirements.txt`

On Windows, use Anaconda Prompt to install the hywin environment that contains all required packages for building the ebook:
 * `conda env create -f window_environment.yml`

## Build ebook

To update the website:

1. EDIT book and make changes, then BUILD the book (from `cd /git/`)
    `jb build hydro-informatics.github.io/`
1. Go to repo root directory (`cd /git/hydro-informatics.github.io/`)
1. Push changes to main branch
   `git add . commit push`
1. Push changes to gh-pages branch
   `ghp-import -n -p -f _build/html`

Read more at [[https://jupyterbook/publish/gh-pages.html]].

## Acknowledgements

[pypi-badge]: https://img.shields.io/pypi/v/jupyter-book.svg
[pypi-link]: https://pypi.org/project/jupyter-book
[conda-badge]: https://anaconda.org/conda-forge/jupyter-book/badges/version.svg
[conda-link]: https://anaconda.org/conda-forge/jupyter-book
