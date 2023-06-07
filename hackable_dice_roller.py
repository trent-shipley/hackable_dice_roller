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
        self.die = die
        self.name = die_name
        self.transform = transform
        self.die_args = die_args

        self.die_value: float = 0

        self.die_roll()

    def die_roll(self) -> float:
        roll = self.die(*self.die_args)
        if self.transform is not None:
            roll = self.transform(roll)
        self.die_value = roll
        return self.die_value

    def get_die_value(self) -> float:
        return self.die_value

    def get_die_name(self) -> str:
        return self.name

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
        
        self.sides = sides
        self.bottom = bottom
             
    def get_bottom(self) -> int:
        return self.bottom
    def get_sides(self) -> int:
        return self.sides



class Dice:

    def __init__(self,
                 die: Die,
                 transform_fn: Callable[[float], float] = None,
                 number_of_dice: int = 1):
        if number_of_dice < 1:
            raise ValueError("Parameter 'number_of_dice' to roll must be at l.")
        self.die = die
        self.transform_fn = transform_fn
        self.number_of_dice = number_of_dice

        self.rolls: list[float] = []
        self.total: float = 0

        self.dice_roll()

    def dice_roll(self) -> tuple[list[float], float]:
        self.clear()
        for _ in range(self.number_of_dice):
            self.rolls.append(self.die.die_roll())

        self.total = sum(self.rolls)
        if self.transform_fn is not None:
            self.total = self.transform_fn(self.total)

        return self.rolls, self.total

    def clear(self):
        self.rolls = []
        self.total = 0

    def get_number_of_dice(self):
        return self.number_of_dice

    def get_rolls(self) -> list[float]:
        return self.rolls.copy()

    def get_total(self) -> float:
        return self.total

    def get_headers(self, with_total: bool = False) -> list[str] | None:
        die_name = self.die.get_die_name()
        headers = [die_name + '_' + str(i) for i in range(self.number_of_dice)]
        if with_total:
            total_name = die_name + '_roll_total'
            headers.append(total_name)
        return headers

    def flatten_dice_data(self) -> list[float] | None:
        return self.rolls.append(self.total)

    def dice_to_numpy(self, with_total: bool = False):
        to_numpy_list = self.get_rolls()
        if with_total:
            to_numpy_list.append(self.total)
        return np.asarray(to_numpy_list)

    def dice_to_pands(self, with_total: bool = False):
        header = self.get_headers(with_total)
        data = self.get_rolls()
        if with_total:
            data.append(self.total)
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
        return self.list_of_rolls.copy()

    def get_list_of_totals(self) -> list[float]:
        return self.list_of_totals

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
        return pd.DataFrame(data=self.flatten_rolls(with_totals),
                            columns=self.get_headers(with_totals))

    def rolls_to_csv(self, path_or_buf=None) -> None:
        self.rolls_to_pandas(with_totals=True).to_csv(path_or_buf=path_or_buf)

    def rolls_to_excel(self, excel_writer, float_format=None):
        self.rolls_to_pandas(with_totals=True).to_excel(excel_writer, float_format)

    def __str__(self):
        self.rolls_to_pandas(with_totals=True).to_string()




