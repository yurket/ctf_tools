#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import os
import stat


PYTHON_TEMPLATE = \
u"""#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function



def main():
    pass


if __name__ == '__main__':
    main()

"""

C_TEMPLATE = \
u"""#include <stdio.h>
#include <string.h>

#include <errno.h>
#include <sys/types.h>
#include <unistd.h>


int main()
{

    return 0;
}

"""

CPP_TEMPLATE = \
u"""#include <iostream>

using namespace std;

int main()
{
    cout << "cpp template" << endl;
    return 0;
}

"""

# correspondance table {language: {template, extension}}
_CORRESP_TABLE = {
    "python": {'template': PYTHON_TEMPLATE, 'ext': '.py'}
    , "c"   : {'template': C_TEMPLATE,      'ext': '.c'}
    , "cpp" : {'template': CPP_TEMPLATE,    'ext': '.cc'}
}


class COLORS:
    r"""
        Uses color-set escape sequences:
        start coloring: \[\e[color\], end coloring: \[\e[m\].
    """
    NOCOLOR = '\033[0m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'

#TODO: Auto-guess template by file extension?
#TODO: Add simple makefiles for c, cpp templates

def main():
    DESCR = 'Program creates ready-to-use source file templates for some' \
            'popular programming languages.'
    parser = argparse.ArgumentParser(description=DESCR)
    parser.add_argument('src_type', type=str, help='source file type [python, c, cpp]')
    parser.add_argument('filename', type=str, help='filelame of new source file')
    parser.add_argument('-f', '--force', action='store_true',
                        help='create file, even if another one exists with same name')
    args = parser.parse_args()
    filename = args.filename
    src_type = args.src_type.lower()
    force_replace = args.force

    if src_type not in _CORRESP_TABLE:
        print("%sError: Wrong src_type! Specify one of the supported: %s" %
              (COLORS.RED, _CORRESP_TABLE.keys()))
        return

    name, ext = os.path.splitext(filename)
    if not ext:
        filename += _CORRESP_TABLE[src_type]['ext']

    if os.path.exists(filename) and not force_replace:
        print("[!] File %s exists! Specify -f, --force option to replace it!"
              % filename)
        return

    with open(filename, 'wb') as f:
        f.write(_CORRESP_TABLE[src_type]['template'])

    # make python sources executable
    if src_type == 'python':
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC)


if __name__ == '__main__':
    main()
