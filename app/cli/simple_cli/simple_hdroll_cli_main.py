import simple_hdroll_cli_parser as shdroll_cli
import app.core.hackable_dice_roller as cli_hdroll

parse_cli_args = shdroll_cli.SimpleHDRollCliParser()
kwargs = parse_cli_args.parse()

if kwargs.add is not None:
    transform = cli_hdroll.add_currying(kwargs.add)
elif kwargs.mult is not None:
    transform = cli_hdroll.multiply_currying(kwargs.mult)
else:
    transform = None

die = cli_hdroll.IntegerDie(transform_fn=transform,
                            sides=kwargs.sides,
                            bottom=kwargs.base)

if kwargs.add_total is not None:
    transform = cli_hdroll.add_currying(kwargs.add_total)
elif kwargs.mult_total is not None:
    transform = cli_hdroll.multiply_currying(kwargs.mult_total)
else:
    transform = None

dice = cli_hdroll.Dice(die,
                       transform_fn=transform,
                       number_of_dice=kwargs.dice)

if kwargs.add_grand_total is not None:
    transform = cli_hdroll.add_currying(kwargs.add_grand_total)
elif kwargs.mult_grand_total is not None:
    transform = cli_hdroll.multiply_currying(kwargs.mult_grand_total)
else:
    transform = None

rolls = cli_hdroll.Rolls(dice,
                         transform_fn=transform,
                         number_of_rolls=kwargs.rolls)

print(rolls.to_string())