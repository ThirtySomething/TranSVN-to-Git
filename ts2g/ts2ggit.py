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

from git import Repo

from ts2g.ts2gconfig import TS2GConfig
from ts2g.ts2gos import TS2GOS


class TS2GGIT:
    '''
    Class to control the Subversion operations
    '''

    def __init__(self: object, config: TS2GConfig, oshandler: TS2GOS) -> None:
        self.config: TS2GConfig = config
        self.oshandler: TS2GOS = oshandler
        self.projectFolder: str = self.oshandler.workspaceFolderGet(self.config.git_project)
        logging.debug('projectFolder [%s]', '{}'.format(self.projectFolder))

    def initProjectRepository(self: object) -> bool:
        if self.oshandler.workspaceFolderExists(self.projectFolder):
            logging.error('Git project [%s] already exists in workspace [%s]', '{}'.format(self.config.git_project), '{}'.format(self.oshandler.workspaceBaseGet()))
            return False

        if not self.oshandler.workspaceFolderCreate(self.config.git_project):
            return False

        projectRepo = Repo.init(self.projectFolder)
        if not projectRepo:
            logging.error('Cannot create bare repo [%s]', '{}'.format(self.projectFolder))
            return False

        return True
