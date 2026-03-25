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

class CommandProcessor:
    def __init__(self, measurements: list):
        self.measurements = measurements

    def execute_file(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    self.execute(line)
                except Exception as e:
                    logging.warning(f"Ошибка в команде {i}: {line} ({e})")

    def execute(self, command_line: str):
        if command_line.startswith("ADD"):
            self._add(command_line[3:].strip())
        elif command_line.startswith("REM"):
            self._remove(command_line[3:].strip())
        elif command_line.startswith("SAVE"):
            self._save(command_line[4:].strip())
        else:
            raise ValueError(f"Неизвестная команда: {command_line}")

    def _add(self, data: str):
        parts = [p.strip() for p in data.split(';')]
        if len(parts) != 5:
            raise ValueError("Неверный формат ADD")

        year, month, day = map(int, parts[0].split('.'))

        m = TemperatureMeasurement(
            date(year, month, day),
            parts[1],
            parts[2],
            parts[3],
            float(parts[4])
        )

        self.measurements.append(m)

    def _remove(self, condition: str):
        parts = condition.split()
        if len(parts) != 3:
            raise ValueError("Неверный формат REM")

        field, op, value = parts

        def check(m):
            attr = getattr(m, field)
            
            if isinstance(attr, date):
                attr_val = attr.strftime("%Y.%m.%d")
                cmp_val = value
            elif isinstance(attr, (int, float)):
                attr_val = float(attr)
                cmp_val = float(value)
            else:
                attr_val = str(attr)
                cmp_val = value

            if op == "<":
                return attr_val < cmp_val
            elif op == ">":
                return attr_val > cmp_val
            elif op == "==":
                return attr_val == cmp_val
            else:
                raise ValueError("Неизвестная операция")

        self.measurements[:] = [m for m in self.measurements if not check(m)]

    def _save(self, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            for m in self.measurements:
                line = f'{m.date.strftime("%Y.%m.%d")} {m.value} "{m.color}" "{m.type_measure}" "{m.location}"\n'
                f.write(line)