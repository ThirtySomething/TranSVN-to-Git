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
    """
    Class to control OS operations
    """

    def __init__(self, workspace: str) -> None:
        """Default constructor

        Args:
            workspace (str): Name of workspace folder
        """
        self.workspaceBase: str = self.__determineWorkspaceBase__(workspace)
        logging.info("workspaceBase [%s]", "{}".format(self.workspaceBase))

    def __determineWorkspaceBase__(self: object, foldername: str) -> str:
        """Determine full os path to workspace folder in relation script path

        Args:
            foldername (str): Foldername in relation to script

        Returns:
            str: Full os path to folder in relation to script
        """
        scriptpath: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        workspacePath: str = os.path.realpath(os.path.join(scriptpath, foldername))
        return workspacePath

    def workspaceBaseGet(self: object) -> str:
        """Full os path name of workspace in relation to script

        Returns:
            str: Full os path to workspace
        """
        return self.workspaceBase

    def workspaceFolderCopy(self: object, foldersrc: str, folderdst: str):
        """Copy folder src to folder dst in workspace

        Args:
            foldersrc (str): Folder source name
            folderdst (str): Folder destination name
        """
        src: str = self.workspaceFolderGet(foldersrc)
        dst: str = self.workspaceFolderGet(folderdst)
        logging.debug("Copy [%s] to [%s]", "{}".format(src), "{}".format(dst))
        shutil.copytree(src, dst)

    def workspaceFolderCreate(self: object, folder: str) -> bool:
        """Create folder in workspace

        Args:
            folder (str): _description_

        Returns:
            bool: False on any failure, otherwise true
        """
        workspaceFolder: str = self.workspaceFolderGet(folder)
        if not self.workspaceFolderExists(workspaceFolder):
            try:
                logging.info("Create workspace folder [%s]", "{}".format(workspaceFolder))
                os.makedirs(workspaceFolder)
            except OSError as error:
                logging.error("Cannot create workspace folder [%s]", "{}".format(workspaceFolder))
        rValue = self.workspaceFolderExists(workspaceFolder)
        return rValue

    def workspaceFolderDelete(self: object, folder: str) -> None:
        """Delete complete folder including content in workspace

        Args:
            folder (str): Name of folder to delete
        """
        try:
            folder2Delete: str = self.workspaceFolderGet(folder)
            logging.debug("folder2Delete [%s]", "{}".format(folder2Delete))
            # Trick used with the onerror, see also
            # https://stackoverflow.com/questions/2656322/shutil-rmtree-fails-on-windows-with-access-is-denied
            shutil.rmtree(folder2Delete, ignore_errors=False, onerror=onerror)
        except Exception as ex:
            logging.error("Exception [%s]", "{}".format(ex))

    def workspaceFolderExists(self: object, folder: str) -> bool:
        """Check if given folder exists in workspace

        Args:
            folder (str): Name of folder to check

        Returns:
            bool: True if folder exists, otherwise false
        """
        workspaceFolder: str = self.workspaceFolderGet(folder)
        result: bool = os.path.exists(workspaceFolder) and os.path.isdir(workspaceFolder)
        return result

    def workspaceFolderGet(self: object, folder: str) -> str:
        """Get full os path of folder in workspace

        Args:
            folder (str): Name of folder in workspace

        Returns:
            str: Full os path to folder in workspace
        """
        workspaceFolder = os.path.join(self.workspaceBase, folder)
        return workspaceFolder

    def workspaceFolderRename(self: object, foldersrc: str, folderdst: str):
        """Rename folder in workspace

        Args:
            foldersrc (str): Folder name source
            folderdst (str): Folder name destination
        """
        src: str = self.workspaceFolderGet(foldersrc)
        dst: str = self.workspaceFolderGet(folderdst)
        logging.debug("Rename [%s] to [%s]", "{}".format(src), "{}".format(dst))
        shutil.move(src, dst)
