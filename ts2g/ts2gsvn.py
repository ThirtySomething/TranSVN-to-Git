"""
******************************************************************************
Copyright 2020 ThirtySomething
******************************************************************************
This file is part of TRANSSVN-TO-GIT.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
******************************************************************************
"""

import logging
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET
import datetime

import svn.local
import svn.remote
from dateutil import parser

from ts2g.ts2gconfig import TS2GConfig
from ts2g.ts2gos import TS2GOS
from ts2g.ts2gsvninfo import TS2GSVNinfo


class TS2GSVN:
    """
    Class to control the Subversion operations
    """

    FOLDER_SVN = ".svn"

    def __init__(self: object, config: TS2GConfig, oshandler: TS2GOS) -> None:
        """Default constructor

        Args:
            config (TS2GConfig): Config options
            oshandler (TS2GOS): Encapsulated os functions
        """
        self.config: TS2GConfig = config
        self.oshandler: TS2GOS = oshandler
        self.repositoryurl: str = self.config.value_get("SVN", "repositoryurl")
        self.repositoryname: str = self.determineRepositoryName()
        self.prefixmsg: bool = self.determinePrefixFlag()
        logging.debug("repositoryurl [%s]", "{}".format(self.repositoryurl))
        logging.debug("repositoryname [%s]", "{}".format(self.repositoryname))

    def checkoutRevision(self: object, revision: int) -> str:
        """Checkout specific SVN revision

        Args:
            revision (int): SVN revision to checkout

        Returns:
            str: Name of checkout folder
        """
        revisionName: str = "svn_" + self.repositoryname
        pathCheckout: str = self.oshandler.workspaceFolderGet(revisionName)
        logging.debug("Checkout revision [%s] to [%s]", "{}".format(revision), "{}".format(pathCheckout))
        reopClient = svn.remote.RemoteClient(
            self.repositoryurl,
            username=self.config.value_get("SVN", "user"),
            password=self.config.value_get("SVN", "password"),
        )
        reopClient.checkout(pathCheckout, revision)
        return revisionName

    def determinePrefixFlag(self: object) -> bool:
        """Determine if prefix for commit messages should be used or not

        Returns:
            bool: True if prefix has to be used, otherwise False
        """
        flag: bool = False
        flag_raw: str = self.config.value_get("GIT", "commit_msg_svn_nr").lower()

        if "y" == flag_raw[0] or "j" == flag_raw[0] or "1" == flag_raw[0]:
            flag = True

        return flag

    def determineRepositoryName(self: object) -> str:
        """Strip repository name from URL

        Returns:
            str: Name of repository
        """
        url_parts = urllib.parse.urlparse(self.repositoryurl.rstrip("/"))
        path_parts = url_parts[2].rpartition("/")
        return path_parts[2]

    def getCommitInfo(self: object, checkout: str, revision: int) -> TS2GSVNinfo:
        """Determine SVN commit information for given revision number

        Args:
            checkout (str): Name of SVN checkout folder
            revision (int): Revision number to get info for

        Returns:
            TS2GSVNinfo: Object containing SVN commit info
        """
        try:
            pathCheckout: str = self.oshandler.workspaceFolderGet(checkout)
            cmdString: str = "svn --non-interactive --no-auth-cache --username {} --password {} log -r{}:{} --xml {}".format(
                self.config.value_get("SVN", "user"), self.config.value_get("SVN", "password"), revision, revision, pathCheckout
            )
            cmdArgs: [] = cmdString.split()
            proc = subprocess.Popen(cmdArgs, stdout=subprocess.PIPE)
            output = proc.stdout.read()
            svnXml: str = output.decode("utf-8")
            root = ET.fromstring(svnXml)
            for element in root.findall("logentry"):
                author: str = element.find("author").text
                commitdate: datetime = parser.parse(element.find("date").text)
                commitmsg_raw: str = element.find("msg").text
                if None == commitmsg_raw:
                    commitmsg_raw = ""
                commitmsg_raw = commitmsg_raw.strip()
                commitmsg: str = ""
                if self.prefixmsg:
                    commitmsg = "#{}: {}".format(revision, commitmsg_raw)
                else:
                    commitmsg = commitmsg_raw
                info: TS2GSVNinfo = TS2GSVNinfo(author, commitmsg, commitdate, revision)
            logging.debug(info)
        except Exception as ex:
            logging.error("Exception [%s]", "{}".format(ex))
        return info

    def getMaxRevisionNumber(self: object) -> int:
        """Determine maximum number of revisions

        Returns:
            int: Maximum revision number of repository
        """
        reopClient = svn.remote.RemoteClient(self.repositoryurl, username=self.config.value_get("SVN", "user"), password=self.config.value_get("SVN", "password"))
        repoInfo = reopClient.info()
        revision: int = repoInfo["entry_revision"]
        return revision

    def svnUpdateToRevision(self: object, checkout: str, revision: int) -> None:
        """Update SVN checkout to given revision

        Args:
            checkout (str): Name of SVN checkout folder
            revision (int): Revision to update to
        """
        try:
            pathCheckout: str = self.oshandler.workspaceFolderGet(checkout)
            cmdString: str = "svn --non-interactive --no-auth-cache --username {} --password {} update -r{} {}".format(
                self.config.value_get("SVN", "user"), self.config.value_get("SVN", "password"), revision, pathCheckout
            )
            cmdArgs: [] = cmdString.split()
            proc = subprocess.Popen(cmdArgs, stdout=subprocess.PIPE)
            output = proc.stdout.read()
            svnXml: str = output.decode("utf-8")
        except Exception as ex:
            logging.error("Exception [%s]", "{}".format(ex))

    def getRepositoryName(self: object) -> str:
        """Get name of SVN repository

        Returns:
            str: Name of SVN repository
        """
        return self.repositoryname

    def getRepositoryUrl(self: object) -> str:
        """Get URL of SVN repository

        Returns:
            str: URL of SVN repository
        """
        return self.repositoryurl
