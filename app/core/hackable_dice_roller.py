# hackable_dice_roller.rolls
from typing import Callable
from random import randrange
import numpy as np
import pandas as pd


def add_currying(x: float):
    """
    add_curring supplies one float to which a curried float is added.
    :param x: the provided number to add.
    :return: The results of a currying lambda which accepts a parameter 'y' as the curried value
    """
    return lambda y: x + y


def multiply_currying(x):
    """
    multiply_curring supplies one float with which a curried float is multiplied.
    :param x: the provided number to multiply.
    :return: The results of a currying lambda which accepts a parameter 'y' as the curried value
    """
    return lambda y: x * y


class Die:
    """
    'Die' represents a physical polyhedral die or probability function.
    """
    def __init__(self,
                 die: Callable[..., float],
                 die_name: str = "",
                 transform: Callable[[float], float] = None,
                 *die_args):
        """

        :param die:  A probability function from which hackable dice roller will draw one sample.
        :param die_name: A string naming the parameter 'die'. The empty string is the default.
        :param transform: A function which reserves one curried parameter where the result of a selected sample
            can be placed.  The function must be curried, and since it must be lazily evaluated, it must be a Python
            lambda.  This parameter is empty, or None by default.  'transform' may be removed in a future version
            leaving all data transformation to post-processing.
        :param die_args: positional arguments to the function provided as a parameter to 'die'.
        """
        self.die = die
        self.name = die_name
        self.transform = transform
        self.die_args = die_args

        self.die_value: float = 0

        self.die_roll()  # need in set up to populate all get methods with valid values

    def die_roll(self) -> float:
        """
        :return: returns one sample from 'die' as altered by 'transform'.
        """
        roll = self.die(*self.die_args)
        if self.transform is not None:
            roll = self.transform(roll)
        self.die_value = roll
        return self.die_value

    def get_die_value(self) -> float:
        """Gets the value of a die which was previously rolled."""
        return self.die_value

    def get_die_name(self) -> str:
        return self.name

    def to_string(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.get_die_name()}: {self.get_die_value()}"


class IntegerDie(Die):
    """
    IntegerDie is used to model a polyhedral die, or any other range of integers with an arbitrary starting point.
    It wraps random.randrange().
    """
    def __init__(self,
                 transform: Callable[[float], float] = None,
                 sides: int = 6,
                 bottom: int = 1):
        """
        Used to model one pseudo-random  selection from an arbitrary range of integers.
        :param transform:  A function which reserves one curried parameter where the result of a selected sample
            can be placed.  The function must be curried, and since it must be lazily evaluated, it must be a Python
            lambda.  This parameter is empty, or None by default.  'transform' may be removed in a future version
            leaving all data transformation to post-processing.
        :param sides: The number of sides on the polyhedral die, or more generally the size of the integer range.
            It must be at least 1.
        :param bottom: 'Floor' might have been a better name.  This is the inclusive start of the integer range.
        """
        if sides <= 0:
            raise ValueError("Parameter 'die' must be at least 1")

        super().__init__(randrange,  # the probability function
                         "d" + str(sides),  # name
                         transform,
                         bottom,  # arg0 = start
                         bottom + sides,  # arg1 = stop
                         1)  # arg2 = step = 1

        self.sides = sides
        self.bottom = bottom
             
    def get_bottom(self) -> int:
        """Return the start of random.randrange()."""
        return self.bottom

    def get_sides(self) -> int:
        """Return random.randrange()'s stop"""
        return self.sides


