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

import logging
import os
import dirsync
import time

from ts2g.ts2gconfig import TS2GConfig
from ts2g.ts2ggit import TS2GGIT
from ts2g.ts2gos import TS2GOS
from ts2g.ts2gsvn import TS2GSVN
from ts2g.ts2gsvninfo import TS2GSVNinfo


class TS2G:
    FOLDER_GIT = ".git"
    FOLDER_SVN = ".svn"

    """
    Class to control the process of the repository transformation
    """

    def __init__(self: object, config: TS2GConfig) -> None:
        """Default constructor

        Args:
            config (TS2GConfig): Config settings
        """
        self.config: TS2GConfig = config
        self.oshandler: TS2GOS = TS2GOS(self.config.value_get("TS2G", "workspace"))
        self.githandler: TS2GGIT = TS2GGIT(self.config, self.oshandler)
        self.svnhandler: TS2GSVN = TS2GSVN(self.config, self.oshandler)
        logging.debug("config [%s]", self.config)

    def addRevisionToGit(self: object, repoNameGit: str, repoNameSvn: str, commitInfo: TS2GSVNinfo):
        """Sync SVN directory to GIT directory, do a "git add . && git commit -m "..." " on GIT directory

        Args:
            repoNameGit (str): Folder name of GIT destination directory
            repoNameSvn (str): Folder name of SVN source directory
            commitInfo (TS2GSVNinfo): SVN Commit info object
        """
        # Create source and destination names for sync
        folder_src: str = self.oshandler.workspaceFolderGet(repoNameSvn)
        folder_dst: str = self.oshandler.workspaceFolderGet(repoNameGit)
        folder_git_src: str = self.oshandler.workspaceFolderGet(os.path.join(repoNameGit, self.FOLDER_GIT))
        folder_git_dst: str = self.oshandler.workspaceFolderGet(self.FOLDER_GIT)

        # Move .git folder outside of repo
        self.oshandler.workspaceFolderRename(folder_git_src, folder_git_dst)

        # Sync folders
        dirsync.sync(folder_src, folder_dst, "sync", verbose=False, exclude=[self.FOLDER_SVN], purge=True)

        # Move .git folder back to repo
        self.oshandler.workspaceFolderRename(folder_git_dst, folder_git_src)

        # Do git add . and git commit -m message
        self.githandler.gitRepositoryAdd(commitInfo)

    def process(self: object) -> bool:
        """Initialize and start conversion process

        Returns:
            bool: False on any failure, otherwise true
        """

        try:
            if False == self.oshandler.workspaceFolderCreate(""):
                return False

            if False == self.githandler.initProjectRepository():
                return False

            repoNameGit: str = self.githandler.gitRepositoryName()
            revisionLimit: int = int(self.config.value_get("SVN", "revision_limit"))

            maxRevision: int = self.svnhandler.getMaxRevisionNumber()
            logging.info("Max revision of [%s] is [%s], limited to [%s]", "{}".format(self.svnhandler.getRepositoryUrl()), "{}".format(maxRevision), "{}".format(revisionLimit))

            repoNameSvn: str = ""
            for revisionNumber in range(1, (maxRevision + 1)):
                process_start: float = time.time()
                logging.info("Working on revision [%s/%s]", "{}".format(revisionNumber), "{}".format(maxRevision))
                if 1 == revisionNumber:
                    repoNameSvn = self.svnhandler.checkoutRevision(revisionNumber)
                else:
                    self.svnhandler.svnUpdateToRevision(repoNameSvn, revisionNumber)
                commitInfo: TS2GSVNinfo = self.svnhandler.getCommitInfo(repoNameSvn, revisionNumber)
                self.addRevisionToGit(repoNameGit, repoNameSvn, commitInfo)
                process_end: float = time.time()
                process_duration: float = process_end - process_start
                logging.info(f"Revision [{revisionNumber}] transferred within [{process_duration:.2f}] seconds")
                if 0 != revisionLimit and revisionLimit <= revisionNumber:
                    logging.info(f"Revision limit of [{revisionLimit}] reached, abort")
                    break

            # Delete svn folder
            folder_svn: str = self.oshandler.workspaceFolderGet(repoNameSvn)
            self.oshandler.workspaceFolderDelete(folder_svn)
        except Exception as ex:
            logging.error("Exception [%s]", "{}".format(ex))
            return False

        return True
