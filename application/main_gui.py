import os
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, QAction, QVBoxLayout, QWidget, QStatusBar,
                             QMessageBox, QLabel)
from PyQt5.QtCore import Qt

from file_reader import FileLoaderThread
from plot_data import plot_strain_distance, plot_strain_time
from analyse_data import AnalyseData
from data_selector import DataSelector


class StressMeasurementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_selector = None
        self.plot_time_action = None
        self.plot_distance_action = None
        self.select_data_area_action = None
        self.loader_thread = None
        self.centralWidget = None
        self.file_path_label = None
        self.statusBar = None
        self.initUI()
        self.file_path = None
        self.distance = None
        self.strain = None
        self.time = None

    # *** GUI ***
    def initUI(self):
        self.setWindowTitle("Stress Measurement Viewer")
        self.setGeometry(100, 100, 400, 150)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Add a label to show the full file path in the central widget
        self.file_path_label = QLabel("No file loaded", self)
        self.file_path_label.setAlignment(Qt.AlignCenter)

        # Layout to hold the label in the central widget
        layout = QVBoxLayout()
        layout.addWidget(self.file_path_label)
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(layout)
        self.setCentralWidget(self.centralWidget)

        # MENU
        # Store references to menus
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)  # Ensure menu bar is part of the window (important for macOS)

        # Create menus
        self.file_menu = self.menubar.addMenu("File")
        self.edit_menu = self.menubar.addMenu("Edit")
        self.plot_menu = self.menubar.addMenu("Plot")
        self.help_menu = self.menubar.addMenu("Help")

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.openFile)
        self.file_menu.addAction(open_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        # Create actions
        self.edit_data_area_action = QAction("Data Area", self)
        self.edit_data_area_action.triggered.connect(self.edit_data_area)
        self.edit_menu.addAction(self.edit_data_area_action)

        self.plot_distance_action = QAction("Strain vs Distance", self)
        self.plot_distance_action.triggered.connect(self.plotStrainDistance)
        self.plot_menu.addAction(self.plot_distance_action)

        self.plot_time_action = QAction("Strain vs Time", self)
        self.plot_time_action.triggered.connect(self.plotStrainTime)
        self.plot_menu.addAction(self.plot_time_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.openAbout)
        self.help_menu.addAction(about_action)

        # Store all actions for easy enabling/disabling
        self.menu_actions = [
            self.edit_data_area_action,
            self.plot_distance_action,
            self.plot_time_action
        ]

        # Initially disable menu actions
        self.setMenuState(False)

    def setMenuState(self, enabled):
        """Enable or disable menu actions based on data availability."""
        for action in self.menu_actions:
            action.setEnabled(enabled)

        # Force UI update (important for macOS)
        self.menubar.repaint()
        QApplication.processEvents()

    # *** READER ***
    def onDataLoaded(self, distance, strain, time, file_path):
        self.distance = distance
        self.strain = strain
        self.time = time
        self.file_path = file_path

        self.statusBar.showMessage(f"Opened: {os.path.basename(file_path)}")
        self.file_path_label.setText(f"File: {os.path.basename(file_path)}")

        self.setMenuState(True)  # Enable menu actions

    def openFile(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open TSV File", "", "TSV Files (*.tsv);;All Files (*)",
                                                   options=options)
        if file_path:
            self.statusBar.showMessage("Processing...")
            self.loader_thread = FileLoaderThread(file_path)
            self.loader_thread.dataLoaded.connect(self.onDataLoaded)
            self.loader_thread.start()
        else:
            self.setMenuState(False)  # Disable menu actions if no file is selected

    # *** EDIT ***
    def edit_data_area(self):
        """Opens Data Selector window."""
        if self.distance is None or self.strain is None:
            return

        analyser = AnalyseData(self.distance, self.strain, self.time)  # Create instance
        self.data_selector = DataSelector(self.distance.size, self.strain.shape[1], self.strain.shape[0], analyser,
                                          self)  # Pass it
        self.data_selector.show()

    def update_data_area(self, start, end):
        """Updates data when 'Set Data Area' is clicked."""
        analyser = AnalyseData(self.distance, self.strain, self.time)
        analyser.select_data_area(start, end)
        self.distance, self.strain, self.time = analyser.distance, analyser.strain, analyser.time

    # *** PLOT ***
    def plotStrainDistance(self):
        if self.distance is None or self.strain is None:
            return
        plot_strain_distance(self.distance, self.strain)

    def plotStrainTime(self):
        if self.time is None or self.strain is None:
            return
        plot_strain_time(self.distance, self.time, self.strain)

    # *** ABOUT ***
    def openAbout(self):
        msg = QMessageBox()
        msg.setWindowTitle("About")
        # Add title and bold formatting
        msg.setText(
            "<h1>Stress Measurement Viewer</h1><p><b>This application was developed by Petr Balik for stress measurement analysis & visualization.</b></p><p>App version: 1.0</p>")
        msg.setTextFormat(Qt.RichText)  # Enable rich text format
        msg.show()
        msg.exec()
