from tkinter import Tk, ttk, Button, Entry, Label, END, StringVar
import tkinter.messagebox as msgbox
from datetime import date
from model import TemperatureMeasurement


class TemperatureApp:
    def __init__(self, root, repository):
        self.root = root
        self.root.title("Temperature Measurements")

        self.repository = repository
        self.measurements = []

        self.tree = ttk.Treeview(root, columns=("date", "color", "type", "location", "value"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor='center')
        self.tree.pack(fill='both', expand=True)

        self._add_controls()

    def _add_controls(self):
        Label(self.root, text="Дата (гггг.мм.дд):").pack()
        self.date_var = StringVar()
        Entry(self.root, textvariable=self.date_var).pack()

        Label(self.root, text="Цвет:").pack()
        self.color_var = StringVar()
        Entry(self.root, textvariable=self.color_var).pack()

        Label(self.root, text="Режим работы:").pack()
        self.type_var = StringVar()
        Entry(self.root, textvariable=self.type_var).pack()

        Label(self.root, text="Место измерения:").pack()
        self.location_var = StringVar()
        Entry(self.root, textvariable=self.location_var).pack()

        Label(self.root, text="Значение:").pack()
        self.value_var = StringVar()
        Entry(self.root, textvariable=self.value_var).pack()

        Button(self.root, text="Добавить", command=self.add_measurement).pack(pady=5)
        Button(self.root, text="Удалить", command=self.delete_selected).pack(pady=5)

        Label(self.root, text="Путь файла:").pack()
        self.file_var = StringVar()
        Entry(self.root, textvariable=self.file_var).pack()

        Button(self.root, text="Открыть файл", command=self.open_file).pack(pady=5)

    def _populate_tree(self):
        for m in self.measurements:
            self.tree.insert('', END, values=self._to_tuple(m))

    def _clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _to_tuple(self, m):
        return (m.date.strftime("%Y.%m.%d"), m.color, m.type_measure, m.location, f"{m.value:.2f}")

    def add_measurement(self):
        try:
            year, month, day = map(int, self.date_var.get().split('.'))
            date_ = date(year, month, day)
            color = self.color_var.get()
            type_ = self.type_var.get()
            location = self.location_var.get()
            value = float(self.value_var.get())

            m = TemperatureMeasurement(date_, color, type_, location, value)
            
            self.measurements.append(m)
            self.tree.insert('', END, values=self._to_tuple(m))

        except Exception as e:
            msgbox.showerror("Ошибка", f"Неверный ввод: {e}")

    def delete_selected(self):
        for item in self.tree.selection():
            index = self.tree.index(item)
            self.tree.delete(item)
            del self.measurements[index]

    def open_file(self):
        try:
            filename = self.file_var.get()
            self.measurements = self.repository.load_from_file(filename)

            self._clear_tree()
            self._populate_tree()
        except Exception:
            msgbox.showerror("Ошибка", "Неверный путь файла!")