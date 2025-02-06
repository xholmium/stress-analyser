import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class FileLoaderThread(QThread):
    dataLoaded = pyqtSignal(np.ndarray, np.ndarray, np.ndarray, str)  # Signal to send loaded data

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        """Loads the file data in a separate thread."""
        try:
            data = np.genfromtxt(self.file_path, delimiter='\t', skip_header=31)
            data = np.delete(data, [1, 2], axis=1)
            distance = data[0, 1:]
            strain = data[1:, 1:]
            time = np.genfromtxt(self.file_path, delimiter='\t', skip_header=32, usecols=0, dtype='datetime64')
            self.dataLoaded.emit(distance, strain, time, self.file_path)  # Send data to main thread
        except Exception as e:
            print(f"Error loading file: {e}")
