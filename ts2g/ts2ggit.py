"""
******************************************************************************
Copyright 2020 ThirtySomething
******************************************************************************
This file is part of TRANSSVN-TO-GIT.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
******************************************************************************
"""

import glob
import logging
import os

import git
import git.util

from ts2g.ts2gconfig import TS2GConfig
from ts2g.ts2gos import TS2GOS
from ts2g.ts2gsvninfo import TS2GSVNinfo

# https://www.devdungeon.com/content/working-git-repositories-python#toc-11


class TS2GGIT:
    """
    Class to control the git operations
    """

    def __init__(self: object, config: TS2GConfig, oshandler: TS2GOS) -> None:
        """Default constructor

        Args:
            config (TS2GConfig): Config options
            oshandler (TS2GOS): Encapsulated file system operations
        """
        self.config: TS2GConfig = config
        self.oshandler: TS2GOS = oshandler
        self.projectFolder: str = self.oshandler.workspaceFolderGet(self.config.value_get("GIT", "project"))
        logging.debug("projectFolder [%s]", "{}".format(self.projectFolder))

    def getActor(self: object, name: str) -> git.Actor:
        """Create actor object used in git commit based on configured usermap

        Args:
            name (str): Name of SVN committer

        Returns:
            git.Actor: Object with username and email as configured
        """
        rval: git.Actor = git.Actor(name=name, email="")
        usermap: list[str] = self.config.value_get("SVN", "usermap")
        for curuser in usermap:
            if curuser.startswith(name):
                logging.debug("found user [%s]", "{}".format(curuser))
                parts = curuser.split("=")
                rval = git.Actor(name=parts[0].strip(), email=parts[1].strip())
                break
        return rval

    def gitRepositoryAdd(self: object, commitInfo: TS2GSVNinfo):
        """Perform git add . and a git commit

        Args:
            commitInfo (TS2GSVNinfo): Information about SVN commit like message, committer, revision
        """
        try:
            projectFolder: str = self.gitRepositoryPath()
            projectRepo = git.Repo(projectFolder)
            logging.debug("Add changes to repository")
            projectRepo.git.add(all=True)
            logging.debug("Perform git commit")
            commitmsg: str = commitInfo.commitmsg
            if not commitmsg:
                commitmsg = ""
            actor: git.Actor = self.getActor(commitInfo.author)
            projectRepo.index.commit(message=commitmsg, author=actor, committer=actor, author_date=commitInfo.date, commit_date=commitInfo.date)
            logging.debug("Git commit done")
        except Exception as ex:
            logging.error("Exception [%s]", "{}".format(ex))

    def gitRepositoryName(self: object) -> str:
        """Retrieve name of GIT destination repo from config options

        Returns:
            str: Plain name of GIT repo
        """
        return self.config.value_get("GIT", "project")

    def gitRepositoryPath(self: object) -> str:
        """Get full qualified path name (=> location) of GIT repo

        Returns:
            str: Full os path name of GIT repo
        """
        return os.path.join(self.projectFolder, "")

    def initProjectRepository(self: object) -> bool:
        """Create empty GIT repo

        Returns:
            bool: False on any failure, otherwise True
        """
        if self.oshandler.workspaceFolderExists(self.projectFolder):
            logging.error("Git project [%s] already exists in workspace [%s]", "{}".format(self.config.value_get("GIT", "project")), "{}".format(self.oshandler.workspaceBaseGet()))
            return False

        if not self.oshandler.workspaceFolderCreate(self.config.value_get("GIT", "project")):
            return False

        projectFolder: str = self.gitRepositoryPath()
        projectRepo = git.Repo.init(projectFolder)
        if not projectRepo:
            logging.error("Cannot create bare repo [%s]", "{}".format(projectFolder))
            return False

        return True
