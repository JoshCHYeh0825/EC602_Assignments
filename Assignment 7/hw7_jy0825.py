# Copyright 2024 Josh Yeh jy0825@bu.edu

import unittest
import importlib.util
import os
import pylint.lint

# Directory containing submissions
submissions_dir = os.path.join(os.getcwd(), "wedding_examples")

# Testing environment Setup


class TestSetup:

    @staticmethod
    def iterate_submissions(test_case, test_func, test_name, max_points):
        for file in os.listdir(submissions_dir):
            if file.startswith("wedding") and file.endswith(".py"):
                file_path = os.path.join(submissions_dir, file)
                try:
                    Wedding = TestSetup.import_wedding(file_path)
                    test_func(test_case, Wedding(), file, test_name, max_points)
                except Exception as e:
                    test_case.add_result(f"{test_name}_{file}", 0, max_points, str(e))

    @staticmethod
    def import_wedding(file_path):
        spec = importlib.util.spec_from_file_location("Wedding", file_path)
        wedding_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wedding_module)
        return wedding_module.Wedding


# Test Points Configuration
test_scores = {
    "test_shuffle": 35,
    "test_shuffle_single": 5,
    "test_shuffle_double": 5,
    "test_barriers": 35,
    "test_no_bars": 10,
    "test_formatting": 10,
}

earned_scores = {test: {"earned": 0, "max": max_points, "error": None}
                 for test, max_points in test_scores.items()}

# Custome class to add results


class CustomTestCase(unittest.TestCase):
    def add_result(self, test_name, earned, max_points, error_msg=None):
        earned_scores[test_name] = {"earned": earned, "max": max_points, "error": error_msg}

# Shuffle tests


class Shuffle_Test(CustomTestCase):
    def test_shuffle(self):
        def test(test_case, wedding):
            guests = "abc"
            expected = ["abc", "acb", "bac", "bca", "cab", "cba"]
            result = wedding.shuffle(guests)
            test_case.assertEqual(sorted(result), sorted(expected))

        TestSetup.iterate_submissions(self, test, "test_shuffle", test_scores["test_shuffle"])

    def test_shuffle_single(self):
        def test(test_case, wedding):
            guests = "a"
            expected = ["a"]
            result = wedding.shuffle(guests)
            self.assertEqual(result, expected)

        TestSetup.iterate_submissions(self, test, "test_shuffle_single", test_scores["test_shuffle_single"])

    def test_shuffle_double(self):
        def test(test_case, wedding):
            guests = "ab"
            expected = ["ab", "ba"]
            result = wedding.shuffle(guests)
            self.assertEqual(sorted(result), sorted(expected))

        TestSetup.iterate_submissions(self, test, "test_shuffle_double", test_scores["test_shuffle_double"])

# Barriers Tests


class Barriers_Test(CustomTestCase):

    def test_barriers(self):
        def test(test_case, wedding):
            guests = "abcd"
            bars = {1, 2}
            expected = ["ab|cd", "ab|dc", "ba|cd", "ba|dc", "db|ca"]
            result = wedding.barriers(guests, bars)
            test_case.assertEqual(sorted(result), sorted(expected))

        TestSetup.iterate_submissions(self, test, "test_barriers", test_scores["test_barriers"])

    def test_no_bars(self):
        def test(test_case, wedding):
            guests = "abc"
            bars = sorted(list(set()))
            expected = ["abc", "acb", "bac", "bca", "cab", "cba"]
            result = wedding.barriers(guests, bars)
            test_case.assertEqual(sorted(result), sorted(expected))

        TestSetup.iterate_submissions(self, test, "test_no_bars", test_scores["test_no_bars"])

# Formatting Test


class Formatting_Test(CustomTestCase):
    def test_formatting(self):
        for file in os.listdir(submissions_dir):
            if file.startswith("wedding") and file.endswith(".py"):
                file_path = os.path.join(submissions_dir, file)
                pylint_opts = [file_path, '--output-format=text']
                try:
                    pylint_result = pylint.lint.Run(pylint_opts, do_exit=False)
                    score = pylint_result.linter.stats.global_note
                    self.assertGreaterEqual(score, 7, f"Pylint score too low: {score}")
                    self.add_result(f"test_formatting_{file}", score, test_scores["test_formatting"])
                except Exception as e:
                    self.add_result(f"test_formatting_{file}", 0, test_scores["test_formatting"], str(e))

# Running the script


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
    )
    print("\nFinal Test Results:")
    for test, result in earned_scores.items():
        print(f"{test:<20} {result['earned']:<10} {result['max']:<10} {result['error']}")