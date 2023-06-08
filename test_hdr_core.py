# test_hdr_core
import unittest
import hackable_dice_roller as hdr
from numpy.random import binomial


class TestBinomial(unittest.TestCase):

    def test_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        print(self.binomial_die.get_die_value())
        assert 0 <= self.binomial_die.die_roll() <= 2

    def test_multiply_currying_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial * 10", hdr.multiply_currying(10), 2, 0.5)
        print(self.binomial_die.get_die_value())
        assert self.binomial_die.die_roll() in [0, 10, 20]


class TestIntegerDie(unittest.TestCase):

    def test_create_and_re_roll(self):
        self.integer_die = hdr.IntegerDie()
        assert self.integer_die.get_bottom() <=  self.integer_die.get_die_value() <= self.integer_die.get_sides()

    def test_name(self):
        self.integer_die = hdr.IntegerDie()
        self.assertEqual(self.integer_die.get_die_name(), 'd6', "Die name is not 'd6'")

    def test_multiples_default_rolls(self):
        self.integer_die = hdr.IntegerDie()
        [print(self.integer_die.die_roll()) for _ in range(6)]

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



class TestBinomialDice(unittest.TestCase):


    def test_1d_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        assert hdr.Dice(self.binomial_die).get_total() in {0, 1, 2}

    def test_2d_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        assert hdr.Dice(self.binomial_die, number_of_dice=2).get_total() in {0, 1, 2, 3, 4}

    def test_1d_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        assert hdr.Dice(self.binomial_die, transform_fn=hdr.add_currying(-10)).get_total() in {-10, -9, -8}

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

if __name__ == '__main__':
    unittest.main()