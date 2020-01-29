#!/usr/bin/env python3

import datetime

def strToDatetime(time_str, time_format):
    return datetime.datetime.strptime(time_str, time_format)

def timeDiff(start, stop):
    elapsed_time = stop - start
    return elapsed_time.total_seconds()

