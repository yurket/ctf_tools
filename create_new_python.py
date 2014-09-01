#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import os
import sys


TEMPLATE = \
u"""#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function



def main():
    pass


if __name__ == '__main__':
    main()

"""

def main():
    DESCR = 'program creates ready-to-use template for average python script.'
    parser = argparse.ArgumentParser(description=DESCR)
    parser.add_argument('filename', type=str, help='filelame of new python source file')
    args = parser.parse_args()

    filename = args.filename
    name, ext = os.path.splitext(filename)
    if not ext:
        filename += '.py'
    with open(filename, 'wb') as f:
        f.write(TEMPLATE)


if __name__ == '__main__':
    main()
