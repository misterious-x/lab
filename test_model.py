import unittest
from unittest.mock import mock_open, patch
from datetime import date
from model import MeasurementParser, MeasurementRepository, CommandProcessor, TemperatureMeasurement

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

class TestCommands(unittest.TestCase):

    def test_add_command(self):
        data = []
        processor = CommandProcessor(data)

        processor.execute("ADD 2024.03.10;Красный;Авто;Иркутск;23.5")

        self.assertEqual(len(data), 1)

    def test_remove_command(self):
        data = [
            TemperatureMeasurement(date(2024, 3, 10), "Красный", "Авто", "Иркутск", 500),
            TemperatureMeasurement(date(2024, 3, 11), "Синий", "Ручной", "Ачинск", 1500),
        ]

        processor = CommandProcessor(data)
        processor.execute("REM value < 1000")

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].value, 1500)

    @patch("builtins.open", new_callable=mock_open)
    def test_save_command(self, mock_file):
        data = [
            TemperatureMeasurement(date(2024, 3, 10), "Красный", "Авто", "Иркутск", 23.5)
        ]

        processor = CommandProcessor(data)
        processor.execute("SAVE test.txt")

        mock_file.assert_called_with("test.txt", 'w', encoding='utf-8')

if __name__ == '__main__':
    unittest.main()