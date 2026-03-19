from dataclasses import dataclass
from datetime import date
import logging


@dataclass
class TemperatureMeasurement:
    date: date
    color: str
    type_measure: str
    location: str
    value: float


class MeasurementParser:
    def parse(self, line: str) -> TemperatureMeasurement:
        strings, remaining_line = self._extract_strings(line)

        if len(strings) != 3:
            raise ValueError("Неверное количество строковых полей")
        
        color, type_measure, location = strings

        parts = remaining_line.split()
        if len(parts) != 2:
            raise ValueError("Неверное количество нестроковых полей")

        date_ = self._parse_date(parts[0])
        value = self._parse_value(parts[1])

        return TemperatureMeasurement(date_, color, type_measure, location, value)

    def _extract_strings(self, line: str):
        strings = []

        while '"' in line:
            start = line.find('"')
            end = line.find('"', start + 1)

            if end == -1:
                raise ValueError("Незакрытая кавычка")

            strings.append(line[start + 1:end])
            line = line[:start] + line[end + 1:]

        return strings, line

    def _parse_date(self, date_str: str) -> date:
        try:
            year, month, day = map(int, date_str.split('.'))
            return date(year, month, day)
        except Exception:
            raise ValueError("Неверный формат даты")

    def _parse_value(self, value_str: str) -> float:
        try:
            return float(value_str)
        except Exception:
            raise ValueError("Неверный формат числа")


class MeasurementRepository:
    def __init__(self, parser: MeasurementParser):
        self.parser = parser

    def load_from_file(self, filename: str):
        result = []

        with open(filename, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                try:
                    m = self.parser.parse(line)
                    result.append(m)
                except Exception as e:
                    logging.warning(f"Ошибка в строке {i}: {line} ({e})")

        return result
