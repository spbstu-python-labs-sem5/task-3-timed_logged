from dataclasses import dataclass
from functools import wraps
from time import perf_counter


MAX_LOG_LENGTH = 100
TRUNCATION_MARK = "..."


@dataclass(frozen=True)
class Timing:
    name: str
    args: tuple
    kwargs: dict
    elapsed_ms: float


TIMINGS: list[Timing] = []


def _short_repr(value):
    rendered = repr(value)
    limit = MAX_LOG_LENGTH - len(TRUNCATION_MARK)
    return rendered if len(rendered) <= MAX_LOG_LENGTH else rendered[:limit] + TRUNCATION_MARK


def _record_call(func, args, kwargs, started, result=None, error=None):
    elapsed = (perf_counter() - started) * 1000
    TIMINGS.append(Timing(func.__name__, args, kwargs, elapsed))
    call = _short_repr((args, kwargs))
    outcome = f"{type(error).__name__}: {error}" if error is not None else _short_repr(result)
    print(f"{func.__name__}{call} -> {outcome} [{elapsed:.3f} ms]")


def timed_logged(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        started = perf_counter()
        try:
            result = func(*args, **kwargs)
        except Exception as error:
            _record_call(func, args, kwargs, started, error=error)
            raise
        _record_call(func, args, kwargs, started, result=result)
        return result

    return wrapper
