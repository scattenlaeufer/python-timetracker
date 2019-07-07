#!/usr/bin/env python3

import datetime
import csv
import os
from pathlib import Path
import argparse


time_file_name = "time"
date_format = "%Y-%m-%d %H:%M"

parser = argparse.ArgumentParser(
    description="A script to track the time spend on a project"
)
parser.add_argument(
    "description",
    type=str,
    help="a short description of the current task",
    nargs=argparse.REMAINDER,
)
parser.add_argument(
    "-a", "--analyze", help="show a small report", default=False, action="store_true"
)
command_group = parser.add_mutually_exclusive_group()
command_group.add_argument(
    "-b", "--start", help="start working", default=False, action="store_true"
)
command_group.add_argument(
    "-e", "--stop", help="stop working", default=False, action="store_true"
)

args = parser.parse_args()

time = []
time_file_path = Path(os.path.dirname(os.path.abspath(__file__))) / time_file_name
with time_file_path.open() as time_file:
    time_csv = csv.reader(time_file, delimiter="\t")
    for row in time_csv:
        time.append(row)


def format_duration(duration):
    duration_hours = int(duration.total_seconds()) // 3600
    duration_minutes = (int(duration.total_seconds()) % 3600) // 60
    return f"{duration_hours: 2}:{duration_minutes:02}"


if args.stop:
    if time[-1][1]:
        print("There is currently no work session running!")
        exit()
    else:
        time[-1][1] = datetime.datetime.now().strftime(date_format)
        if args.description and time[-1][2]:
            answer = True
            while not answer in ("y", "Y", "n", "N", ""):
                answer = input(
                    f"There is already a decription: {time[-1][2]}\nOverwrite it? [y/N]"
                )
            if answer in ("y", "Y"):
                time[-1][2] = " ".join(args.description)

if args.analyze:
    duration_total = datetime.timedelta(seconds=0)
    print("Start" + " " * 12 + "| End" + " " * 14 + "| Time  | Description")
    print("-" * 17 + "+" + "-" * 18 + "+" + "-" * 7 + "+" + "-" * 18)
    for work_session in time:
        start = datetime.datetime.strptime(work_session[0], date_format)
        if work_session[1]:
            end = datetime.datetime.strptime(work_session[1], date_format)
        else:
            end = datetime.datetime.now()
        duration = end - start
        duration_total += duration
        duration_str = format_duration(duration)
        print(
            f"{start.strftime(date_format)} | {end.strftime(date_format)} | {duration_str} | {work_session[2]}"
        )
    print(f"\nTotal time worked: {format_duration(duration_total)}")

if args.start:
    if not time[-1][1]:
        print(
            "There is a work session still going on. Finish it before starting a new one!"
        )
    else:
        if args.description:
            time.append(
                [
                    datetime.datetime.now().strftime(date_format),
                    "",
                    " ".join(args.description),
                ]
            )
        else:
            time.append([datetime.datetime.now().strftime(date_format), "", ""])

if args.start or args.stop:
    with time_file_path.open("w") as time_file:
        time_csv = csv.writer(time_file, delimiter="\t")
        time_csv.writerows(time)
