from math import isfinite
from random import uniform
from time import sleep

from timed_logged import timed_logged


@timed_logged
def random_sleep(use_random_val=False):
    seconds = uniform(0, 0.06) if use_random_val else float(input("Enter sleep duration in seconds: "))
    if not isfinite(seconds) or seconds < 0:
        raise ValueError("Sleep duration must be a finite non-negative number of seconds")
    sleep(seconds)
    return seconds


if __name__ == "__main__":
    random_sleep()
