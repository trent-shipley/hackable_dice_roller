# shdroll.py
# shdroll stands for simple hackable dice rol
import sys
sys.path.extend(['../..',
                 '../../src'
                 '../../src/core'])
from shdroll_cli_parser import SimpleHDRollCliParser
from src.core import core

parse_cli_args = SimpleHDRollCliParser()
kwargs = parse_cli_args.parse()

if kwargs.add is not None:
    transform = core.add_currying(kwargs.add)
elif kwargs.mult is not None:
    transform = core.multiply_currying(kwargs.mult)
else:
    transform = None

# Create a die
die = core.IntegerDie(transform_fn=transform,
                      sides=kwargs.sides,
                      bottom=kwargs.base)

if kwargs.add_total is not None:
    transform = core.add_currying(kwargs.add_total)
elif kwargs.mult_total is not None:
    transform = core.multiply_currying(kwargs.mult_total)
else:
    transform = None

# create N dice to throw
dice = core.Dice(die,
                 transform_fn=transform,
                 number_of_dice=kwargs.dice)

if kwargs.add_grand_total is not None:
    transform = core.add_currying(kwargs.add_grand_total)
elif kwargs.mult_grand_total is not None:
    transform = core.multiply_currying(kwargs.mult_grand_total)
else:
    transform = None

# Throw the set of dice N-times.
rolls = core.Rolls(dice,
                   transform_fn=transform,
                   number_of_rolls=kwargs.rolls)

if kwargs.print_args: print(kwargs)
print(rolls.to_string())