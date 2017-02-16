import os
from collections import namedtuple

goal_info = namedtuple("goal_info", ['shortname', 'description', 'startdate', 'period', 'derivatives'])

with open(os.path.dirname(os.path.realpath(__file__)) + "/config", "r") as f:
    conf_path = f.readline().rstrip()
    goals = []
    for line in f.readlines():
        shortname, description, start_date, period, *derivatives = line.split(";")
        period = int(period)
        derivatives = [float(d) for d in derivatives]
        goal = goal_info(shortname, description, start_date, period, derivatives)
        goals.append(goal)

        # for g in goals:
        #     print(g)
        # print(conf_path)
