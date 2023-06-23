# simple_hdroll_cli_parser
import argparse


class SimpleHDRollCliParser:

    def __init__(self):
        self.parser = argparse.ArgumentParser(add_help=True,
                                              description="Hackable Dice Roller: "
                                                          "A simple Python dice roller for the command line.")

        self.parser.add_argument('--base', '-b', type=int, default='1',
                                 help='Where the dice roll starts, 7, 0, -3, etc. The default in 1.')
        self.parser.add_argument('--sides', '-s', type=int, default='6',
                                 help='The number of sides on the die.  It must be at least 1.  Sides defaults to 6.')
        self.parser.add_argument('--dice', '-d', type=int, default='1',
                                 help="The number of dice to roll at once.  It must be al least 1. Dice defaults to 1")
        self.parser.add_argument('--rolls', '-r', type=int, default='1',
                                 help="The number of times to roll a set of dice. It must be at least 1.  "
                                      "Rolls defaults to 1.")

        self.parser.add_argument('--add', '-a', type=float, default=None,
                                 help="A number to add to each die. Enter a negative number to subtract."
                                      "--add is mutually exclusive with --mult.")
        self.parser.add_argument('--add-total', type=float, default=None,
                                 help="A number to add to the total of a throw of the set of dice. "
                                      "Enter a negative number to subtract."
                                      "--add-total is mutually exclusive with --mult-total")
        self.parser.add_argument('--add-grand-total', type=float, default=None,
                                 help="A number to add to the grand-total of all the rolled dice sets. "
                                      "Enter a negative number to subtract."
                                      "--add-grand-total is mutually exclusive with --mult-grand-total")

        self.parser.add_argument('--mult', '-m', type=float, default=None,
                                 help="A number to multiply with each die.  Enter a decimal less than one to divide."
                                      "--mult is mutually exclusive with --add.")
        self.parser.add_argument('--mult-total', type=float, default=None,
                                 help="A number to multiply with the total of a throw of the set of dice. "
                                      "Enter a decimal less than one to divide."
                                      "--mult-total is mutually exclusive with --add-total.")
        self.parser.add_argument('--mult-grand-total', type=float, default=None,
                                 help="A number to multiply with the grand-total of all the rolled dice sets. "
                                      "Enter decimal less than one to divide."
                                      "--melt-grand-total is mutually exclusive with --add-grand-total")

    def parse(self):
        kwargs = self.parser.parse_args()
        print(kwargs)

        if kwargs.add is not None and kwargs.mult is not None:
            raise SyntaxError("--add and --mult cannot both be used.")
        if kwargs.add_total is not None and kwargs.mult_total is not None:
            raise SyntaxError("--add-total and --mult-total cannot both be used.")
        if kwargs.add_grand_total is not None and kwargs.mult_grand_total is not None:
            raise SyntaxError("--add-grand-total and --mult-grand-total cannot both be used.")

        return kwargs
