import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

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
        current_datetime = 1
        row = pd.DataFrame([current_datetime, value], columns=self.df.columns)
        self.df.append(row)


    def plot_cumsum(self):
        y = self.df.cumsum('count')
        x = self.df['datetime']
        plt.plot(x,y)
        plt.show()
if __name__=="__main__":
    g = Goal("pushups", "20 pushups first day in morning", 20, "1 day")
    g.append_df(4)
    print(g, g.shortname, g.description, g.count, g.period, g.df)

