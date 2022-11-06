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

from ts2g.ts2gconfig import TS2GConfig
from ts2g.ts2gos import TS2GOS
from ts2g.ts2gsvninfo import TS2GSVNinfo

# https://www.devdungeon.com/content/working-git-repositories-python#toc-11


class TS2GGIT:
    """
    Class to control the git operations
    """

    def __init__(self: object, config: TS2GConfig, oshandler: TS2GOS) -> None:
        self.config: TS2GConfig = config
        self.oshandler: TS2GOS = oshandler
        self.projectFolder: str = self.oshandler.workspaceFolderGet(self.config.git_project)
        logging.debug("projectFolder [%s]", "{}".format(self.projectFolder))

    def gitRepositoryAdd(self: object, commitInfo: TS2GSVNinfo):
        try:
            projectFolder: str = self.gitRepositoryPath()
            projectRepo = git.Repo(projectFolder)
            files_to_add = []
            logging.info("Collecting files in folder [{}]".format(projectFolder))
            for filename in glob.iglob(projectFolder + "**/**", recursive=True):
                fname: str = str(filename)
                if os.path.isdir(fname):
                    # Skip directories
                    continue
                gitFile: str = fname.replace(projectFolder, "")
                if gitFile.startswith("\.git"):
                    # Skip everything of special git folder
                    continue
                files_to_add.append(gitFile)
            logging.info("Adding [{}] files to repo".format(len(files_to_add)))
            projectRepo.index.add(files_to_add)
            logging.info("Perform git commit")
            projectRepo.index.commit(commitInfo.commitmsg, author_date=commitInfo.date, commit_date=commitInfo.date)
            logging.info("Git commit done")
        except Exception as ex:
            logging.error("Exception [%s]", "{}".format(ex))

    def gitRepositoryName(self: object) -> str:
        return self.config.git_project

    def gitRepositoryPath(self: object) -> str:
        return os.path.join(self.projectFolder, "")

    def initProjectRepository(self: object) -> bool:
        if self.oshandler.workspaceFolderExists(self.projectFolder):
            logging.error("Git project [%s] already exists in workspace [%s]", "{}".format(self.config.git_project), "{}".format(self.oshandler.workspaceBaseGet()))
            return False

        if not self.oshandler.workspaceFolderCreate(self.config.git_project):
            return False

        projectFolder: str = self.gitRepositoryPath()
        projectRepo = git.Repo.init(projectFolder)
        if not projectRepo:
            logging.error("Cannot create bare repo [%s]", "{}".format(projectFolder))
            return False

        return True