class Dice:
    """
    'Dice' represents one 'throw' of N dice with the same number of sides, or N distinct single samples of the same
    probability function.
    """

    def __init__(self,
                 die: Die,
                 transform_fn: Callable[[float], float] = None,
                 number_of_dice: int = 1):
        """
        'Dice' represents one throw of 'number_of_dice' having the same number of sides or
        the same probability function.
        :param die: an object of class Die in this submodule which models the kind of dice used in this throw.
        :param transform_fn: A function which reserves one curried parameter where the result of a selected sample
            can be placed.  The function must be curried, and since it must be lazily evaluated, it must be a Python
            lambda.  This parameter is empty, or None by default.  'transform' may be removed in a future version
            leaving all data transformation to post-processing.  This transforms the dice throw's total only.
        :param number_of_dice: The number of times to throw the die.  It must be at least 1.
        """
        if number_of_dice < 1:
            raise ValueError("Parameter 'number_of_dice' to roll must be at l.")
        self.die = die
        self.transform_fn = transform_fn
        self.number_of_dice = number_of_dice

        self.rolls: list[float] = []
        self.total: float = 0

        self.dice_roll()  # initializes 'get' methods.

    def dice_roll(self) -> tuple[list[float], float]:
        """
        'dice_roll' emulates a throw of one or more polyhedral dice, or several independent selections from a
        probability function
        :return: 'dice' roll returns a list of rolls or experiments and the sum of the rolls or experiments' results.
        """
        self.clear()
        for _ in range(self.number_of_dice):
            self.rolls.append(self.die.die_roll())

        self.total = sum(self.rolls)
        if self.transform_fn is not None:
            self.total = self.transform_fn(self.total)

        return self.rolls, self.total

    def clear(self) -> type[None]:
        """
        clears the list of rolls and the throw's total so the next throw is tabla rasa.
        :return: None is returned
        """
        self.rolls = []
        self.total = 0

    def get_number_of_dice(self) -> int:
        return self.number_of_dice

    def get_rolls(self) -> list[float]:
        """
        :return: deep copies and returns the list of rolls.
        """
        copy_list = []
        for roll in self.rolls:
            copy_list.append(roll)
        return copy_list

    def get_total(self) -> float:
        """
        :return: Returns the sum of dice or independent experiments in the throw.
        """
        return self.total

    def get_headers(self, with_total: bool = False) -> list[str]:
        """
        Provides standard headers for a dice throw.  This may be useful to provide headers when converting a Dice roll
        to pandas
        :param with_total: includes a header for the throw's total if True.
        :return: A string for use as a  table's header.
        """
        die_name = self.die.get_die_name()
        headers = [die_name + '_' + str(i) for i in range(self.number_of_dice)]
        if with_total:
            total_name = f"{self.number_of_dice}_*_{die_name}_roll_total"
            headers.append(total_name)
        return headers

    def get_rolls_with_total(self) -> list[float]:
        """
        This is a convenience function which appends the calculated total to the list of individual die rolls.
        :return: [rolls].append total.
        """
        data = self.rolls.copy()
        data.append(self.get_total())
        return data

    def dice_to_numpy(self, with_total: bool = False):
        """
        Converts the list from get_rolls_with_total to a numpy array.
        :param with_total: includes the throw's total if True.
        :return: A numpy array.
        """
        to_numpy_list = self.get_rolls()
        if with_total:
            to_numpy_list.append(self.total)
        return np.asarray(to_numpy_list)

    def dice_to_pandas(self, with_total: bool = False):
        """
        Converts the list to a one-row pandas DataFrame
        :param with_total: includes the throw's total if True.
        :return: A one-row pandas DataFrame
        """
        header = self.get_headers(with_total)
        if with_total:
            data = self.get_rolls_with_total()
        else:
            data = self.get_rolls()
        data = [data]  # a list of a list makes pandas think this is a row in a table.
        return pd.DataFrame(data,
                            columns=header,
                            index=None,
                            dtype=float)

    def dice_to_csv(self, path_or_buf=None) -> None:
        """
        Uses pandas to output the dice roll and its total as a csv file.
        :param path_or_buf: Where to save the csv output
        :return: None
        """
        self.dice_to_pandas(with_total=True).to_csv(path_or_buf=path_or_buf)

    def __str__(self) -> str:
        return self.dice_to_pandas(with_total=True).to_string()

    def to_string(self) -> str:
        return self.__str__()


class Rolls:

    def __init__(self,
                 dice: Dice,
                 transform_fn: Callable[[float], float] = None,
                 number_of_rolls: int = 1):
        if number_of_rolls < 1:
            raise ValueError("Parameter 'number_of_rolls' must be at l.")
        self.dice = dice
        self.transform_fn = transform_fn
        self.number_of_rolls = number_of_rolls

        self.list_of_rolls: list[list[float]] = []
        self.list_of_totals: list[float] = []

        self.total: float = 0

        self.roll_n_times()

    def roll_n_times(self) -> tuple[list[list[float]], list[float], float]:
        self.rolls_clear()
        for _ in range(self.number_of_rolls):
            self.dice.dice_roll()
            current_total = self.dice.get_total()
            self.total += current_total
            self.list_of_totals.append(current_total)
            self.list_of_rolls.append(self.dice.get_rolls())

        if self.transform_fn is not None:
            self.total = self.transform_fn(self.total)

        return self.list_of_rolls, self.list_of_totals, self.total

    def rolls_clear(self):
        self.list_of_rolls = []
        self.list_of_totals = []
        self.total = 0

    def get_rolls(self) -> list[list[float]]:
        outer_list = []
        for dice_list in self.list_of_rolls:
            row = []
            for die in dice_list:
                row.append(die)
            outer_list.append(row)
        return outer_list

    def get_list_of_totals(self) -> list[float]:
        dice_totals = []
        for dice_total in self.list_of_totals:
            dice_totals.append(dice_total)
        return dice_totals

    def get_total(self) -> float:
        return self.total

    def get_headers(self, with_totals: bool = False) -> list[str]:
        headers = self.dice.get_headers(with_totals)
        if with_totals:
            headers.append('grand_total')
        return headers

    def flatten_rolls(self, with_totals: bool = False) -> list[list[float]]:
        local_rolls = self.get_rolls()
        if with_totals:
            for i in range(len(local_rolls)):
                local_rolls[i].append(self.list_of_totals[i])
                local_rolls[i].append(self.total)
        return local_rolls

    def rolls_to_numpy(self, with_totals: bool = False):
        return np.asarray(self.flatten_rolls(with_totals))

    def rolls_to_pandas(self, with_totals: bool = False):
        df = pd.DataFrame(data=self.flatten_rolls(with_totals),
                          columns=self.get_headers(with_totals))
        return df

    def rolls_to_csv(self, path_or_buf=None) -> None:
        self.rolls_to_pandas(with_totals=True).to_csv(path_or_buf=path_or_buf)

    def rolls_to_excel(self, excel_writer, sheet_name='Sheet1', float_format=None):
        self.rolls_to_pandas(with_totals=True).to_excel(excel_writer,
                                                        sheet_name=sheet_name,
                                                        float_format=float_format)

    def to_string(self):
        return self.__str__()

    def __str__(self):
        return self.rolls_to_pandas(with_totals=True).to_string()
