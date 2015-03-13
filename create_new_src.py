#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import os


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
    """
        Uses color-set escape sequences:
        start coloring: \[\e[color\], end coloring: \[\e[m\].
    """
    NOCOLOR = '\033[0m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'

#TODO: check if files already exist

def main():
    DESCR = 'program creates ready-to-use template for average python script.'
    parser = argparse.ArgumentParser(description=DESCR)
    parser.add_argument('src_type', type=str, help='source file type [python, c, cpp]')
    parser.add_argument('filename', type=str, help='filelame of new source file')
    args = parser.parse_args()

    filename = args.filename
    src_type = args.src_type.lower()

    if src_type in _CORRESP_TABLE:
        name, ext = os.path.splitext(filename)
        if not ext:
            filename += _CORRESP_TABLE[src_type]['ext']
        with open(filename, 'wb') as f:
            f.write(_CORRESP_TABLE[src_type]['template'])
    else:
        print("%sError: Wrong src_type! Specify one of the supported: %s" %
              (COLORS.RED, _CORRESP_TABLE.keys()))


if __name__ == '__main__':
    main()
