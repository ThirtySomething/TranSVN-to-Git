from pathlib import Path
from TransSVN_to_Git.Utilities import Utilities
import os
import pprint
import shutil
import svn.local
import svn.remote
import sys


class TTSG_SVN:
    _passWord = ''
    _repoUrl = ''
    _svnCO = 'tmpsvn'
    _userName = ''
    _workDir = ''

    def __init__(self, repoUrl, workDir, userName, passWord):
        self._passWord = passWord
        self._repoUrl = repoUrl
        self._userName = userName
        self._workDir = Path(workDir)

    def CheckOutRevision(self, revisionNr):
        svndir = Path(self.GetWorkingDir())
        if os.path.exists(svndir) and os.path.isdir(svndir):
            Utilities.DeleteFolderRecursive(svndir)
        repoRemote = svn.remote.RemoteClient(self._repoUrl)
        repoRemote.checkout(svndir, revisionNr)

    def GetLastRevision(self):
        repoRemote = svn.remote.RemoteClient(self._repoUrl)
        repoInfo = repoRemote.info()
        revision = int(repoInfo['commit_revision'])
        return revision

    def GetWorkingDir(self):
        locWdir = os.path.join(self._workDir, self._svnCO)
        return locWdir

    def Info(self):
        print('Repo URL [%s]' % (self._repoUrl))
        print('Revision [%d]' % (self.GetLastRevision()))
        print('Work dir [%s]' % (self._workDir))

    def SVNInfo(self):
        repoRemote = svn.remote.RemoteClient(self._repoUrl)
        repoInfo = repoRemote.info()
        pprint.pprint(repoInfo)
