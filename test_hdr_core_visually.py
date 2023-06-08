# test_hdr_core_visually
import unittest
import hackable_dice_roller as hdr
from numpy.random import binomial


class TestWithVisualVerification(unittest.TestCase):

    def test_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        for _ in range(30):
            self.binomial_die.die_roll()
            print(self.binomial_die.get_die_value())

    def test_default_integer_die_rolls(self):
        self.integer_die = hdr.IntegerDie()
        print(self.integer_die.get_die_value())  # auto populates on creation
        [print(self.integer_die.die_roll()) for _ in range(30)]

    def test_2d_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        self.binomial_dice = hdr.Dice(self.binomial_die, number_of_dice=2)
        print(self.binomial_dice)  # auto populates
        for _ in range(29):
            self.binomial_dice.dice_roll()
            print(self.binomial_dice)



