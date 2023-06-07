# hackable_dice_roller.rolls
from __future__ import annotations
from typing import Callable
from random import normalvariate, randrange, seed
import traceback
import numpy as np
import pandas as pd


def add_currying(x):
    return lambda y: x + y


def multiply_currying(x):
    return lambda y: x * y


class Die:
    def __init__(self,
                 die: Callable[..., float],
                 die_name: str = "",
                 transform: Callable[[float], float] = None,
                 *die_args):
        self._die = die
        self._name = die_name
        self._transform = transform
        self._die_args = die_args

        self._die_value: float = 0

        self.die_roll()

    def die_roll(self) -> float:
        roll = self._die(*self._die_args)
        if self._transform is not None:
            roll = self._transform(roll)
        self._die_value = roll
        return self._die_value

    def get_die_value(self) -> float:
        return self._die_value

    def get_die_name(self) -> str:
        return self._name

    def __str__(self):
        return f"{self.get_die_name()}: {self.get_die_value()} "


class IntegerDie(Die):
    def __init__(self,
                 transform: Callable[[float], float] = None,
                 sides: int = 6,
                 bottom: int = 1):
        if sides <= 0:
            raise ValueError("Parameter 'die' must be at least 1")

        super().__init__(randrange,
                         "d" + str(sides),
                         transform,
                         bottom,
                         bottom + sides,
                         1)

    #     self._die_roll()
    #
    # def _die_roll(self) -> float:
    #     return super()


class Dice:

    def __init__(self,
                 die: Die,
                 transform_fn: Callable[[float], float] = None,
                 number_of_dice: int = 1):
        if number_of_dice < 1:
            raise ValueError("Parameter 'number_of_dice' to roll must be at l.")
        self._die = die
        self._transform_fn = transform_fn
        self._number_of_dice = number_of_dice

        self._rolls: list[float] = []
        self._total: float = 0

        self.dice_roll()

    def dice_roll(self) -> tuple[list[float], float]:
        self.clear()
        for _ in range(self._number_of_dice):
            self._rolls.append(self._die.die_roll())

        self._total = sum(self._rolls)
        if self._transform_fn is not None:
            self._total = self._transform_fn(self._total)

        return self._rolls, self._total

    def clear(self):
        self._rolls = []
        self._total = 0

    def get_number_of_dice(self):
        return self._number_of_dice

    def get_rolls(self) -> list[float]:
        return self._rolls.copy()

    def get_total(self) -> float:
        return self._total

    def get_headers(self, with_total: bool = False) -> list[str] | None:
        die_name = self._die.get_die_name()
        headers = [die_name + '_' + str(i) for i in range(self._number_of_dice)]
        if with_total:
            total_name = die_name + '_roll_total'
            headers.append(total_name)
        return headers

    def flatten_dice_data(self) -> list[float] | None:
        return self._rolls.append(self._total)

    def dice_to_numpy(self, with_total: bool = False):
        to_numpy_list = self.get_rolls()
        if with_total:
            to_numpy_list.append(self._total)
        return np.asarray(to_numpy_list)

    def dice_to_pands(self, with_total: bool = False):
        header = self.get_headers(with_total)
        data = self.get_rolls()
        if with_total:
            data.append(self._total)
        return pd.DataFrame(data, columns=header, dtype=float)

    def __str__(self):
        self.dice_to_pands(with_total=True).to_string()


