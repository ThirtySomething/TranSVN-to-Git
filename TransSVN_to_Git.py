import sys
from TransSVN_to_Git.TTSG_SVN import TTSG_SVN


def main():
    print('Here we are!')
    svnRepo = TTSG_SVN('svn://192.168.71.10/texdocs',
                       'C:\\Users\\jochen\\Downloads\\TranSVN-to-Git',
                       'jochen',
                       'cul8er'
                       )
    svnRepo.Info()
    # svnRepo.SVNInfo()
    print(svnRepo.GetWorkingDir())
    svnRepo.CheckOutRevision(1)
    return 0


main()
