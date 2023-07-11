import subprocess as sbp
import unittest

shdr_path = '../../../src/cli/shdroll.py'

"""
Need to automate
"""


class TestShdroll(unittest.TestCase):

    def test_default(self):
        """
        The default works
        :return: None.  Prints text.
        """
        out = sbp.run(['python', shdr_path], stdout=sbp.PIPE, stderr=sbp.STDOUT)
        print(out.stdout.decode())

    def test_print_args(self):
        """
        The default with the input arguments printed to screen
        :return: None.  Prints text.
        """
        out = sbp.run(['python', shdr_path, '--print-args'], stdout=sbp.PIPE, stderr=sbp.STDOUT)
        print(out.stdout.decode())


    def test_base_and_sides(self):
        """
        Start at -10 with a one-sided die.  Output should be -10.
        :return: None.  Prints text.
        """
        out = sbp.run(['python', shdr_path, '--base', '-10', '--sides', '1'], stdout=sbp.PIPE, stderr=sbp.STDOUT)
        print(out.stdout.decode())

    def test_dice(self):
        """
        2d6
        :return: None.  Prints text.
        """
        out = sbp.run(['python', shdr_path, '--dice', '2'], stdout=sbp.PIPE, stderr=sbp.STDOUT)
        print(out.stdout.decode())

    def test_rolls(self):
        """
        1d6 rolled 2x
        :return: None.  Prints text.
        """
        out = sbp.run(['python', shdr_path, '--rolls', '2'], stdout=sbp.PIPE, stderr=sbp.STDOUT)
        print(out.stdout.decode())

    def test_add(self):
        """
        Add 10 to 0. 10, per row 20, grand total 40
        :return: None.  Prints text.
        """
        out = sbp.run(['python', shdr_path, '--base', '0', '--sides', '1',
                       '--dice', '2', '--roll', '2',
                       '--add', '10'], stdout=sbp.PIPE, stderr=sbp.STDOUT)
        print(out.stdout.decode())

    def test_add_total(self):
        """
        Each die 0, +10 to each total = 10.  GT = 20
        :return: None.  Prints text.
        """
        out = sbp.run(['python', shdr_path, '--base', '0', '--sides', '1',
                       '--dice', '2', '--roll', '2',
                       '--add-total', '10'], stdout=sbp.PIPE, stderr=sbp.STDOUT)
        print(out.stdout.decode())

    def test_add_grand_total(self):
        """
        GT = 10
        :return: None.  Prints text.
        """
        out = sbp.run(['python', shdr_path, '--base', '0', '--sides', '1',
                       '--dice', '2', '--roll', '2',
                       '--add-grand-total', '10'], stdout=sbp.PIPE, stderr=sbp.STDOUT)
        print(out.stdout.decode())

    def test_mult(self):
        """
        2 x 2 x 10, T 20, GT 40
        :return: None.  Prints text.
        """
        out = sbp.run(['python', shdr_path, '--base', '1', '--sides', '1',
                       '--dice', '2', '--roll', '2',
                       '--mult', '10'], stdout=sbp.PIPE, stderr=sbp.STDOUT)
        print(out.stdout.decode())

    def test_mult_total(self):
        """
        2 x 10 = 20, x2 = 40
        :return: None.  Prints text.
        """
        out = sbp.run(['python', shdr_path, '--base', '1', '--sides', '1',
                       '--dice', '2', '--roll', '2',
                       '--mult-total', '10'], stdout=sbp.PIPE, stderr=sbp.STDOUT)
        print(out.stdout.decode())

    def test_mult_grand_total(self):
        """
        4 x 10 = 40
        :return: None.  Prints text.
        """
        out = sbp.run(['python', shdr_path, '--base', '1', '--sides', '1',
                       '--dice', '2', '--roll', '2',
                       '--mult-grand-total', '10'], stdout=sbp.PIPE, stderr=sbp.STDOUT)
        print(out.stdout.decode())

    def test_csv(self):
        """
        :return: None.  Saves CSV.
        """
        out = sbp.run(['python', shdr_path,
                       '--dice', '2', '--roll', '2',
                       '--to-csv', 'test.csv'], stdout=sbp.PIPE, stderr=sbp.STDOUT)

    def test_xlsx(self):
        """
        :return: None.  Saves Excel.
        """
        out = sbp.run(['python', shdr_path,
                       '--dice', '2', '--roll', '2',
                       '--to-xlsx', 'test.xlsx'], stdout=sbp.PIPE, stderr=sbp.STDOUT)

    def test_all(self):
        out = sbp.run(['python', shdr_path, '--sides', '6', '--dice', '2', '--rolls', '2'],
                      stdout=sbp.PIPE, stderr=sbp.STDOUT)
        print(out.stdout.decode())

    def test_zero_sides(self):
        """
        Sides must be >= 1
        :return: None.
        """
        self.assertRaises(Exception,
                          sbp.run, ['python', shdr_path, '--sides', '0'],
                          stdout=sbp.PIPE, stderr=sbp.STDOUT, check=True)

    def test_zero_dice(self):
        """
        Dice must be >= 1
        :return: None.
        """
        self.assertRaises(Exception,
                          sbp.run, ['python', shdr_path, '--dice', '0'],
                          stdout=sbp.PIPE, stderr=sbp.STDOUT, check=True)

    def test_zero_rolls(self):
        """
        Rolls must be >= 1
        :return: None.
        """
        self.assertRaises(Exception,
                          sbp.run, ['python', shdr_path, '--rolls', '0'],
                          stdout=sbp.PIPE, stderr=sbp.STDOUT, check=True)
