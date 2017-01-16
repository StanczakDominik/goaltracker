#!/usr/bin/env python
"""A python implementation of Beeminder style goal tracking"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
from config import goals

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
        self.df = self.load_df()

    def load_df(self):
        """Loads goal dataframe from csv file.
        If it doesn't exist, creates a new dataframe."""

        filename = self.shortname + ".csv"
        if os.path.isfile(filename):
            print("Found {}!".format(filename))
            loaded = pd.read_csv(filename, parse_dates=['datetime'], index_col=0)
            return loaded
        else:
            print("Starting a-fresh in {}!".format(filename))
            df = pd.DataFrame(columns=['datetime','count'], )
            return df

    def progress(self, value):
        """Appends occurence of goal with current time to the dataframe's end."""
        current_datetime = datetime.datetime.today()
        self.df.loc[len(self.df)] = [current_datetime, value]
        self.save_df()

    def plot_cumsum(self):
        """Plots a neat comparison of your progress, compared to what you wanted
        to accomplish in that area."""

        y = self.df['count'].cumsum()
        x = self.df['datetime']

        first_day = self.df['datetime'][0].to_pydatetime()

        all_days = (datetime.datetime.today()-first_day).days
        x_plot = pd.date_range(start=first_day, end=datetime.datetime.today()+datetime.timedelta(1), freq=str(self.period)+'D')
        days_for_calc = np.arange(x_plot.size)
        y_supposed = self.count
        for index, factor in enumerate(self.factors): #TODO: do this via broadcasting
            power = index + 1 # we're starting from 0
            y_supposed += days_for_calc**power * factor / self.period


        fig, ax = plt.subplots()
        ax.set_title(self.shortname.upper())
        ax.plot(x,y, "bo--", label="Your progress!")
        ax.plot(x_plot, y_supposed, "r-", label="How you should be doing!")
        ax.fill_between(x_plot, y_supposed - self.leeway, y_supposed + self.leeway, color="yellow", alpha=0.5)
        ax.vlines([datetime.datetime.today()],
                y_supposed.min(),
                max((y.max(), y_supposed.max())),
                "k", "--", label="Right now!")
        ax.legend(loc='best')
        ax.grid()
        ax.set_xlabel("Time")
        ax.set_ylabel("Progress")
        plt.show()

    def save_df(self):
        """Saves the dataframe to .csv."""
        print(self.df.to_csv(self.shortname + ".csv"))

if __name__=="__main__":
    goal_dict = {}
    # load from config
    for goal_name, goal_data in goals.items():
        goal_dict[goal_name] = Goal(*goal_data)

    # plot current status
    for goal_name, g in goal_dict.items():
        if g.df.size > 0:
            g.plot_cumsum()

    all_names = ""
    for goal_name in goal_dict.keys():
        all_names = all_names + goal_name + ", "
    all_names = all_names.rstrip(", ")
    while True:
        name = "boo"
        while name not in goal_dict.keys():
            name = input("Input goal name. Choose from: {}.".format(all_names))
            if name == "exit":
                exit()
        value = input("Input value for {} update".format(name))
        goal_dict[name].progress(float(value))
        goal_dict[name].plot_cumsum()
