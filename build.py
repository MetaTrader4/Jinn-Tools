#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CODE IS POETRY
# TRADING IS MARTIAL ART
# Kolier.Li <kolier.li@gmail.com> [http://kolier.li]

# Build the Genie Project

# Usage
# build.py <lib> <dep1,dep2,dep3>

from os import listdir
from os import walk
import sys

lib = sys.argv[1]
deps = []
if len(sys.argv) > 2:
    deps = sys.argv[2].strip().split(',')

# Header Block
header = """// CODE IS POETRY
// TRADING IS MARTIAL ART
// Kolier.Li <kolier.li@gmail.com> [http://kolier.li]

// Things in Your Dreams that Pop Up When You Wish For it
"""

# ======================================
# Functions
# ======================================

# Dependencies
def depends(deps):
    if len(sys.argv) <= 2:
        return ''
    info = separator('dependencies')
    for dep in deps:
        info += '#include "../' + dep + '/' + dep + '.mqh' + '"\n'
    return info

# Function to Build Package Title
def separator(name):
    return """
// =====================================
// {0}
// =====================================

""".format(name.title())

# Function to Print Each Module in Package
# @todo Handle empty file
def package_info(package, modules):
    info = ''
    for module in modules:
        status = test_status(package, module)
        if len(status) == 0:
            info += '#include "' + module_path(package, module) + '"\n'
        else:
            info += '//' + status + ' #include "' + module_path(package, module) + '"\n'
    return info

def module_path(package, module):
    return package + '/' + module

def test_status(package, module):
    file = open(lib + '/' + module_path(package, module), "r")
    i = 0
    for line in file:
        i += 1
        if i > 20:
            return ''
        if '@module-notready' in line:
            return '@module-notready'
        if '@module-deprecated' in line:
            return '@module-deprecated'
    return ''

def write_deps():
    output = header
    output += depends(deps)
    f = open(lib + '/' + 'lib.mqh', 'w')
    print(output.strip(), file=f)
    
    
def write_lib():
    output = header
    #
    packages = []
    for (dirpath, dirnames, filenames) in walk(lib):
        packages.extend(dirnames)
        packages.remove('.git')
        break
    for package in packages:
        modules = []
        for (dirpath, dirnames, filenames) in walk(lib +'/' + package):
            modules.extend(filenames)
            break
        output += separator(package)
        output += package_info(package, modules)
    #
    f = open(lib + '/' + lib + '.mqh', 'w')
    print(output.strip(), file=f)
    
# ======================================
# Runtime
# ======================================

write_deps()

write_lib()
