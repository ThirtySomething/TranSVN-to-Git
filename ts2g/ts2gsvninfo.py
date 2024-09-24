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

import datetime


class TS2GSVNinfo:
    """
    Data object
    """

    def __init__(self: object, author: str, commitmsg: str, date: datetime, revision: int) -> None:
        self._author: str = author
        self._commitmsg: str = commitmsg
        self._date: datetime = date
        self._revision: int = revision

    def __str__(self) -> str:
        measstr: str = "author [{}], commitmsg [{}], date [{}], revision [{}]".format(self._author, self._commitmsg, self._date, self._revision)
        return measstr

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def author(self: object) -> str:
        return self._author

    @property
    def commitmsg(self: object) -> str:
        return self._commitmsg

    @property
    def date(self: object) -> datetime:
        return self._date

    @property
    def revision(self: object) -> int:
        return self._revision
