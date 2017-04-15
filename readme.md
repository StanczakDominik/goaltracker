# Goaltracker
A Beeminder inspired  program to help track progress on habits you want to implement
and generate pretty plots while you're at it. Shoutout to Beeminder for creating a wonderful service!

Mostly based on the data science Python ecosystem, written with Pandas practice in mind.

### Current status

This project is mostly abandoned now. I've learned what I wanted, including that the folks at Beeminder are true badasses.

## Usage
1. Put the directory where you want to store your data in `config` (see `config.sample`).
2. Use `goaltracker.py --create` to create your next goal to track. The arguments for that are
    1. short name
    2. longer description
    3. start date for the goal, `YYYY-MM-DD`
    4. update period ("I want to do `X` per this many days")
    5. progress derivatives:
      1. how many units of your activity you want to do every period
      2. how many units of your activity do you want to add every period
      3. how fast do you want to increase the rate of change mentioned above
      4. and so on, as many as you'd like
    
    So an example would be `--create thesisrefactor "A refactoring commit" 2017-02-22 7 4 1` for 4 thesis commits each
    week, with 1 additional added per week.
