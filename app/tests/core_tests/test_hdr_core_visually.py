# test_hdr_core_visually
import unittest
from app.core import hackable_dice_roller as hdr
from numpy.random import binomial
from os.path import dirname


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

    def test_2d6_to_numpy(self):
        print(hdr.Dice(die=hdr.IntegerDie(), number_of_dice=2).dice_to_numpy())

    def test_2d_binomial(self):
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        self.binomial_dice = hdr.Dice(self.binomial_die, number_of_dice=2)
        print("\nroll 2_binomial, flipping a coin 2 times, 30 times")
        print(self.binomial_dice)  # auto populates
        for _ in range(29):
            self.binomial_dice.dice_roll()
            print(self.binomial_dice)

    def test_2d_binomial_to_csv(self):
        dice_test_csv = dirname(__file__) + '/' + 'dice_test.csv'
        print(dice_test_csv)
        self.binomial_die = hdr.Die(binomial, "binomial", None, 2, 0.5)
        hdr.Dice(self.binomial_die, number_of_dice=2).dice_to_csv(dice_test_csv)


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
        print(roll_x2.get_rolls_with_totals(with_totals=True))
        print(roll_x2.rolls_to_pandas(with_totals=False))
        print(roll_x2.rolls_to_pandas(with_totals=True))
        print(roll_x2)

    def test_2d6_x2_to_numpy(self):
        die = hdr.IntegerDie()  # d6
        one_d6 = hdr.Dice(die, number_of_dice=2)  # 2d6
        roll_x2 = hdr.Rolls(dice=one_d6, number_of_rolls=2)  # 2d6*2
        print(roll_x2.rolls_to_numpy())

    def test_2d6_x2_to_csv(self):
        rolls_test_csv = dirname(__file__) + '/' + 'rolls_test.csv'
        print(rolls_test_csv)
        die = hdr.IntegerDie()  # d6
        one_d6 = hdr.Dice(die, number_of_dice=2)  # 2d6
        roll_x2 = hdr.Rolls(dice=one_d6, number_of_rolls=2)  # 2d6*2
        roll_x2.rolls_to_csv(rolls_test_csv)

    def test_2d6_x2_to_xlsx(self):
        rolls_test_xlsx = dirname(__file__) + '/' + 'rolls_test.xlsx'
        print(rolls_test_xlsx)
        die = hdr.IntegerDie()  # d6
        one_d6 = hdr.Dice(die, number_of_dice=2)  # 2d6
        roll_x2 = hdr.Rolls(dice=one_d6, number_of_rolls=2)  # 2d6*2
        roll_x2.rolls_to_excel(rolls_test_xlsx)



if __name__ == '__main__':
    unittest.main()


