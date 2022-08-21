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


class TS2GOS:
    '''
    Class to control the process of the repository transformation
    '''

    def __init__(self, workspace: str) -> None:
        self.workspaceBase: str = self.__determineWorkspaceBase__(workspace)
        logging.info('workspaceBase [%s]', '{}'.format(self.workspaceBase))

    def __determineWorkspaceBase__(self: object, foldername: str) -> str:
        scriptpath: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        workspacePath: str = os.path.realpath(os.path.join(scriptpath, foldername))
        return workspacePath

    def workspaceBaseGet(self: object) -> str:
        return self.workspaceBase

    def workspaceFolderCreate(self: object, folder: str) -> bool:
        workspaceFolder: str = self.workspaceFolderGet(folder)
        if not self.workspaceFolderExists(workspaceFolder):
            try:
                logging.info('Create workspace folder [%s]', '{}'.format(workspaceFolder))
                os.makedirs(workspaceFolder)
            except OSError as error:
                logging.error('Cannot create workspace folder [%s]', '{}'.format(workspaceFolder))
        rValue = self.workspaceFolderExists(workspaceFolder)
        return rValue

    def workspaceFolderExists(self: object, folder: str) -> bool:
        workspaceFolder: str = self.workspaceFolderGet(folder)
        result: bool = (os.path.exists(workspaceFolder) and os.path.isdir(workspaceFolder))
        return result

    def workspaceFolderGet(self: object, folder: str) -> str:
        workspaceFolder = os.path.join(self.workspaceBase, folder)
        return workspaceFolder
