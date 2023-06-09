# test_hdr_core
import unittest
import hackable_dice_roller as hdr
from numpy.random import binomial


class TestBinomial(unittest.TestCase):

    def test_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        assert 0 <= self.binomial_die.die_roll() <= 2

    def test_multiply_currying_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial * 10", hdr.multiply_currying(10), 2, 0.5)
        assert self.binomial_die.die_roll() in [0, 10, 20]


class TestIntegerDie(unittest.TestCase):

    def test_create_and_re_roll(self):
        self.integer_die = hdr.IntegerDie()
        assert self.integer_die.get_bottom() <=  self.integer_die.get_die_value() <= self.integer_die.get_sides()

    def test_name(self):
        self.integer_die = hdr.IntegerDie()
        self.assertEqual(self.integer_die.get_die_name(), 'd6', "Die name is not 'd6'")

    def test_d100(self):
        self.integer_die = hdr.IntegerDie(sides=100)
        assert self.integer_die.get_bottom() <=  self.integer_die.get_die_value() <= self.integer_die.get_sides()

    def test_d2(self):
        self.integer_die = hdr.IntegerDie(sides=2)
        assert self.integer_die.get_bottom() <= self.integer_die.get_die_value() <= self.integer_die.get_sides()

    def test_d1(self):
        self.integer_die = hdr.IntegerDie(sides=1)
        assert self.integer_die.get_bottom() <= self.integer_die.get_die_value() <= self.integer_die.get_sides()

    def test_add_currying(self):
        self.integer_die = hdr.IntegerDie(transform=hdr.add_currying(9), sides=1)
        self.assertEqual(self.integer_die.get_die_value(), 10,
                          f"The addition is wrong: {self.integer_die.get_die_value()}")

    def test_negative_bottom(self):
        self.integer_die = hdr.IntegerDie(bottom=-10, sides=6)
        assert self.integer_die.get_bottom() <= self.integer_die.get_die_value() <= \
            self.integer_die.get_bottom() + self.integer_die.get_sides() - 1

    def test_zero_bottom_with_d1(self):
        self.integer_die = hdr.IntegerDie(bottom=0, sides=1)
        assert self.integer_die.get_bottom() <= self.integer_die.get_die_value() <= \
            self.integer_die.get_bottom() + self.integer_die.get_sides() - 1

    def test_zero_sides(self):
        self.assertRaises(ValueError, hdr.IntegerDie, bottom=1, sides=0)



class TestDice(unittest.TestCase):


    def test_1d_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        assert hdr.Dice(self.binomial_die).get_total() in {0, 1, 2}

    def test_2d_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        assert hdr.Dice(self.binomial_die, number_of_dice=2).get_total() in {0, 1, 2, 3, 4}

    def test_1d_binomial_with_transform(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        assert hdr.Dice(self.binomial_die, transform_fn=hdr.add_currying(-10)).get_total() in {-10, -9, -8}

    def test_must_have_at_least_1_die(self):
        self.assertRaises(ValueError, hdr.Dice, die=hdr.IntegerDie(), number_of_dice=0)


class TestRolls(unittest.TestCase):

    def test_1d1_transformed(self):
        die = hdr.IntegerDie(sides=1)  # d6
        one_d1 = hdr.Dice(die, number_of_dice=1)  # 2d60
        self.assertEqual(10,
                         hdr.Rolls(dice=one_d1, transform_fn=hdr.add_currying(9)).get_total(),
                         "transformation of Rolls did not work.")  # 1d1*1 + 10

    def test_number_of_rolls_is_0(self):
        die = hdr.IntegerDie()  # d6
        one_d6 = hdr.Dice(die, number_of_dice=2)  # 2d6
        self.assertRaises(ValueError, hdr.Rolls, dice=one_d6, number_of_rolls=0)


if __name__ == '__main__':
    unittest.main()
