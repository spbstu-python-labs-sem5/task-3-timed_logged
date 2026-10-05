from time import sleep

from timed_logged import timed_logged


@timed_logged
def slow_sum(left, right, delay=0.5):
    sleep(delay)
    return left + right


if __name__ == "__main__":
    delay = float(input("Enter sleep duration in seconds: "))
    slow_sum(1, 2, delay=delay)
