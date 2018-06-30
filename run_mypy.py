#!/usr/bin/env/python

import sys
from subprocess import call

is_python2 = sys.version_info < (3, 0)

if __name__ == '__main__':
    if not is_python2:
        rc = call('mypy --strict --ignore-missing-imports ./potranslator/')
        raise SystemExit(rc)
