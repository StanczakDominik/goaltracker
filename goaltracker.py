#!/usr/bin/env python
# coding=utf-8
"""A python implementation of Beeminder style goal tracking"""

import argparse
import textwrap

from Goal import Goal
from config import goals, conf_path

debug = False
if debug:
    import matplotlib

    matplotlib.use('TkAgg')
# noinspection PyPep8
import matplotlib.pyplot as plt


def update_goal(goal_name, goal_update_value=1):
    print(f"Added {goal_update_value} to {goal_name}!")
    goal_dict[goal_name].progress(float(goal_update_value))
    goal_dict[goal_name].review_progress()
    if args.show:
        goal_dict[goal_name].plot_cumsum()


def create_goal(shortname, description, startdate, period, derivatives):
    descriptor_line = ";".join([shortname, description, startdate, period, *derivatives])
    with open(conf_path + "/" + shortname + ".csv", "w") as f:
        f.write(descriptor_line)
        f.write("\n,datetime,count")

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
    parser.add_argument("-s", "--show", nargs='?', const='go_all', type=str, help="Progress review mode")
    parser.add_argument("-rv", "--review_verbose", help="Verbose Text review mode", action="store_true")
    parser.add_argument("-r", "--review", help="Text review mode", action="store_true")
    parser.add_argument("-rl", "--review_left", help="Text review mode",
                        action="store_true")  # TODO: this needs a cleanup
    parser.add_argument("-u", "--update", nargs=2, metavar=('name', 'value'), action='append',
                        help='Update an existing goal')
    parser.add_argument("-c", "--checkoff", nargs=1, metavar=('name',), action='append',
                        help='Update an existing goal by 1.')
    parser.add_argument("--create", nargs='*', help='Create a goal.')
    args = parser.parse_args()

    if args.update:  # command line update mode
        for goal_name, goal_update_value in args.update:
            update_goal(goal_name, goal_update_value)
    if args.create:
        shortname, description, startdate, period, *derivatives = args.create
        derivatives = [str(int(i)) for i in derivatives]
        print(derivatives)
        create_goal(shortname, description, startdate, period, derivatives)

    if args.checkoff:
        for goal_name in args.checkoff:
            update_goal(*goal_name)
    if args.review_verbose:
        for name, goal in goal_dict.items():
            report = goal.review_progress()

            if report.how_much_ahead > 0:
                print(textwrap.dedent(f"""Awesome! You're {report.how_much_ahead:.1f} units ahead in {goal.shortname}.
                        You can, if need be, slack off safely for {report.days_to_equalize} days.
                        Or we could kick it up a notch..."""))  # TODO: difficulty increase option
            elif report.how_much_ahead == 0:
                print(f"You're EXACTLY on track in {goal.shortname}. W00t.")
            else:  # progress_diff < 0:
                print(textwrap.dedent(f"""
                    You're {-report.how_much_ahead:.1f} units behind in {goal.shortname}.
                    You would need to do {-report.how_much_ahead:.1f} units to catch up right now,
                    which is equivalent to {-report.days_to_equalize} days' work at a current rate of
                    {report.progress_rate} per {goal.period} days.
                    Get to it."""))

    if args.review:
        separator = " | "
        print(separator.join(
            [f"{'HABIT':20}", f"{'AHEAD':6}", f"{'DAYS':6}",
             f"{'RATE':6}"]))

        for name, goal in goal_dict.items():
            report = goal.review_progress()
            table_string = separator.join(
                [f"{goal.shortname:20}", f"{report.how_much_ahead:6.1f}", f"{report.days_to_equalize:6}",
                 f"{report.progress_rate:6.1f}"])
            print(table_string)

    if args.review_left:
        separator = " | "
        print(separator.join(
            [f"{'HABIT':20}", f"{'BEHIND':6}", f"{'DAYS':6}",
             f"{'RATE':6}"]))

        for name, goal in goal_dict.items():  # TODO: sort values
            report = goal.review_progress()
            if report.days_to_equalize < 0:
                table_string = separator.join(
                    [f"{goal.shortname:20}", f"{-report.how_much_ahead:6.1f}", f"{-report.days_to_equalize:6}",
                     f"{report.progress_rate:6.1f}"])
                print(table_string)

    if args.show:  # progress display mode
        for goal in goal_dict.values():
            if (len(goal.df) > 0) and ((args.show == 'go_all') or (goal.shortname == args.show)):
                goal.review_progress()
                goal.plot_cumsum(show=False)
        plt.show()
