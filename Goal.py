import datetime
import os
import textwrap

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from config import conf_path


class Goal:
    """Class representing a goal you want to pursue.

    Goal("pushups", "20 pushups first thing in morning", 1, 20, 1)
    shortname - short, no spaces, name for goal
    description - more verbose description
    period - per how many days...
    count - how many you want to do
    additional - factors for additional terms in polynomial
    """

    def __init__(self, shortname, description, period, *additional):
        self.shortname = shortname
        self.description = description
        self.period = period
        self.count = additional[0]
        self.leeway = 3 * self.count / period
        self.factors = np.array(additional)
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

        first_day = self.df['datetime'][0].to_pydatetime()
        x_plot = pd.date_range(start=first_day, end=datetime.datetime.today() + datetime.timedelta(1),
                               freq=str(self.period) + 'D')

        if only_today:
            return np.arange(x_plot.size)[-1]
        else:
            return x_plot

    def calculate_supposed_progress(self, days_for_calc):
        y_supposed = self.count
        for index, factor in enumerate(self.factors):  # TODO: do this via broadcasting
            power = index + 1  # we're starting from 0
            y_supposed += days_for_calc ** power * factor / self.period
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
        if show:
            plt.show()

    def review_progress(self):
        current_progress = self.df['count'].sum()
        supposed_progress = self.calculate_supposed_progress(self.days_for_calculation(True))
        progress_diff = -supposed_progress + current_progress
        days_to_equalize = 0  # TODO: solve polynomial equation to get number of days

        if self.factors.size == 2:
            b = self.factors[0] / self.period
            a = self.factors[1] / self.period ** 2
            c = progress_diff
            days_to_equalize = int(round((-b + np.sqrt(b ** 2 - 4 * a * c)) / 2 / a))

        if progress_diff > 0:
            print(textwrap.dedent(f"""Awesome! You're {progress_diff:.1f} units ahead in {self.shortname}.
                    You can, if need be, slack off safely for {days_to_equalize}.
                    Or we could kick it up a notch..."""))  # TODO: difficulty increase option
        elif progress_diff == 0:
            print("You're EXACTLY on track in {self.name}. W00t.")
        else:  # progress_diff < 0:
            print(textwrap.dedent(f"""
                You're {-progress_diff:.1f} units behind in {self.shortname}.
                You would need to do {-progress_diff:.1f} units to catch up right now,
                which is equivalent to {days_to_equalize} days' work.
                Get to it."""))

    def save_df(self):
        """Saves the dataframe to .csv."""
        print(self.df.to_csv(self.filepath))
