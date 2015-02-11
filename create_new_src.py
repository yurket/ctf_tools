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

class COLORS:
    NOCOLOR = '\033[0m'
    RED = '\033[91m'


def main():
    DESCR = 'program creates ready-to-use template for average python script.'
    parser = argparse.ArgumentParser(description=DESCR)
    parser.add_argument('src_type', type=str, help='source file type [python, c]')
    parser.add_argument('filename', type=str, help='filelame of new source file')
    args = parser.parse_args()

    filename = args.filename
    src_type = args.src_type.lower()
    if src_type == 'python':
        name, ext = os.path.splitext(filename)
        if not ext:
            filename += '.py'
        with open(filename, 'wb') as f:
            f.write(PYTHON_TEMPLATE)
    elif src_type == 'c':
        name, ext = os.path.splitext(filename)
        if not ext:
            filename += '.cc'
        with open(filename, 'wb') as f:
            f.write(C_TEMPLATE)
    else:
        print("Error: Wrong %ssrc_type%s! Specify one of the supported: 'c' or 'python'" %
              (COLORS.RED, COLORS.NOCOLOR))


if __name__ == '__main__':
    main()
