# TranSVN-to-Git

There are a lot of scripts and tools around to convert a [SVN] repository to a
[git] repository. But usually they need a lot of manual steps. This script aims
to do most of the steps automated.

## License

This project is licensed under the [MIT License][MIT].

## Repositories without  branches, tags and trunk

Such kind of repositories are not easy to convert because of the missing default
settings. The script will start from the first [SVN] revision and will commit
this changes to the [git] repository. This will be done for each [SVN] revision
up to the latest.

## Libraries

This program is using some libraries. They are installed by the following way:

```python
pip install GitPython
pip install svn
```

You can find the homepage of the projects here:

- [GitPython][libgit]
- [svn][libsvn]

[git]: https://git-scm.com/
[MIT]: https://opensource.org/licenses/MIT
[SVN]: https://subversion.apache.org/
[libgit]: https://github.com/gitpython-developers/GitPython
[libsvn]: https://github.com/dsoprea/PySvn