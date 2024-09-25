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

## The setup

On the first startup of the script a config file is written - and then the script aborts with a failure because of the invalid default settings. The config file is named `program.json` and looks like this one:

```json
{
    "GIT": {
        # Use "#XXX: " as prefix for GIT commit message where XXX is the SVN revision number
        "commit_msg_svn_nr": "yes",
        # Name of the GIT repo in workspace folder (=> Destination repo)
        "project": "<enter project name here>"
    },
    "LOGGING": {
        # Name of the log file
        "logfile": "program.log",
        # Loglevel, either "info" or "debug"
        "loglevel": "info",
        # Format of log message
        "logstring": "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s:%(funcName)s | %(message)s"
    },
    "SVN": {
        # Password for SVN user
        "password": "<enter password here>",
        # URL to SVN repository
        "repositoryurl": "<enter svn url here>",
        # Name of used SVN user
        "user": "<enter user here>",
        # Map of SVN commit user to emails used for GIT commit
        "usermap": [
            "username = email"
        ]
    },
    "TS2G": {
        # Name of workspace folder
        "workspace": "./workspace"
    }
}
```

## The process

The first action is the creation of a workspace folder. Inside of this folder all work will be done.

The next step is the creation of an empty empty [git][GIT] repository in the workspace folder. This repository contains the result of the transformation.

Then the latest [SVN revision][SVN] number is determined. If the URL or the credentials are invalid, the program stops here.

Now the loop from the first to the latest revision starts:

- For the first revision do a [SVN checkout][SVN], for all others do a [SVN update to revision][SVN]
- Determine the commit information for the [SVN revision][SVN]
- Synchronize the [SVN][SVN] checkout to the [git][GIT] repository ignoring the `.git` and `.svn` folder
- Do `git add .` and `git commit -m "<SVN message>"` for the git repository

After the last revision is converted, the [SVN checkout][SVN] will be deleted.

The whole process is very time consuming. But hey - still start the script and start/continue with another task ;-)

Maybe there is a misunderstanding of how [git][GIT] works. The expected result is a [git][GIT] repository in the shape of your [SVN][SVN] repository including almost the whole history.<sup>1)</sup> If some [SVN externals][SVN_EXTERNAL] are used, they must be replaced manually as [git submodules][GIT_SUBMODULE]. Additional all special [SVN][SVN] attributes needs to be revised if there is a equivalent for [git][GIT] a repository - and if required they need to be set manually.

<sup>1)</sup> The reason for almost the whole history is that you cannot add empty folders to a [git][GIT] repository without dirty hacks. So if there are empty folders committed to your [SVN][SVN] repository, the same commit cannot be done on a [git][GIT] repository.

## Libraries

This program is using some libraries. The requirements are listed in the file `requirements.txt`. If you start the program using one of the `runme` scripts, then a virtual environment `venv` will be created and the required libraries will be installed inside.

You can find the homepage of the projects here:

* [GitPython][LIBGIT]
* [svn][LIBSVN]
* [pysvn][PYSVN]

## SVN authors

To get a list of the SVN authors for a mapping (see config above), you might want to use this statement:

```bash
# bash command
svn log -q --no-auth-cache --username <USER> --password <PASSWORD> <REPOSITORY URL> | grep -i '(' | cut -d '|' -f 2 | sort -u > users.txt
```

Then you have to update/extend the file to match the following format:

```bash
SVN-USERNAME = email@example.com
```

[GIT]: https://git-scm.com/
[GIT_SUBMODULE]: https://git-scm.com/book/en/v2/Git-Tools-Submodules
[LIBGIT]: https://github.com/gitpython-developers/GitPython
[LIBSVN]: https://github.com/dsoprea/PySvn
[MIT]: https://opensource.org/licenses/MIT
[PYSVN]: https://pysvn.sourceforge.io
[SVN]: https://subversion.apache.org/
[SVN_EXTERNAL]: https://svnbook.red-bean.com/en/1.7/svn.advanced.externals.html
