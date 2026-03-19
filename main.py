import logging
from tkinter import Tk
from model import MeasurementParser, MeasurementRepository
from view import TemperatureApp


logging.basicConfig(
    filename="app.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


if __name__ == "__main__":
    parser = MeasurementParser()
    repo = MeasurementRepository(parser)

    root = Tk()
    app = TemperatureApp(root, repo)
    root.mainloop()