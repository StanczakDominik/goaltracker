import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime

goals = {"pushups", "meditation", "duolingo"}
class Goal:
    """Class representing a goal you want to pursue."""
    def __init__(self, shortname, description, count, period):
        """
        Goal("pushups", "20 pushups first day in morning", 20, "1 day")
        """
        # TODO: readable format for period?
        self.shortname = shortname
        self.description = description
        self.count = count
        self.period = period
        self.df = self.load_df()

    def load_df(self):
        filename = self.shortname + ".csv"
        if os.path.isfile(filename):
            return pd.read_csv(filename)
        else:
            df = pd.DataFrame(columns=['datetime','count'])
            return df

    def append_df(self, value):
        current_datetime = datetime.datetime.today()
        self.df.loc[len(self.df)] = [current_datetime, value]


    def plot_cumsum(self):
        y = self.df['count'].cumsum()
        x = self.df['datetime']
        plt.plot(x,y)
        plt.show()
if __name__=="__main__":
    g = Goal("pushups", "20 pushups first day in morning", 20, "1 day")
    for i in range(10):
        g.append_df(i)
    print(g.df)
    g.plot_cumsum()
