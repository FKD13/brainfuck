#!/usr/bin/env python
# -*- coding: utf-8 -*-
import interpreter
import sys

print(sys.argv)
if len(sys.argv) == 3 and sys.argv[1] in ['-f', '-b']:
    if sys.argv[1] == '-f':
        with open(sys.argv[2], 'r') as f:
            strings = ''
            for line in f:
                strings += line.strip()
            interpreter.Interpreter(strings).interpret()
    else:
        interpreter.Interpreter(sys.argv[2]).interpret()
else:
    print('Usage: [-f file] [-b brainfuck]')
    exit(1)