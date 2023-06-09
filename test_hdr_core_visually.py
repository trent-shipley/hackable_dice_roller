# test_hdr_core_visually
import unittest
import hackable_dice_roller as hdr
from numpy.random import binomial


class TestWithVisualVerification(unittest.TestCase):

    def test_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        print("\n'roll' a binomial 'die' with two flips of a coin 30 times")
        for _ in range(30):
            self.binomial_die.die_roll()
            print(self.binomial_die.get_die_value())

    def test_default_integer_die_rolls(self):
        self.integer_die = hdr.IntegerDie()
        print("\nroll a d6 30 times")
        print(self.integer_die.get_die_value())  # auto-populates on creation
        [print(self.integer_die.die_roll()) for _ in range(30)]

    def test_2d_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        self.binomial_dice = hdr.Dice(self.binomial_die, number_of_dice=2)
        print("\nroll 2_binomial, flipping a coin 2 times, 30 times")
        print(self.binomial_dice)  # auto populates
        for _ in range(29):
            self.binomial_dice.dice_roll()
            print(self.binomial_dice)


class TestRolls(unittest.TestCase):

    def test_d6_1x(self):
        die = hdr.IntegerDie()
        one_d6 = hdr.Dice(die)
        roll_x1 = hdr.Rolls(dice=one_d6)
        print("\nroll 1d6 x 1")
        print(roll_x1.roll_n_times())

    def test_2d6_x1(self):
        die = hdr.IntegerDie()
        one_d6 = hdr.Dice(die, number_of_dice=2)
        roll_x1 = hdr.Rolls(dice=one_d6)
        print("\nroll 2d6 x 1")
        print(roll_x1.roll_n_times())

    def test_2d6_x2(self):
        die = hdr.IntegerDie()  # d6
        one_d6 = hdr.Dice(die, number_of_dice=2)  # 2d6
        roll_x2 = hdr.Rolls(dice=one_d6, number_of_rolls=2)  # 2d6*2
        print("\nroll 2d6 x 2")
        print(roll_x2.roll_n_times())
        print(roll_x2.get_headers(with_totals=True))
        print(roll_x2.flatten_rolls(with_totals=True))
        print(roll_x2.rolls_to_pandas(with_totals=False))
        print(roll_x2.rolls_to_pandas(with_totals=True))
        print(roll_x2)


if __name__ == '__main__':
    unittest.main()


