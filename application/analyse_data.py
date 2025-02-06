import numpy as np


class AnalyseData:
    def __init__(self, distance, strain, time, start_spin=None, end_spin=None):
        self.strain = strain
        self.distance = distance
        self.time = time
        self.start_spin = start_spin
        self.end_spin = end_spin

    def find_peak_area(self, baseline_spin, min_delta_spin, max_delta_spin, time_id):
        start_index = None
        end_index = None

        for i in range(1, len(self.strain[time_id])):  # Start from 1 to avoid out-of-bounds
            if (
                    np.abs(self.strain[time_id][i]) > baseline_spin and
                    min_delta_spin < np.abs(self.strain[time_id][i] - self.strain[time_id][i - 1]) < max_delta_spin
            ):
                if start_index is None:
                    start_index = i  # First valid point
                end_index = i  # Continuously update end_index

        if start_index is not None and end_index is not None:
            start_distance = self.distance[start_index]
            end_distance = self.distance[end_index]
            print(
                f"START: index: {start_index}, distance: {start_distance}, END: index: {end_index}, distance: {end_distance}")  # Debugging output

            # Update the spinboxes
            if self.start_spin is not None:
                self.start_spin.setValue(start_index)
            if self.end_spin is not None:
                self.end_spin.setValue(end_index)
        else:
            print("No valid peak area found.")  # Debugging print

    def calculate_strain_max(self):
        strain_mean = []

        for i in range(0, self.strain.shape[0]):
            abs_mean_value = np.abs(np.nanmean(self.strain[i]))
            strain_mean.append((i, abs_mean_value))

        # Sort the list by the value (second element of the tuple) in descending order
        strain_mean = sorted(strain_mean, key=lambda x: x[1], reverse=True)[:3]

        # Print the top 3 highest values along with their iteration index
        print("Top 3 highest values and their corresponding indices:")
        for index, value in strain_mean:
            print(f"Index: {index}, Value: {value}")

    def select_data_area(self, start, end):
        """Trims distance, strain, and time based on start and end indices."""
        if start >= end or start < 0 or end > self.distance.size:
            print("Invalid selection range.")
            return

        self.distance = self.distance[start:end]
        self.strain = self.strain[:, start:end]  # Keep all time steps
        self.time = self.time[start:end]  # Trim time accordingly

        print(f"Data trimmed: New size = {self.distance.size}")
