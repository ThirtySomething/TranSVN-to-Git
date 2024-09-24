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
import logging.config

from ts2g.ts2g import TS2G
from ts2g.ts2gconfig import TS2GConfig

TS2G_CONFIG = TS2GConfig("program.json")
TS2G_CONFIG.save()

# Setup logging for dealing with UTF-8, unfortunately not available for basicConfig
LOGGER_SETUP = logging.getLogger()
LOGGER_SETUP.setLevel(TS2G_CONFIG.value_get("LOGGING", "loglevel").upper())
LOGGER_HANDLER = logging.FileHandler(TS2G_CONFIG.value_get("LOGGING", "logfile"), "w", "utf-8")
LOGGER_HANDLER.setFormatter(logging.Formatter(TS2G_CONFIG.value_get("LOGGING", "logstring")))
LOGGER_SETUP.addHandler(LOGGER_HANDLER)

# Script to convert a Subversion repository to a git repository
if __name__ == "__main__":
    logging.info("debugFlag is set to [%s]", "{}".format(TS2G_CONFIG.value_get("LOGGING", "loglevel").upper()))
    converter = TS2G(TS2G_CONFIG)
    status = converter.process()
    logging.info("process result is [%s]", "{}".format(status))
