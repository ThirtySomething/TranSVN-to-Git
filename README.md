# TranSVN-to-Git

Convert a [Subversion][SVN] repository into a [git][GIT] repository.

## License

This project is licensed under the [MIT License][MIT].

## Motivation

There are a lot of scripts and tools to convert a [Subversion][SVN] repository to a [git][GIT] repository. But usually they need at least manual steps. This script aims to do most of the steps automated.

## Prerequisites

You need to have [git][GIT] and [Subversion][SVN] installed and located in the path. Use the following links:

* For [git][GIT]: <https://git-scm.com/downloads> - Just download, accept the defaults and install.
* For [Subversion][SVN]: <https://tortoisesvn.net/downloads.de.html> - Download, start the setup and enable at least the option `command line client tools`.

## How it works

In the config file there are some required settings. The first setting is the source of the [Subversion][SVN] - the name, the url and the credentials to the repository. The second setting is the destination - the name of the [git][GIT] repository.

The programm will create in a working folder an empty [git][GIT] repository. Then it will loop over all [Subversion][SVN] revisions. For each revision it will do

* A [Subversion][SVN] checkout
* Synchronize the [SVN][SVN] checkout to the [git][GIT] repository ignoring the `.git` and `.svn` folder
* Do `git add .` and `git commit -m <SVN message>` for the git repository
* Delete the [Subversion][SVN] checkout

Because of this the whole process is very time consuming. But hey - still start the script and start/continue with other task ;-)

Maybe there is a misunderstanding of how [git][GIT] works. The expected result is a [git][GIT] repository in the shape of your [SVN][SVN] repository including almost the whole history.<sup>1)</sup> If some [SVN externals][SVN_EXTERNAL] are used, they must be replaced manually as [git submodules][GIT_SUBMODULE]. Additional all special [SVN][SVN] attributes needs to be revised if there is a equivalent for [git][GIT] repository - they need also to be set manually.

<sup>1)</sup> The reason for almost the whole history is that you cannot add empty folders to a [git][GIT] repository without dirty hacks. So if there are empty folders committed to your [SVN][SVN] repository, the same commit cannot be done on a [git][GIT] repository.

## Libraries

This program is using some libraries. The requirements are listed in the file `requirements.txt`. If you start the program using one of the `runme` scripts, then a virtual environment `venv` will be created and the required libraries will be installed inside.

You can find the homepage of the projects here:

* [GitPython][LIBGIT]
* [svn][LIBSVN]
* [pysvn][PYSVN]

## SVN authors

To get a list of the SVN authors for a mapping, you might want to use this statement:

```bash
# bash command
svn log -q --no-auth-cache --username <USER> --password <PASSWORD> <REPOSITORY URL> | grep -i '(' | cut -d '|' -f 2 | sort -u > users.txt
```

Then you have to update/extend the file to match the following format:

```bash
<SVN-USERNAME> = Firstname Lastname <email@example.com>
```

[GIT]: https://git-scm.com/
[GIT_SUBMODULE]: https://git-scm.com/book/en/v2/Git-Tools-Submodules
[LIBGIT]: https://github.com/gitpython-developers/GitPython
[LIBSVN]: https://github.com/dsoprea/PySvn
[MIT]: https://opensource.org/licenses/MIT
[PYSVN]: https://pysvn.sourceforge.io
[SVN]: https://subversion.apache.org/
[SVN_EXTERNAL]: https://svnbook.red-bean.com/en/1.7/svn.advanced.externals.html
