# TranSVN-to-Git

Convert a [Subversion][SVN] repository into a [git][GIT] repository.

## License

This project is licensed under the [MIT License][MIT].

## Motivation

There are a lot of scripts and tools to convert a [Subversion][SVN] repository to a [git][GIT] repository. But usually they need at least manual steps. This script aims to do all of the steps automated.

## How it works

In the config file there are some required settings. The first setting is the source of the [Subversion][SVN] - the name, the url and the credentials to the repository. The second setting is the destination - the name of the [git][GIT] repository.

Then the programm will create in a working folder an empty [git][GIT] repository. Then it will loop over all [Subversion][SVN] revisions. For each revision it will do

* A [Subversion][SVN] checkout
* In the checkout delete the `.svn` folder
* Move the `.git` folder of the [git][GIT] repository to the folder of the [Subversion][SVN] checkout
* Do `git add .` and `git commit -m <SVN message>` for the git repository
* Delete the previous [git][GIT] repository
* Treat the [Subversion][SVN] checkout as [git][GIT] repository and move it to the previous location

Maybe there is a misunderstanding of how [git][GIT] works. We will see what the result will be.

## Libraries

This program is using some libraries. The requirements are listed in the file `requirements.txt`. If you start the program using one of the `runme` scripts, then a virtual environment `venv` will be created and the required libraries will be installed inside.

You can find the homepage of the projects here:

* [GitPython][LIBGIT]
* [svn][LIBSVN]
* [pysvn][PYSVN]

[GIT]: https://git-scm.com/
[MIT]: https://opensource.org/licenses/MIT
[SVN]: https://subversion.apache.org/
[LIBGIT]: https://github.com/gitpython-developers/GitPython
[LIBSVN]: https://github.com/dsoprea/PySvn
[PYSVN]: https://pysvn.sourceforge.io
