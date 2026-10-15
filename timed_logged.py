from functools import wraps
from time import perf_counter


def timed_logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        started = perf_counter()
        try:
            result = func(*args, **kwargs)
        except BaseException as error:
            elapsed = (perf_counter() - started) * 1000
            print(
                f"{func.__name__}(args={args}, kwargs={kwargs}) -> "
                f"{type(error).__name__}: {error} [{elapsed:.3f} ms]"
            )
            raise

        elapsed = (perf_counter() - started) * 1000
        print(
            f"{func.__name__}(args={args}, kwargs={kwargs}) -> "
            f"{result!r} [{elapsed:.3f} ms]"
        )
        return result

    return wrapper
