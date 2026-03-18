from dataclasses import dataclass
from datetime import date

@dataclass
class TemperatureMeasurement:
    date: date
    type_measure: str
    location: str
    value: float
            
line = '    2026.02.10   "Автоматический"    "Nizhny Novgorod"    -5.6    '
strings = []
while '"' in line:
    ind1 = line.find('"')
    ind2 = line.find('"', ind1+1)
    strings.append(line[ind1+1:ind2])
    line = line[:ind1] + line[ind2+1:]

type_measure, location = strings

digits = line.split()
year, month, day = [int(c) for c in digits[0].split('.')]
date_ = date(year, month, day)
value = float(digits[1])

temp = TemperatureMeasurement(date_, type_measure, location, value)

print(temp.date, temp.type_measure, temp.location, temp.value)
