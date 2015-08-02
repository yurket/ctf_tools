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

using std::cout;
using std::endl;

int main()
{
    cout << "cpp template" << endl;
    return 0;
}

"""

_EXT_TO_TEMPLATE = {
    '.py'   : PYTHON_TEMPLATE
    , '.c'  : C_TEMPLATE

    , '.cpp': CPP_TEMPLATE
    , '.cc' : CPP_TEMPLATE
    , '.cxx': CPP_TEMPLATE
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

#TODO: Add simple makefiles for c, cpp templates
#TODO: print_colored_error() or @colored

def main():
    DESCR = 'Program creates ready-to-use source file templates for some' \
            'popular programming languages.'
    parser = argparse.ArgumentParser(description=DESCR)
    parser.add_argument('filename', type=str, help='filelame of new source file with correct extension')
    parser.add_argument('-f', '--force', action='store_true',
                        help='replace existing file')
    args = parser.parse_args()
    filename = args.filename
    force_replace = args.force

    name, ext = os.path.splitext(filename)
    if not ext:
        print("%sError: Wrong extension! Specify one of the supported: %s" %
              (COLORS.RED, _EXT_TO_TEMPLATE.keys()))
        return

    if os.path.exists(filename) and not force_replace:
        print("[!] File %s exists! Specify -f, --force option to replace it!"
              % filename)
        return

    with open(filename, 'wb') as f:
        f.write(_EXT_TO_TEMPLATE[ext])

    # make python sources executable
    if ext == '.py':
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC)


if __name__ == '__main__':
    main()
