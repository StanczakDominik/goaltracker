#!/usr/bin/env python
"""A python implementation of Beeminder style goal tracking"""

import argparse

from Goal import Goal
from config import goals

debug = False
if debug:
    import matplotlib

    matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def update_goal(goal_name, goal_update_value=1):
    print(f"Added {goal_update_value} to {goal_name}!")
    goal_dict[goal_name].progress(float(goal_update_value))
    goal_dict[goal_name].review_progress()
    if args.show:
        goal_dict[goal_name].plot_cumsum()


if __name__ == "__main__":
    goal_dict = {}
    # load from config
    all_names = ""
    for goal in goals:
        goal_dict[goal.shortname] = Goal(goal.shortname, goal.description, goal.startdate, goal.period,
                                         *goal.derivatives)
        all_names = all_names + goal.shortname + ", "
    all_names = all_names.rstrip(", ")

    parser = argparse.ArgumentParser(
        description='Track goal status and progress. Run without arguments for interactive mode.')
    parser.add_argument("-s", "--show", help="Progress review mode", action="store_true")
    parser.add_argument("-r", "--review", help="Text review mode", action="store_true")
    parser.add_argument("-u", "--update", nargs=2, metavar=('name', 'value'), action='append',
                        help='Update an existing goal')
    parser.add_argument("-c", "--checkoff", nargs=1, metavar=('name',), action='append',
                        help='Update an existing goal by 1.')
    args = parser.parse_args()

    if args.update:  # command line update mode
        for goal_name, goal_update_value in args.update:
            update_goal(goal_name, goal_update_value)
    elif args.checkoff:
        for goal_name in args.checkoff:
            update_goal(*goal_name)
    elif args.review:
        for name, goal in goal_dict.items():
            goal.review_progress()
    elif args.show:  # progress display mode
        for goal in goal_dict.values():
            if len(goal.df) > 0:
                goal.review_progress()
                goal.plot_cumsum(show=False)
        plt.show()

    else:  # interactive mode
        for g in goal_dict.values():
            if g.df.size > 0:
                g.review_progress()
                g.plot_cumsum()
        while True:
            # TODO: streamline this process
            name = "boo"
            while name not in goal_dict.keys():
                # input numbers to update last
                name = input(
                    f"Input goal name. Choose from: {all_names}. Input number to update previous: {name}. (NOT YET IMPLEMENTED)")
                # TODO: input number to update previous
                if name == "exit":
                    exit()
            value = input(f"Input value for {name} update.")
            goal_dict[name].progress(float(value))
            goal_dict[name].plot_cumsum()
            goal_dict[name].review_progress()
