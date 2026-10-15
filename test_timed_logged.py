import contextlib
import io
import unittest
from unittest.mock import patch

from timed_logged import timed_logged


class TimedLoggedTests(unittest.TestCase):
    def test_logs_name_arguments_result_and_elapsed_milliseconds(self):
        @timed_logged
        def combine(*args, separator="-", **kwargs):
            "Combine values."
            return separator.join(map(str, (*args, *kwargs.values())))

        output = io.StringIO()
        long_value = "x" * 150
        with patch("timed_logged.perf_counter", side_effect=(1.0, 1.0125)):
            with contextlib.redirect_stdout(output):
                result = combine("a", "b", separator=":", extra="c", payload=long_value)

        self.assertEqual(result, f"a:b:c:{long_value}")
        self.assertIn("combine", output.getvalue())
        self.assertIn("('a', 'b')", output.getvalue())
        self.assertIn("'extra': 'c'", output.getvalue())
        self.assertIn(long_value, output.getvalue())
        self.assertIn("12.500 ms", output.getvalue())

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

    def test_logs_base_exception_and_reraises_it(self):
        @timed_logged
        def stop():
            raise KeyboardInterrupt("stop")

        output = io.StringIO()
        with patch("timed_logged.perf_counter", side_effect=(2.0, 2.005)):
            with contextlib.redirect_stdout(output), self.assertRaisesRegex(
                KeyboardInterrupt, "stop"
            ):
                stop()

        self.assertIn("KeyboardInterrupt: stop", output.getvalue())
        self.assertIn("5.000 ms", output.getvalue())


if __name__ == "__main__":
    unittest.main()
