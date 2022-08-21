'''
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
'''

import logging
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET

import svn.local
import svn.remote

from ts2g.ts2gconfig import TS2GConfig
from ts2g.ts2gos import TS2GOS


class TS2GSVN:
    '''
    Class to control the Subversion operations
    '''

    def __init__(self: object, config: TS2GConfig, oshandler: TS2GOS) -> None:
        self.config: TS2GConfig = config
        self.oshandler: TS2GOS = oshandler
        self.repositoryurl: str = self.config.svn_repositoryurl
        self.repositoryname: str = self.__determineRepositoryName__()
        logging.debug('repositoryurl [%s]', '{}'.format(self.repositoryurl))
        logging.debug('repositoryname [%s]', '{}'.format(self.repositoryname))

    def __determineRepositoryName__(self: object) -> str:
        url_parts = urllib.parse.urlparse(self.repositoryurl.rstrip('/'))
        path_parts = url_parts[2].rpartition('/')
        return path_parts[2]

    def __getCheckoutName__(self: object, revision: int) -> str:
        revisionName: str = 'svn_' + self.repositoryname + '_' + str(revision)
        checkoutName: str = self.oshandler.workspaceFolderGet(revisionName)
        return checkoutName

    def getMaxRevisionNumber(self: object) -> int:
        reopClient = svn.remote.RemoteClient(self.repositoryurl, username=self.config.svn_user, password=self.config.svn_password)
        repoInfo = reopClient.info()
        revision: int = repoInfo['entry_revision']
        return revision

    def getRepositoryUrl(self: object) -> str:
        return self.repositoryurl

    def getRepositoryName(self: object) -> str:
        return self.repositoryname

    def getCommitMessage(self: object, checkout: str, revision: int) -> str:
        message: str = ''
        try:
            proc = subprocess.Popen(['svn', '--non-interactive', 'log', '-r', str(revision) + ':' + str(revision), '--xml', checkout], stdout=subprocess.PIPE)
            output = proc.stdout.read()
            svnXml: str = output.decode('ascii')
            root = ET.fromstring(svnXml)
            for element in root.findall('logentry'):
                message: str = element.find('msg').text
        except Exception as ex:
            logging.error('Exception [%s]', '{}'.format(ex))
        return message

    def checkoutRevision(self: object, revision: int) -> str:
        pathCheckout: str = self.__getCheckoutName__(revision)
        logging.info('Checkout revision [%s] to [%s]', '{}'.format(revision), '{}'.format(pathCheckout))
        reopClient = svn.remote.RemoteClient(self.repositoryurl, username=self.config.svn_user, password=self.config.svn_password)
        reopClient.checkout(pathCheckout, revision)
        return pathCheckout
