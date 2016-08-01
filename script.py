#! /usr/bin/env python
# -*- coding: utf-8 -*-

# python imports
import sys
import os
import subprocess

# project imports
from run import fwpath, venv_dir


def setup_venv():
    if not os.path.isdir(venv_dir):
        p = subprocess.Popen(['virtualenv', venv_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = p.communicate()
        if not p[1]:
            print p[0]
        else:
            print "error: please install virtualenv (sudo pip install virtualenv)"
            exit(0)


if __name__ == '__main__':
    setup_venv()
    args = ' '.join(sys.argv[1:])
    command = '%s/bin/python %s/run.py %s' % (venv_dir, fwpath, args)
    os.system(command)
