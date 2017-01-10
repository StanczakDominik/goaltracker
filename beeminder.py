import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime

goals = {"pushups", "meditation", "duolingo"}
class Goal:
    """Class representing a goal you want to pursue.

    Goal("pushups", "20 pushups first day in morning", 20, 1)
    shortname - short, no spaces, name for goal
    description - more verbose description
    count - how many you want to do...
    period - per how many days
    """
    def __init__(self, shortname, description, count, period):
        # TODO: readable format for period?
        self.shortname = shortname
        self.description = description
        self.count = count
        self.period = period
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
        g.save_df()

    def plot_cumsum(self):
        """Plots a neat comparison of your progress, compared to what you wanted
        to accomplish in that area."""

        y = self.df['count'].cumsum()
        x = self.df['datetime']
        plt.plot(x,y, "bo--", label="Your progress!")

        first_day = self.df['datetime'][0].to_pydatetime()

        all_days = (datetime.datetime.today()-first_day).days
        x_plot = pd.date_range(start=first_day, end=datetime.datetime.today()+datetime.timedelta(1), freq=str(self.period)+'D')
        y_supposed = np.arange(x_plot.size) * self.count / self.period + self.count

        plt.plot(x_plot, y_supposed, "r-", label="How you should be doing!")
        plt.vlines([datetime.datetime.today()], y_supposed.min(), y_supposed.max(), "k", "--", label="Right now!")
        plt.legend(loc='best')
        plt.grid()
        plt.xlabel("")
        plt.show()

    def save_df(self):
        """Saves the dataframe to .csv."""
        self.df.to_csv(self.shortname + ".csv")
if __name__=="__main__":
    g = Goal("pushups", "20 pushups first day in morning", 20, 1)
    # print(g.df)
    # for i in range(10):
    #     g.progress(i)
    # # g.df.set_value(0,'datetime', datetime.datetime(2017,1,1))
    # # g.save_df()
    g.plot_cumsum()