class Rolls:

    def __int__(self,
                dice: Dice,
                transform_fn: Callable[[float], float] = None,
                number_of_rolls: int = 1):
        if number_of_rolls < 1:
            raise ValueError("Parameter 'number_of_rolls' must be at l.")
        self._dice = dice
        self._transform_fn = transform_fn
        self._number_of_rolls = number_of_rolls

        self._list_of_rolls: list[list[float]] = []
        self._list_of_totals: list[float] = []

        self._total: float = 0

        self.roll_n_times()

    def roll_n_times(self) -> tuple[list[list[float]], list[float], float]:
        self.rolls_clear()
        for _ in range(self._number_of_rolls):
            self._dice.dice_roll()
            current_total = self._dice.get_total()
            self._total += current_total
            self._list_of_totals.append(current_total)
            self._list_of_rolls.append(self._dice.get_rolls())

        if self._transform_fn is not None:
            self._total = self._transform_fn(self._total)

        return self._list_of_rolls, self._list_of_totals, self._total

    def rolls_clear(self):
        self._list_of_rolls = []
        self._list_of_totals = []
        self._total = 0

    def get_rolls(self) -> list[list[float]]:
        return self._list_of_rolls.copy()

    def get_list_of_totals(self) -> list[float]:
        return self._list_of_totals

    def get_total(self) -> float:
        return self._total

    def get_headers(self, with_totals: bool = False) -> list[str]:
        headers = self._dice.get_headers(with_totals)
        if with_totals:
            headers.append('grand_total')
        return headers

    def flatten_rolls(self, with_totals: bool = False) -> list[list[float]]:
        local_rolls = self.get_rolls()
        if with_totals:
            for i in range(len(local_rolls)):
                local_rolls[i].append(self._list_of_totals[i])
                local_rolls[i].append(self._total)
        return local_rolls

    def rolls_to_numpy(self, with_totals: bool = False):
        return np.asarray(self.flatten_rolls(with_totals))

    def rolls_to_pandas(self, with_totals: bool = False):
        return pd.DataFrame(data=self.flatten_rolls(with_totals),
                            columns=self.get_headers(with_totals))

    def rolls_to_csv(self, path_or_buf=None) -> None:
        self.rolls_to_pandas(with_totals=True).to_csv(path_or_buf=path_or_buf)

    def rolls_to_excel(self, excel_writer, float_format=None):
        self.rolls_to_pandas(with_totals=True).to_excel(excel_writer, float_format)

    def __str__(self):
        self.rolls_to_pandas(with_totals=True).to_string()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    seed(0)

    integer_die = IntegerDie()
    print(integer_die)
    print(integer_die.die_roll())
    print(integer_die.die_roll())
    print(integer_die.die_roll())
    print(integer_die.die_roll())
    print(IntegerDie(sides=100))
    print(IntegerDie(bottom=1, sides=2))
    print(IntegerDie(bottom=1, sides=1))
    # assert IntegerDie(transform=add_currying(9),  bottom=1, sides=1).die_roll() == (1, 10)
    # assert IntegerDie(bottom=-10, sides=6).die_roll() == (-6, -6)
    # assert IntegerDie(bottom=11, sides=6).die_roll() == (14, 14)
    # assert IntegerDie(bottom=0, sides=1).die_roll() == (0, 0)
    # try:
    #     print(IntegerDie(bottom=1, sides=0).die_roll())
    # except ValueError as v:
    #     print(v)
    #     traceback.print_stack()
    #
    # [print(integer_die.die_roll()) for _ in range(6)]
    #
    # normal_die = Die(normalvariate)
    # print(normal_die.die_roll())
    # normal_die = Die(normalvariate, "normalvariate*20", multiply_currying(20), 0, 1)
    # print(normal_die.die_roll())
    #
    # dice = Dice(IntegerDie(), None, 2)
    # [print(dice.dice_roll()) for _ in range(6)]
    #
    # normal_die = Die(normalvariate, "normalvariate", None, 0, 1)
    # dice = Dice(die=normal_die, number_of_dice=2)
    # [print(dice.dice_roll()) for _ in range(6)]
    #
    # Dice(IntegerDie(sides=100), number_of_dice=1).dice_roll()
    # try:
    #     print(Dice(IntegerDie(), number_of_dice=0).dice_roll())
    # except ValueError as v:
    #     print(v)
    #     traceback.print_stack()

    #
    # assert RollInstruction().roll_n_times() == [([3], 3)]
    # assert RollInstruction(times_to_roll=2).roll_n_times() == \
    #        [([4], 4),
    #         ([3], 3)]
    # assert RollInstruction(number_of_dice=2,
    #                        times_to_roll=4)\
    #            .roll_n_times() == [([5, 2], 7),
    #                                ([5, 2], 7),
    #                                ([3, 2], 5),
    #                                ([1, 5], 6)]
    # assert RollInstruction(number_of_dice=1, die=100,
    #                        bottom=1, times_to_roll=1)\
    #            .roll_n_times() == [([33], 33)]
    # assert RollInstruction(number_of_dice=2, die=100,
    #                        bottom=1, times_to_roll=2)\
    #            .roll_n_times() == [([69, 91], 160),
    #                                ([78, 19], 97)]
    # try:
    #     print(RollInstruction(number_of_dice=1, die=6,
    #                           bottom=1, times_to_roll=0)\
    #           .roll_n_times())
    # except ValueError as v:
    #     print(v)
    #     traceback.print_stack()
    # try:
    #     print(RollInstruction(number_of_dice=0, die=6,
    #                           bottom=1, times_to_roll=1)\
    #           .roll_n_times())
    # except ValueError as v:
    #     print(v)
    #     traceback.print_stack()
    # try:
    #     print(RollInstruction(number_of_dice=1, die=0,
    #                           bottom=1, times_to_roll=1)\
    #           .roll_n_times())
    # except ValueError as v:
    #     print(v)
    #     traceback.print_stack()
