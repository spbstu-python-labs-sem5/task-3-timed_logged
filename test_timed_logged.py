import contextlib
import io
import unittest
from unittest.mock import patch

from timed_logged import TIMINGS, timed_logged


class TimedLoggedTests(unittest.TestCase):
    def setUp(self):
        TIMINGS.clear()

    def test_logs_name_arguments_result_and_elapsed_milliseconds(self):
        @timed_logged
        def combine(*args, separator="-", **kwargs):
            "Combine values."
            return separator.join(map(str, (*args, *kwargs.values())))

        output = io.StringIO()
        with patch("timed_logged.perf_counter", side_effect=(1.0, 1.0125)):
            with contextlib.redirect_stdout(output):
                result = combine("a", "b", separator=":", extra="c")

        self.assertEqual(result, "a:b:c")
        self.assertIn("combine", output.getvalue())
        self.assertIn("('a', 'b')", output.getvalue())
        self.assertIn("'extra': 'c'", output.getvalue())
        self.assertIn("a:b:c", output.getvalue())
        self.assertIn("12.500 ms", output.getvalue())
        self.assertAlmostEqual(TIMINGS[-1].elapsed_ms, 12.5)

    def test_preserves_function_name_and_docstring(self):
        def original(value):
            "Original function documentation."
            return value

        decorated = timed_logged(original)

        self.assertEqual(decorated.__name__, "original")
        self.assertEqual(decorated.__doc__, "Original function documentation.")

    def test_logs_exception_and_reraises_it(self):
        @timed_logged
        def fail(value):
            raise ValueError(f"bad value: {value}")

        output = io.StringIO()
        with patch("timed_logged.perf_counter", side_effect=(2.0, 2.005)):
            with contextlib.redirect_stdout(output), self.assertRaisesRegex(ValueError, "bad value: 7"):
                fail(7)

        self.assertIn("ValueError: bad value: 7", output.getvalue())
        self.assertIn("5.000 ms", output.getvalue())
        self.assertEqual(TIMINGS[-1].name, "fail")


if __name__ == "__main__":
    unittest.main()
