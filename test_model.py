import unittest
from datetime import date
from model import MeasurementParser, MeasurementRepository
import tempfile
import os


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

    def _create_temp_file(self, content: str):
        tmp = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_load_skips_invalid_lines(self):
        content = (
            '2024.03.10 23.5 "Красный" "Авто" "Иркутск"\n'
            'invalid line\n'
            '2024.03.11 20.0 "Синий" "Ручной" "Ачинск"\n'
        )

        filename = self._create_temp_file(content)
        try:
            result = self.repo.load_from_file(filename)
            self.assertEqual(len(result), 2)
        finally:
            os.remove(filename)

    # Тест на пропуск пустых строк
    def test_skip_empty_lines(self):
        content = (
            '\n'
            '2024.03.10 23.5 "Красный" "Авто" "Иркутск"'
            '\n'
        )
        filename = self._create_temp_file(content)
        try:
            result = self.repo.load_from_file(filename)
            self.assertEqual(len(result), 1)
        finally:
            os.remove(filename)

    # Тест на загрузку пустого файла
    def test_load_empty_file(self):
        filename = self._create_temp_file("")
        try:
            result = self.repo.load_from_file(filename)
            self.assertEqual(result, [])
        finally:
            os.remove(filename)


if __name__ == '__main__':
    unittest.main()