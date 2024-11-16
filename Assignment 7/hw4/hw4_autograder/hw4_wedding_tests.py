# %%
# Tests

import otter
import subprocess
import unittest
import importlib.util
import sys
import os

assignment_name = "wedding_assignment"
requirements = ["otter-grader"]
grader = otter.Notebook()


submissions_dir = os.path.join(os.getcwd(), "submissions")

# %%


class TestSetup:

    # Dynamic import of Wedding class
    @staticmethod
    def import_wedding(file_path):
        spec = importlib.util.spec_from_file_location("student_wedding",
                                                      file_path)
        student_wedding = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student_wedding)
        return student_wedding.Wedding

    # Iterate through all submissions and apply the test
    @staticmethod
    def iterate_submissions(test_func):
        for file in os.listdir(submissions_dir):
            if file.startswith("wedding") and file.endswith(".py"):
                file_path = os.path.join(submissions_dir, file)
                with unittest.TestCase().subTest(filename=file):
                    Wedding = TestSetup.import_wedding(file_path)
                    test_func(Wedding, file)

    @staticmethod
    def get_pycodestyle_path():
        python_bin = sys.executable
        pycodestyle_path = os.path.join(os.path.dirname(python_bin),
                                        'Scripts', 'pycodestyle')

        if sys.platform == "win32" and not os.path.exists(pycodestyle_path):
            pycodestyle_path = os.path.join(os.path.dirname(python_bin),
                                            'Scripts', 'pycodestyle.exe')

        if os.path.exists(pycodestyle_path):
            return pycodestyle_path

        return "pycodestyle"

# %%
# Shuffle


class Shuffle_Test(unittest.TestCase):

    def test_shuffle(self):
        def test(wedding, file):
            wedding = Wedding()
            guests = "abc"
            expected = ["abc", "acb", "bac", "bca", "cab", "cba"]
            result = wedding.shuffle(guests)
            self.assertEqual(sorted(result), sorted(expected))

        TestSetup.iterate_submissions(test)

    def test_shuffle_single(self):
        def test(wedding, file):
            wedding = Wedding()
            guests = "a"
            expected = ["a", "a"]
            result = wedding.shuffle(guests)
            self.assertEqual(result, expected)

        TestSetup.iterate_submissions(test)

    def test_shuffle_double(self):
        def test(wedding, file):
            wedding = Wedding()
            guests = "ab"
            expected = ["ab", "ba"]
            result = wedding.shuffle(guests)
            self.assertEqual(sorted(result), sorted(expected))

        TestSetup.iterate_submissions(test)


# %%
# Barriers


class Barriers_Test(unittest.TestCase):

    def test_barriers(self):
        def test(wedding, file):
            wedding = Wedding()
            guests = "abcd"
            bars = {2}
            expected = ["ab|cd", "ab|dc", "ba|cd", "ba|dc", "db|ca"]
            result = wedding.barriers(guests, bars)
            self.assertEqual(sorted(result), sorted(expected))

        TestSetup.iterate_submissions(test)

    def test_no_bars(self):
        def test(wedding, file):
            wedding = Wedding()
            guests = "abc"
            bars = set()
            expected = ["abc", "acb", "bac", "bca", "cab", "cba"]
            result = set(wedding.barriers(guests, bars))
            self.assertEqual(result, expected)

        TestSetup.iterate_submissions(test)

    def test_multiple_bars(self):
        def test(wedding, file):
            wedding = Wedding()
            guests = "abcd"
            bars = {1, 3}
            expected = ["a|b|cd", "a|b|dc",
                        "b|a|cd", "b|a|dc",
                        "c|a|bd", "c|a|db",
                        "d|a|bc", "d|a|cb",
                        "a|c|bd", "a|c|db",
                        "a|d|bc", "a|d|cb"]
            result = set(wedding.barriers(guests, bars))
            self.assertEqual(result, expected)

        TestSetup.iterate_submissions(test)


# %%
# Formatting

class pep8_test(unittest.TestCase):

    def test_formatting(self):
        def test(_, file):
            file_path = os.path.join(submissions_dir, file)

            pycodestyle_path = TestSetup.get_pycodestyle_path()

            result = subprocess.run(
                [pycodestyle_path, file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True)

            mistakes = result.stdout.strip()
            self.assertEqual(mistakes, "",
                             f"Formatting Mistakes found:\n{mistakes}")

        TestSetup.iterate_submissions(test)


# %%
if __name__ == "__main__":
    # Test a sample submission
    sample_file = os.path.join(submissions_dir, "wedding0.py")
    if os.path.exists(sample_file):
        Wedding = TestSetup.import_wedding(sample_file)
        sample = Wedding()

        print("Running sample tests:")
        unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Shuffle_Test)
        )
    else:
        print(f"Sample file {sample_file} not found. Running all tests...")

    # Run all tests
    unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    )


# %%
"""
# Run all tests
if __name__ == "__main__":
    unittest.main()
"""
