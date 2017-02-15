import datetime
import os
import textwrap

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from config import conf_path


def polynomial_coefficients(period, additional):
    polynomial_derivatives = np.array([0] + list(additional))
    polynomial_denominators = np.arange(polynomial_derivatives.size)
    polynomial_denominators[0] = 1
    return polynomial_derivatives / (polynomial_denominators * period ** polynomial_denominators)


class Goal:
    """Class representing a goal you want to pursue.

    Goal("pushups", "20 pushups first thing in morning", 1, 20, 1)
    shortname - short, no spaces, name for goal
    description - more verbose description
    period - per how many days...
    count - how many you want to do
    additional - factors for additional terms in polynomial
    """

    current_date = datetime.datetime.today()
    tomorrow_date = current_date + datetime.timedelta(days=1)
    tomorrow_plotting_date = tomorrow_date + datetime.timedelta(days=1)

    def __init__(self, shortname, description, startdate, period, *derivatives):
        """

        :param str shortname: unique ID name
        :param str description: A longer description of the goal.
        :param period: how often do you want to do this?
        :param derivatives: how many units you want to add to each derivative each period.
            20, 1: start with 20 units periodically, increase by 1 each period.
            20, 1, 1: start with 20 units periodically, increase by 1+which_period each period.
        """
        self.shortname = shortname
        self.description = description
        self.startdate = datetime.datetime.strptime(startdate, "%Y-%m-%d")
        self.period = period
        self.count = derivatives[0]
        self.leeway = 3 * self.count / self.period
        self.polynomial_coefficients = polynomial_coefficients(self.period, derivatives)
        self.polynomial = np.poly1d(self.polynomial_coefficients[::-1], variable="t")
        self.factors = np.array(derivatives)
        self.filepath = conf_path + self.shortname + ".csv"
        # TODO: make sure file path exists
        self.df = self.load_df()

    def load_df(self):
        """Loads goal dataframe from csv file.
        If it doesn't exist, creates a new dataframe."""

        if os.path.isfile(self.filepath):
            print("Found {}!".format(self.filepath))
            loaded = pd.read_csv(self.filepath, parse_dates=['datetime'], index_col=0)
            return loaded
        else:
            print("Starting a-fresh in {}!".format(self.filepath))
            df = pd.DataFrame(columns=['datetime', 'count'], )
            return df

    def progress(self, added_value):
        """Appends occurence of goal with current time to the dataframe's end."""
        current_datetime = datetime.datetime.today()
        self.df.loc[len(self.df)] = [current_datetime, added_value]
        self.save_df()

    def days_for_calculation(self, only_today=False):

        first_day = self.startdate
        x_plot = pd.date_range(start=first_day, end=Goal.tomorrow_plotting_date,
                               freq=str(self.period) + 'D')

        if only_today:
            return np.arange(x_plot.size)[-1]
        else:
            return x_plot

    def calculate_supposed_progress(self, days_for_calc):
        y_supposed = self.polynomial(days_for_calc)
        return y_supposed

    def plot_cumsum(self, show=True):
        """Plots a neat comparison of your progress, compared to what you wanted
        to accomplish in that area."""

        y = self.df['count'].cumsum()
        x = self.df['datetime']

        x_plot = self.days_for_calculation()
        # TODO: use np.polyval here!
        y_supposed = self.calculate_supposed_progress(np.arange(x_plot.size))

        fig, ax = plt.subplots()
        ax.set_title(self.shortname.upper())
        ax.plot(x, y, "bo--", label="Your progress!")
        ax.plot(x_plot, y_supposed, "r-", label="How you should be doing!")
        ax.fill_between(x_plot, y_supposed - self.leeway, y_supposed + self.leeway, color="yellow", alpha=0.5)
        for sign in [-1, +1]:
            for value, color in [(1, "orange"), (2, "red")]:
                ax.fill_between(x_plot, y_supposed + sign * (value + 1) * self.leeway,
                                y_supposed + value * sign * self.leeway, color=color, alpha=0.3)
        ax.vlines([datetime.datetime.today()],
                  y_supposed.min(),
                  max((y.max(), y_supposed.max())),
                  "k", "--", label="Right now!")
        ax.hlines(y.iloc[-1], x.iloc[-1], datetime.datetime.today(), 'k', '--')
        ax.legend(loc='best')
        ax.grid()
        ax.set_xlabel("Time")
        ax.set_ylabel("Progress")
        ax.set_xlim(self.startdate, Goal.tomorrow_date)
        if show:
            plt.show()

    def review_progress(self):
        current_progress = self.df['count'].sum()
        supposed_progress = self.calculate_supposed_progress(self.days_for_calculation(True))
        progress_diff = current_progress - supposed_progress
        periods_to_equalize = ((self.polynomial - current_progress).r - self.days_for_calculation(True)).max()

        # cur_day = self.days_for_calculation(True)
        # prog_rate = self.polynomial.deriv()(cur_day)
        # print(f"Current rate of progress is {prog_rate} units per {self.period} days.")
        if progress_diff > 0:
            print(textwrap.dedent(f"""Awesome! You're {progress_diff:.1f} units ahead in {self.shortname}.
                    You can, if need be, slack off safely for {np.floor(periods_to_equalize*self.period).astype(int)} days.
                    Or we could kick it up a notch..."""))  # TODO: difficulty increase option
        elif progress_diff == 0:
            print(f"You're EXACTLY on track in {self.shortname}. W00t.")
        else:  # progress_diff < 0:
            print(textwrap.dedent(f"""
                You're {-progress_diff:.1f} units behind in {self.shortname}.
                You would need to do {-progress_diff:.1f} units to catch up right now,
                which is equivalent to {np.floor(-periods_to_equalize*self.period).astype(int)} days' work.
                Get to it."""))

    def save_df(self):
        """Saves the dataframe to .csv."""
        print(self.df.to_csv(self.filepath))