# Python Libraries
import csv
import time
from datetime import datetime
from typing import List  # To define the type of lists

##

class AcousticsDataRecordLib:
    def __init__(self, ROS2_PACKAGE_DIRECTORY: str = "") -> None:
        # Global variables for .csv file manipulation ----------
        # Get the path for the directory where we will store our data
        self.acoustics_data_directory = ROS2_PACKAGE_DIRECTORY + "acoustics_data/"   

        timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
        data_file_name = "acoustics_data_" + timestamp + ".csv"
        self.data_file_location = self.acoustics_data_directory + data_file_name     

        self.csv_headers = [
            "Time",
            "Hydrophone1",
            "Hydrophone2",
            "Hydrophone3",
            "Hydrophone4",
            "Hydrophone5",
            "FilterResponse",
            "FFT",
            "Peaks",
            "TDOA",
            "Position",
        ]

        # Make new .csv file for logging blackbox data ----------
        with open(self.data_file_location, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.csv_headers)

    # Methods for external uses ----------
    def log_data_to_csv_file(
        self,
        hydrophone1: List[int] = [0],
        hydrophone2: List[int] = [0],
        hydrophone3: List[int] = [0],
        hydrophone4: List[int] = [0],
        hydrophone5: List[int] = [0],
        filter_response: List[int] = [0],
        fft: List[int] = [0],
        peaks: List[int] = [0],
        tdoa: List[float] = [0.0],
        position: List[float] = [0.0],
    ) -> None:
        # Get current time in hours, minutes, seconds, and milliseconds
        current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        # Write to .csv file
        with open(self.data_file_location, mode="a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                [
                    current_time,
                    hydrophone1,
                    hydrophone2,
                    hydrophone3,
                    hydrophone4,
                    hydrophone5,
                    filter_response,
                    fft,
                    peaks,
                    tdoa,
                    position,
                ]
            )
