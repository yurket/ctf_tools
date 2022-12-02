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

CMAKE_TEMPLATE = """cmake_minimum_required(VERSION 3.14)
project({project_name})

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

add_executable({project_name} {cpp_filename})
"""

CLANG_FORMAT = """# https://clang-format-configurator.site/
---
BraceWrapping: {}
ColumnLimit: 100
IndentWidth: 4
AllowShortBlocksOnASingleLine: Never
AllowShortCaseLabelsOnASingleLine: false
AllowShortEnumsOnASingleLine: false
AllowShortFunctionsOnASingleLine: None
AllowShortIfStatementsOnASingleLine: Never
AllowShortLoopsOnASingleLine: false
AlignArrayOfStructures: Left
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


def add_CMakeLists(project_name: str, cpp_filename: str, force_replace: bool):
    cmake_filename = "CMakeLists.txt"
    if not force_replace:
        exit_if_exists(cmake_filename)

    with open(cmake_filename, "wb") as f:
        template = CMAKE_TEMPLATE.format(
            project_name=project_name, cpp_filename=cpp_filename
        ).encode("utf-8")
        f.write(template)


def add_clang_format(force_replace: bool):
    clang_format_filename = ".clang-format"
    if not force_replace:
        exit_if_exists(clang_format_filename)

    with open(clang_format_filename, "wb") as f:
        f.write(CLANG_FORMAT.encode("utf-8"))


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
    parser.add_argument(
        "-cm",
        "--cmake-project-name",
        help="additionally creates CMakeLists.txt with filled in project_name",
    )
    args = parser.parse_args()
    filename = args.filename
    cmake_project_name = args.cmake_project_name
    force_replace = args.force

    if cmake_project_name:
        add_CMakeLists(cmake_project_name, filename, force_replace)
        add_clang_format(force_replace)

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
