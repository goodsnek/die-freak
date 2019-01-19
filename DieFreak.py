#!/usr/bin/python3
# DieFreak - A calculator for the frequency table of tabletop dice rolls.
# Author: Eric Kolb - eric@goodsnek.com


import csv
import getopt
import re
import sys


__roll_pattern__: str = r"\s*(?P<pool>\d+)[Dd](?P<facets>\d+)(\s?[Cc]([Hh][Oo][Oo][Ss][Ee])?\s*(?P<choose>\d+))?"


def main(argv):
    freq = {}
    file_out = False
    try:
        opts, args = getopt.getopt(argv, "hr:o:", ["help", "roll=", "out="])
    except getopt.GetoptError:
        print("Invalid arguments. Use -h or --help for syntax.")
        sys.exit(1)
    if len(opts) == 0:
        print("Invalid arguments. Use -h or --help for syntax.")
        sys.exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help_text()
            sys.exit()
        elif opt in ("-o", "--out"):
            file_out = arg
        elif opt in ("-r", "--roll"):
            # Roll the dice!
            pool, facets, chosen = parse_roll(arg)
            rolls = roll_dice(pool, facets, chosen)

            # Calculate the frequency table
            for roll in rolls:
                sum = 0
                for die in roll:
                    sum += die
                if not freq.get(sum):
                    freq[sum] = 1
                else:
                    freq[sum] += 1

    # File output
    if len(freq):
        sorted_freq = dict(sorted(freq.items()))
        if file_out:
            # Write the output to CSV
            with open(file_out, 'w', newline='\n') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                for score in sorted_freq:
                    writer.writerow([score, sorted_freq.get(score)])
                csvfile.close()
        else:
            # Screen output
            print("Roll" + ("\t" * 2) + "Frequency")
            print("=========================")
            for score in sorted_freq:
                print(str(score) + ("\t" * 2) + str(sorted_freq.get(score)))


def parse_roll(roll):
    chosen = -1

    m = re.match(__roll_pattern__, roll)
    if not m:
        raise SyntaxError("Parsing error. Rolls must match 'XdY [choose Z].")
    pool = int(m.group('pool'))
    facets = int(m.group('facets'))
    if m.group('choose'):
        chosen = int(m.group('choose'))

    # Validate parsed values
    if pool < 1:
        print("Dice pool must be at least 1 die.")
        raise ValueError
    elif facets < 1:
        print("Dice must have at least 1 side.")
        raise ValueError
    elif chosen != -1 and chosen > pool:
        print("Number of dice chosen must not be larger than the dice pool.")
        raise ValueError

    return pool, facets, chosen


def roll_dice(pool, facets, chosen):
    all_rolls = []
    roll = []

    # Create the initial roll (all 1s)
    for i in range(pool):
        roll.append(1)
    all_rolls.append(select_dice(roll.copy(), chosen))
    start_roll = roll.copy()
    # Special case: facets = 1
    if facets == 1:
        return all_rolls

    # Proceed in reverse-speedometer style until we're back to 1s
    looped = False
    while not looped:
        roll = tick_roll(roll, facets)

        # Terminate if looped
        if roll == start_roll:
            looped = True
        else:
            # Down-select to chosen number of dice and return.
            all_rolls.append(select_dice(roll.copy(), chosen))
    return all_rolls


def tick_roll(roll, facets, pos=0):
    # Special case - total rollover
    dice = len(roll)
    if pos >= dice:
        for i in range(dice):
            roll[i] = 1
        return roll

    # Standard case - tick die by 1
    roll[pos] += 1

    # Single digit rollover
    if roll[pos] > facets:
        roll[pos] = 1
        return tick_roll(roll, facets, pos+1)
    return roll


def select_dice(results, chosen):
    if chosen < 0:
        return results
    pool_count = len(results)
    if chosen >= pool_count:
        return results

    # Drop the lowest value dice until we've dropped the difference between chosen and the pool
    for each in range(pool_count - chosen):
        min_val = 0
        for i in results:
            if min_val == 0 or i < min_val:
                min_val = i
        results.remove(min_val)
    return results


def help_text():
    print('''
DieFreak - a frequency for dice rolls
=====================================
-h, --help: Displays this help text.
-r "roll", --roll "roll":
        Calculates the frequency table for the roll specified as a parameter.
        Understands "XdY choose Z" where Z <= X and Y >= 1.
        Alternative forms are "XdY" and "XdYcZ".
-o "/path/to/outfile.csv", --roll "/path/to/outfile.csv":
        Outputs the frequency table as a CSV instead of to standard output.
    ''')


main(sys.argv[1:])
