from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QSpinBox, QFrame
from matplotlib import pyplot as plt


class DataSelector(QDialog):
    def __init__(self, distance_size, strain_size, time_size ,analyser, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Data Selector")
        self.analyser = analyser  # Store reference to AnalyseData

        self.start_spin = QSpinBox()
        self.start_spin.setRange(0, distance_size)
        self.start_spin.setValue(0)
        self.start_spin.valueChanged.connect(self.check_range)

        self.end_spin = QSpinBox()
        self.end_spin.setRange(0, distance_size)
        self.end_spin.setValue(distance_size)
        self.end_spin.valueChanged.connect(self.check_range)

        self.select_data_area_button = QPushButton("Select Data Area")
        self.select_data_area_button.clicked.connect(self.data_area_selector)
        #self.select_data_area_button.setEnabled(True)  # Initially disabled?

        # Horizontal Separator
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setFrameShadow(QFrame.Sunken)

        self.time_spin = QSpinBox()
        self.time_spin.setRange(0, time_size-1)
        self.time_spin.setValue(time_size)
        self.find_time_button = QPushButton("Find time")
        self.find_time_button.clicked.connect(self.find_time_on_click)

        #Horizontal Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)

        self.baseline_spin = QSpinBox()
        self.baseline_spin.setRange(0, strain_size)
        self.baseline_spin.setValue(50)

        self.min_delta_spin = QSpinBox()
        self.min_delta_spin.setRange(0, strain_size)
        self.min_delta_spin.setValue(20)

        self.max_delta_spin = QSpinBox()
        self.max_delta_spin.setRange(0, strain_size)
        self.max_delta_spin.setValue(1000)

        self.find_area_button = QPushButton("Find Peak Area")
        self.find_area_button.clicked.connect(lambda: self.analyser.find_peak_area(
            self.baseline_spin.value(),
            self.min_delta_spin.value(),
            self.max_delta_spin.value(),
            self.time_spin.value()
        ))  # Connect button

        self.start_spin.repaint()
        self.end_spin.repaint()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Start Point:"))
        layout.addWidget(self.start_spin)
        layout.addWidget(QLabel("End Point:"))
        layout.addWidget(self.end_spin)
        layout.addWidget(self.select_data_area_button)  # Moved here
        layout.addWidget(separator)  # Horizontal line

        layout.addWidget(QLabel("Time:"))
        layout.addWidget(self.time_spin)
        layout.addWidget(self.find_time_button)
        layout.addWidget(separator1)

        layout.addWidget(QLabel("Baseline:"))
        layout.addWidget(self.baseline_spin)
        layout.addWidget(QLabel("Min Delta:"))
        layout.addWidget(self.min_delta_spin)
        layout.addWidget(QLabel("Max Delta:"))
        layout.addWidget(self.max_delta_spin)
        layout.addWidget(self.find_area_button)

        self.setLayout(layout)

    def check_range(self):
        """Enable/disable 'Set Data Area' based on spinbox values."""
        self.select_data_area_button.setEnabled(self.start_spin.value() < self.end_spin.value())

    def data_area_selector(self):
        """Passes selected values to parent."""
        plt.close('all')  # Close all open plots
        self.parent().update_data_area(self.start_spin.value(), self.end_spin.value())
        self.accept()

    def find_peak_area(self):
        """Call find_peak_area() from AnalyseData with user input."""
        baseline = self.baseline_spin.value()
        min_delta = self.min_delta_spin.value()
        max_delta = self.max_delta_spin.value()
        selected_time = self.time_spin.value()

        self.analyser.find_peak_area(baseline, min_delta, max_delta)  # Call function
        #self.analyse_data.find_peak_area(baseline, min_delta, max_delta)

    def find_time_on_click(self):
        """Call calculate_strain_max() from AnalyseData"""
        self.analyser.calculate_strain_max()