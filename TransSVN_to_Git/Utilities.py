import pathlib

class Utilities:
    @staticmethod
    def DeleteFolderRecursive(pth):
        for sub in pth.iterdir():
            if sub.is_dir():
                Utilities.DeleteFolderRecursive(sub)
            else:
                sub.unlink()
            pth.rmdir() # if you just want to delete dir content, remove this line
