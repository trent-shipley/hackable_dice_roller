# hackable_dice_roller
from typing import Any, List, Tuple, Callable
from random import normalvariate, randrange, seed
import traceback


def add_currying(x):
    return lambda y: x + y


def multiply_currying(x):
    return lambda y: x * y


class DieRoll:
    def __init__(self,
                 die: Callable[..., float],
                 transform: Callable[[float], float] = None,
                 *die_args):
        self._die = die
        self._transform = transform
        self._die_args = die_args

    def die_roll(self) -> float:
        roll = self._die(*self._die_args)
        if self._transform is not None:
            roll = self._transform(roll)
        return roll


class IntegerDieRoll(DieRoll):
    def __init__(self,
                 transform: Callable[[float], float] = None,
                 sides: int = 6,
                 bottom: int = 1):
        super().__init__(randrange,
                         transform,
                         bottom,
                         bottom + sides,
                         1)
        if sides <= 0:
            raise ValueError("Parameter 'die' must be at least 1")

    def die_roll(self) -> float:
        return int(super().die_roll())


# class RollInstruction:
#     def __init__(self,
#                  number_of_dice: int = 1,
#                  die: int = 6,
#                  bottom: int = 1,
#                  # modifiers: str = None,
#                  times_to_roll: int = 1
#                  ):
#         if times_to_roll < 1:
#             raise ValueError("Parameter 'times_to_roll' the dice must be at least 1")
#         self._number_of_dice = number_of_dice
#         self._die = die
#         self._bottom = bottom
#         # self._modifiers = modifiers
#         self._times_to_roll = times_to_roll
#
#     def dice_roll(number_of_dice: int = 1,
#                   bottom: int = 1,
#                   die: int = 6) -> Tuple[List[int], int]:
#         if number_of_dice < 1:
#             raise ValueError("Parameter 'number_of_dice' to roll must be at l.")
#         rolls = []
#         rolls_with_total = ()
#         for _ in range(number_of_dice):
#             rolls.append(RollInstruction.die_roll(bottom, die))
#         # rolls = [RollInstruction.die_roll(bottom, die) for _ in range(number_of_dice)]
#         # print(type(rolls), rolls)
#         total = sum(rolls)
#         return rolls, total
#
#     def roll_n_times(self) -> List[Tuple[List[int], int]]:
#         return [RollInstruction.dice_roll(number_of_dice=self._number_of_dice,
#                           bottom=self._bottom,
#                           die=self._die) for _ in range(self._times_to_roll)]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    seed(0)

    integer_die_roll = IntegerDieRoll()
    assert integer_die_roll.die_roll() == 4
    assert IntegerDieRoll(sides=100).die_roll() == 98
    assert IntegerDieRoll(bottom=1, sides=2).die_roll() == 2
    assert IntegerDieRoll(bottom=1, sides=1).die_roll() == 1
    assert IntegerDieRoll(transform=add_currying(9),  bottom=1, sides=1).die_roll() == 10
    try:
        print(IntegerDieRoll(bottom=1, sides=0).die_roll())
    except ValueError as v:
        print(v)
        traceback.print_stack()

    # assert RollInstruction.dice_roll() == ([3], 3)
    # assert RollInstruction.dice_roll(die=100) == ([66], 66)
    # assert RollInstruction.dice_roll(number_of_dice=2) == ([4, 4], 8)
    # try:
    #     print(RollInstruction.dice_roll(number_of_dice=0))
    # except ValueError as v:
    #     print(v)
    #     traceback.print_stack()
    # try:
    #     print(RollInstruction.dice_roll(die=0))
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
    # assert RollInstruction(number_of_dice=1, die=6,
    #                        bottom=-10, times_to_roll=1)\
    #            .roll_n_times() == [([-8], -8)]
    # assert RollInstruction(number_of_dice=1, die=6,
    #                        bottom=10, times_to_roll=2)\
    #            .roll_n_times() == [([10], 10),
    #                                ([15], 15)]
    # assert RollInstruction(number_of_dice=1, die=1,
    #                        bottom=0, times_to_roll=1)\
    #            .roll_n_times() == [([0], 0)]
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
