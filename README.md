# Welcome

This book is built with a template from the [Executable Book Project](https://executablebooks.org).

## Build info

Make sure `ghp-import` is installed:   `pip install ghp-import`

To update the website:

1. EDIT book and make changes, then BUILD the book (from `cd /git/`)
    `jb build hydro-informatics.github.io/`
1. Go to repo root directory (`cd /git/hydro-informatics.github.io/`)
1. Push changes to master branch
   `git add . commit push`
1. Push changes to gh-pages branch
   `ghp-import -n -p -f _build/html`

Read more at [[https://jupyterbook/publish/gh-pages.html]].

## Acknowledgements

[pypi-badge]: https://img.shields.io/pypi/v/jupyter-book.svg
[pypi-link]: https://pypi.org/project/jupyter-book
[conda-badge]: https://anaconda.org/conda-forge/jupyter-book/badges/version.svg
[conda-link]: https://anaconda.org/conda-forge/jupyter-book
