# Goaltracker
A Beeminder inspired  program to help track progress on habits you want to implement
and generate pretty plots while you're at it. Shoutout to Beeminder for creating a wonderful service!

Mostly based on the data science Python ecosystem, written with Pandas practice in mind.

## Usage
1. Create a `config` file based on `config.sample`.
  * The first line is the directory where you want to keep your habit data in .csv format
  * The second line is the list of stuff you want to track, with the following ordering:
    1. short name
    2. longer description
    3. start date for the goal, `YYYY-MM-DD`
    4. update period ("I want to do `X` per this many days")
    5. progress derivatives:
      1. how many units of your activity you want to do every period
      2. how many units of your activity do you want to add every period
      3. how fast do you want to increase the rate of change mentioned above
      4. and so on, as many as you'd like
