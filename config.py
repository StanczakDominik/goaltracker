from collections import namedtuple

goal_info = namedtuple("goal_info", ['shortname', 'description', 'startdate', 'period', 'derivatives'])
conf_path = "/home/dominik/private_notes/goaltracker/"

goals = [goal_info("pushups", "20 pushups first day in morning", "2017-01-09", 1, [20, 1 / 2]),
         ]
