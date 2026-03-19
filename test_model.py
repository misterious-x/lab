import unittest
from unittest.mock import mock_open, patch
from datetime import date
from model import MeasurementParser, MeasurementRepository

class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = MeasurementParser()

    def test_valid_line(self):
        line = '2024.03.10 23.5 "Красный" "Авто" "Иркутск"'
        m = self.parser.parse(line)

        self.assertEqual(m.date, date(2024, 3, 10))
        self.assertEqual(m.color, "Красный")
        self.assertEqual(m.type_measure, "Авто")
        self.assertEqual(m.location, "Иркутск")
        self.assertEqual(m.value, 23.5)

    def test_invalid_unclosed_quote(self):
        line = '2024.03.10 23.5 "Красный "Авто" "Иркутск"'
        with self.assertRaises(ValueError):
            self.parser.parse(line)

    def test_invalid_date(self):
        line = '2024.15.10 23.5 "Красный" "Авто" "Иркутск"'
        with self.assertRaises(ValueError):
            self.parser.parse(line)

    def test_invalid_value(self):
        line = '2024.03.10 abc "Красный" "Авто" "Иркутск"'
        with self.assertRaises(ValueError):
            self.parser.parse(line)


class TestRepository(unittest.TestCase):

    def setUp(self):
        self.repo = MeasurementRepository(MeasurementParser())

    def test_load_skips_invalid_lines(self):
        content = (
            '2024.03.10 23.5 "Красный" "Авто" "Иркутск"\n'
            'invalid line\n'
            '2024.03.11 20.0 "Синий" "Ручной" "Ачинск"\n'
        )

        with patch("builtins.open", mock_open(read_data=content)):
            result = self.repo.load_from_file("fake.txt")

        self.assertEqual(len(result), 2)

    def test_skip_empty_lines(self):
        content = (
            '\n'
            '2024.03.10 23.5 "Красный" "Авто" "Иркутск"\n'
            '\n'
        )

        with patch("builtins.open", mock_open(read_data=content)):
            result = self.repo.load_from_file("fake.txt")

        self.assertEqual(len(result), 1)

    def test_load_empty_file(self):
        with patch("builtins.open", mock_open(read_data="")):
            result = self.repo.load_from_file("fake.txt")

        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()