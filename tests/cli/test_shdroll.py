import sys
sys.path.extend(['../..',
                 '../../src',
                 '../../src/cli'])
import unittest
from src.cli import shdroll as shdr
import subprocess as sbp

shdr_path = '../../src/cli/shdroll.py'

out, err = sbp.run('python', shdr_path,
                   # stdout=sbp.PIPE,
                   # stderr=sbp.PIPE
                   )
print(out, err)


