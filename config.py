# coding=utf-8
import os
from collections import namedtuple

goal_info = namedtuple("goal_info", ['shortname', 'description', 'startdate', 'period', 'derivatives', 'filename'])

with open(os.path.dirname(os.path.realpath(__file__)) + "/config") as f:
    conf_path = f.readline().rstrip()
    goals = []
    for csv_location in [os.path.join(conf_path, csv) for csv in os.listdir(conf_path)]:
        with open(csv_location) as csv:
            line = csv.readline()
            shortname, description, start_date, period, *derivatives = line.split(";")
        period = int(period)
        derivatives = [float(d) for d in derivatives]
        goal = goal_info(shortname, description, start_date, period, derivatives, csv_location)
        goals.append(goal)