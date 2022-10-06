#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import stat


PYTHON_TEMPLATE = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
import unittest

class MyTest(unittest.TestCase):
    def test_first(self):
        self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()

"""

RUBY_TEMPLATE = """#!/usr/bin/env ruby


def main()
    puts "ruby template"
    return 0
end


if __FILE__ == $PROGRAM_NAME
  exit main()
end

"""

C_TEMPLATE = """#include <stdio.h>
#include <string.h>

#include <errno.h>
#include <sys/types.h>
#include <unistd.h>


int main()
{

    return 0;
}

"""

CPP_TEMPLATE = """#include <iostream>
#include <string>

int main()
{
    std::cout << "cpp template" << std::endl;
    return 0;
}

"""

BASH_TEMPLATE = """#!/bin/bash

echo template
"""

CMAKE_TEMPLATE = """cmake_minimum_required(VERSION 3.10)
project({project_name})

add_executable({project_name} {project_name}.cpp)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
"""


_EXT_TO_TEMPLATE = {
    ".py": PYTHON_TEMPLATE,
    ".rb": RUBY_TEMPLATE,
    ".c": C_TEMPLATE,
    ".cpp": CPP_TEMPLATE,
    ".cc": CPP_TEMPLATE,
    ".cxx": CPP_TEMPLATE,
    ".sh": BASH_TEMPLATE,
}


class COLORS:
    """
    Uses color-set escape sequences:
    start coloring: \[\e[color\], end coloring: \[\e[m\].
    """

    NOCOLOR = "\033[0m"
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"


# TODO: print_colored_error() or @colored


def exit_if_exists(filename: str):
    if os.path.exists(filename):
        print(
            "%s[!] File %s exists! Specify -f, --force option to replace it!%s"
            % (COLORS.YELLOW, filename, COLORS.NOCOLOR)
        )
        exit(1)


def create_cmake_project(project_name: str, force_replace: bool):
    cmake_filename = "CMakeLists.txt"
    cpp_filename = project_name + ".cpp"
    if not force_replace:
        exit_if_exists(cmake_filename)
        exit_if_exists(cpp_filename)

    with open(cmake_filename, "wb") as f:
        template = CMAKE_TEMPLATE.format(project_name=project_name).encode("utf-8")
        f.write(template)

    with open(cpp_filename, "wb") as f:
        template = CPP_TEMPLATE.encode("utf-8")
        f.write(template)


def main():
    DESCR = (
        "Program creates ready-to-use source file templates for some"
        "popular programming languages."
    )
    parser = argparse.ArgumentParser(description=DESCR)
    parser.add_argument(
        "filename", type=str, help="filelame of new source file with correct extension"
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="replace existing file"
    )
    parser.add_argument("--project-name", help="project name for CMakeLists.txt")
    args = parser.parse_args()
    filename = args.filename
    project_name = args.project_name if args.project_name else "template"
    force_replace = args.force

    if filename == "CMakeLists.txt":
        create_cmake_project(project_name, force_replace)
        return

    _, ext = os.path.splitext(filename)
    if not ext or ext not in _EXT_TO_TEMPLATE.keys():
        print(
            "%sError: Wrong extension! Specify one of the supported: %s %s"
            % (COLORS.RED, _EXT_TO_TEMPLATE.keys(), COLORS.NOCOLOR)
        )
        return

    if not force_replace:
        exit_if_exists(filename)

    with open(filename, "wb") as f:
        template = _EXT_TO_TEMPLATE[ext].encode("utf-8")
        f.write(template)

    # make python sources executable
    executable_scripts_extentions = [".py", ".sh", ".rb"]
    if ext in executable_scripts_extentions:
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC)


if __name__ == "__main__":
    main()
