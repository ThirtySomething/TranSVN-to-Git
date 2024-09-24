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

    def __init__(self: object, config: TS2GConfig, oshandler: TS2GOS) -> None:
        self.config: TS2GConfig = config
        self.oshandler: TS2GOS = oshandler
        self.repositoryurl: str = self.config.value_get("SVN", "repositoryurl")
        self.repositoryname: str = self.__determineRepositoryName__()
        logging.debug("repositoryurl [%s]", "{}".format(self.repositoryurl))
        logging.debug("repositoryname [%s]", "{}".format(self.repositoryname))

    def __determineRepositoryName__(self: object) -> str:
        url_parts = urllib.parse.urlparse(self.repositoryurl.rstrip("/"))
        path_parts = url_parts[2].rpartition("/")
        return path_parts[2]

    def checkoutRevision(self: object, revision: int) -> str:
        revisionName: str = "svn_" + self.repositoryname + "_" + str(revision)
        pathCheckout: str = self.oshandler.workspaceFolderGet(revisionName)
        logging.info("Checkout revision [%s] to [%s]", "{}".format(revision), "{}".format(pathCheckout))
        reopClient = svn.remote.RemoteClient(
            self.repositoryurl,
            username=self.config.value_get("SVN", "user"),
            password=self.config.value_get("SVN", "password"),
        )
        reopClient.checkout(pathCheckout, revision)
        return revisionName

    def getCommitInfo(self: object, checkout: str, revision: int) -> TS2GSVNinfo:
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
                info: TS2GSVNinfo = TS2GSVNinfo(element.find("author").text, element.find("msg").text, parser.parse(element.find("date").text), revision)
            logging.info(info)
        except Exception as ex:
            logging.error("Exception [%s]", "{}".format(ex))
        return info

    def svnUpdateToRevision(self: object, checkout: str, revision: int) -> None:
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

    def getMaxRevisionNumber(self: object) -> int:
        reopClient = svn.remote.RemoteClient(self.repositoryurl, username=self.config.value_get("SVN", "user"), password=self.config.value_get("SVN", "password"))
        repoInfo = reopClient.info()
        revision: int = repoInfo["entry_revision"]
        return revision

    def gitRepositoryName(self: object) -> str:
        return self.repositoryname

    def getRepositoryUrl(self: object) -> str:
        return self.repositoryurl
