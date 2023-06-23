# test_hdr_core
import unittest
from app.core import hackable_dice_roller as hdr
from numpy.random import binomial


class TestBinomialDie(unittest.TestCase):

    def test_binomial(self):
        """
        See if Die will accept numpy.binomial as an arbitrary call-back function
        :return: None.
        """
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        for _ in range(50):
            assert 0 <= self.binomial_die.die_roll() in {0, 1, 2}

    def test_multiply_currying_binomial(self):
        """
        See if a call-back and currying lambda function can be passed to Die.__init__
        :return: None.
        """
        self.binomial_die = hdr.Die(binomial, "binomial * 10", hdr.multiply_currying(10), 2, 0.5)
        for _ in range(50):
            assert self.binomial_die.die_roll() in {0, 10, 20}


class TestIntegerDie(unittest.TestCase):
    """
    The primary use of hackable dice roller is simulating polynomial dice in a simple GUI
    """

    def test_create_and_re_roll(self):
        """
        The default case.  A six-sided die.
        :return: None.
        """
        self.integer_die = hdr.IntegerDie()
        for _ in range(50):
            assert self.integer_die.get_bottom() <= self.integer_die.get_die_value() < \
                   self.integer_die.get_bottom() + self.integer_die.get_sides()

    def test_create_and_str(self):
        """
        To string works as designed ... or not.
        :return: None.
        """
        self.assertRegex(hdr.IntegerDie().to_string(), r"^d6: \d+$")

    def test_name(self):
        """
        Die name works as designed
        :return: None.
        """
        self.integer_die = hdr.IntegerDie()
        self.assertEqual(self.integer_die.get_die_name(), 'd6', "Die name is not 'd6'")

    def test_d100(self):
        """
        Arbitrary sized integer die, d100.
        :return: None.
        """
        self.integer_die = hdr.IntegerDie(sides=100)
        for _ in range(300):
            assert self.integer_die.get_bottom() <= self.integer_die.get_die_value() <\
                   self.integer_die.get_bottom() + self.integer_die.get_sides()

    def test_d2(self):
        """
        Test a d2
        :return: None.
        """
        self.integer_die = hdr.IntegerDie(sides=2)
        for _ in range(30):
            assert self.integer_die.get_bottom() <= self.integer_die.get_die_value() < \
                   self.integer_die.get_bottom() + self.integer_die.get_sides()

    def test_d1(self):
        """
        Start at 1, end at 1, should be one
        :return: None.
        """
        self.integer_die = hdr.IntegerDie(sides=1)
        for _ in range(10):
            assert self.integer_die.get_die_value() == 1

    def test_add_currying(self):
        """
        Check that the IntegerDie subclass can process a curried lambda function.
        :return: None.
        """
        self.integer_die = hdr.IntegerDie(transform_fn=hdr.add_currying(9), sides=1)
        for _ in range(10):
            self.assertEqual(self.integer_die.get_die_value(), 10,
                             f"The addition is wrong: {self.integer_die.get_die_value()}")

    def test_negative_bottom(self):
        """
        Test that an intger die can start at a negative number
        :return: None.
        """
        self.integer_die = hdr.IntegerDie(bottom=-10, sides=6)
        assert self.integer_die.get_bottom() <= self.integer_die.get_die_value() < \
            self.integer_die.get_bottom() + self.integer_die.get_sides()

    def test_zero_bottom_with_d1(self):
        """
        Show an integer die can start at zero.
        :return: None.
        """
        self.integer_die = hdr.IntegerDie(bottom=0, sides=1)
        assert self.integer_die.get_bottom() <= self.integer_die.get_die_value() < \
            self.integer_die.get_bottom() + self.integer_die.get_sides()

    def test_zero_sides(self):
        """
        Show that an IntegerDie must have a positive number of sides.
        :return: None.
        """
        self.assertRaises(ValueError, hdr.IntegerDie, bottom=1, sides=0)


class TestDice(unittest.TestCase):

    def test_1d_binomial(self):
        """
        Throw Dice with an arbitrary call-back function
        :return: None.
        """
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        for _ in range(50):
            assert hdr.Dice(self.binomial_die).get_total() in {0, 1, 2}

    def test_2d_binomial(self):
        """
        Throw Dice with call back function used 2 times
        :return: None.
        """
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        for _ in range(100):
            assert hdr.Dice(self.binomial_die, number_of_dice=2).get_total() in {0, 1, 2, 3, 4}

    def test_1d_binomial_with_transform(self):
        """
        Roll an arbitrary callback function and transform the total with a curried lambda function.
        :return: None.
        """
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        for _ in range(50):
            assert hdr.Dice(self.binomial_die, transform_fn=hdr.add_currying(-10)).get_total() in {-10, -9, -8}

    def test_must_have_at_least_1_die(self):
        """
        Demonstrate you must have a positive number of Dice.
        :return: None.
        """
        self.assertRaises(ValueError, hdr.Dice, die=hdr.IntegerDie(), number_of_dice=0)


class TestRolls(unittest.TestCase):

    def test_1d1_transformed(self):
        """
        Demonstrate the transformation of the grand total of all the Rolls with a curried lambda function.
        :return: None.
        """
        die = hdr.IntegerDie(sides=1)  # d6
        one_d1 = hdr.Dice(die, number_of_dice=1)  # 2d60
        self.assertEqual(10,
                         hdr.Rolls(dice=one_d1, transform_fn=hdr.add_currying(9)).get_total(),
                         "transformation of Rolls did not work.")  # 1d1*1 + 10

    def test_number_of_rolls_is_0(self):
        """
        Demonstrate you need to make a positive number of Rolls.
        :return: None.
        """
        die = hdr.IntegerDie()  # d6
        one_d6 = hdr.Dice(die, number_of_dice=2)  # 2d6
        self.assertRaises(ValueError, hdr.Rolls, dice=one_d6, number_of_rolls=0)


if __name__ == '__main__':
    unittest.main()
