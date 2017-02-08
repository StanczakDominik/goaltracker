import numpy as np

from Goal import Goal


def test_period():
    initial_daily = 20
    initial_daily_increase = 1
    for period in range(1, 5):
        g = Goal("test", "", period, initial_daily, initial_daily_increase)
        times = np.arange(5)
        # print(period)
        # print(times)
        # print(g.poly_values(times))
        test1 = g.poly_diffs(times)
        expected_derivatives = (initial_daily + times * initial_daily_increase / period) / period
        assert np.isclose(expected_derivatives, test1).all()


if __name__ == '__main__':
    test_period()
