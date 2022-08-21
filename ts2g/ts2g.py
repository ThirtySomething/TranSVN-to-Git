'''
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
'''

import logging
import os

from ts2g.ts2gconfig import TS2GConfig
from ts2g.ts2ggit import TS2GGIT
from ts2g.ts2gos import TS2GOS
from ts2g.ts2gsvn import TS2GSVN


class TS2G:
    '''
    Class to control the process of the repository transformation
    '''

    def __init__(self: object, config: TS2GConfig) -> None:
        self.config: TS2GConfig = config
        self.oshandler: TS2GOS = TS2GOS(self.config.ts2g_workspace)
        self.githandler: TS2GGIT = TS2GGIT(self.config, self.oshandler)
        self.svnhandler: TS2GSVN = TS2GSVN(self.config, self.oshandler)
        logging.debug('config [%s]', '{}'.format(self.config))

    def addRevisionToGit(self: object, repoNameGit: str, repoNameSvn: str, commitmsg: str):
        # 1. Delete .svn folder
        deletionFolder: str = os.path.join(repoNameSvn, '.svn')
        self.oshandler.workspaceFolderDelete(deletionFolder)

        # 2. Copy .git folder
        foldersrc: str = os.path.join(repoNameGit, '.git')
        folderdst: str = os.path.join(repoNameSvn, '.git')
        self.oshandler.workspaceFolderCopy(foldersrc, folderdst)

        # 3. Delete git project
        self.oshandler.workspaceFolderDelete(repoNameGit)

        # 4. Rename to git project
        self.oshandler.workspaceFolderRename(repoNameSvn, repoNameGit)

        # 5. Do git add . and git commit -m message
        self.githandler.getRepositoryAdd(commitmsg)

    def process(self: object) -> bool:
        if False == self.oshandler.workspaceFolderCreate(''):
            return False

        if False == self.githandler.initProjectRepository():
            return False

        repoNameGit: str = self.githandler.getRepositoryName()

        maxRevision: int = self.svnhandler.getMaxRevisionNumber()
        logging.info('Max revision of [%s] is [%s]', '{}'.format(self.svnhandler.getRepositoryUrl()), '{}'.format(maxRevision))

        for revisionNumber in range(1, (maxRevision+1)):
            logging.info('Working on revision [%s/%s]', '{}'.format(revisionNumber), '{}'.format(maxRevision))
            repoNameSvn: str = self.svnhandler.checkoutRevision(revisionNumber)
            commitMessage: str = self.svnhandler.getCommitMessage(repoNameSvn, revisionNumber)
            self.addRevisionToGit(repoNameGit, repoNameSvn, commitMessage)

        return True
