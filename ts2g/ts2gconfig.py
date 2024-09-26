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

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../vendor/MDO/MDO/"))

from MDO import MDO


class TS2GConfig(MDO):
    """
    Contains dynamic settings of TS2G
    """

    def setup(self: object) -> None:
        """Config options used for transforming SVN repo into GIT repo."""
        self.add("GIT", "commit_msg_svn_nr", "yes")
        self.add("GIT", "project", "<enter project name here>")
        self.add("LOGGING", "logfile", "program.log")
        self.add("LOGGING", "loglevel", "info")
        self.add("LOGGING", "logstring", "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s:%(funcName)s | %(message)s")
        self.add("SVN", "revision_limit", 0)
        self.add("SVN", "password", "<enter password here>")
        self.add("SVN", "repositoryurl", "<enter svn url here>")
        self.add("SVN", "user", "<enter user here>")
        self.add("SVN", "usermap", ["username = email"])
        self.add("TS2G", "workspace", "./workspace")
