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
import shutil


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat

    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


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

    def workspaceFolderDelete(self: object, folder: str) -> None:
        try:
            folder2Delete: str = self.workspaceFolderGet(folder)
            logging.debug('folder2Delete [%s]', '{}'.format(folder2Delete))
            # Trick used with the onerror, see also
            # https://stackoverflow.com/questions/2656322/shutil-rmtree-fails-on-windows-with-access-is-denied
            shutil.rmtree(folder2Delete, ignore_errors=False, onerror=onerror)
        except Exception as ex:
            logging.error('Exception [%s]', '{}'.format(ex))

    def workspaceFolderCopy(self: object, foldersrc: str, folderdst: str):
        src: str = self.workspaceFolderGet(foldersrc)
        dst: str = self.workspaceFolderGet(folderdst)
        logging.debug('Copy [%s] to [%s]', '{}'.format(src), '{}'.format(dst))
        shutil.copytree(src, dst)

    def workspaceFolderRename(self: object, foldersrc: str, folderdst: str):
        src: str = self.workspaceFolderGet(foldersrc)
        dst: str = self.workspaceFolderGet(folderdst)
        logging.debug('Rename [%s] to [%s]', '{}'.format(src), '{}'.format(dst))
        os.rename(src, dst)
