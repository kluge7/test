#!/usr/bin/env python3
# Import libraries
import numpy
import smbus2


class ThrusterInterfaceAUVDriver:
    def __init__(
        self,
        i2c_bus=1,
        pico_i2c_address=0x21,
        system_operational_voltage=16.0,
        ros2_package_name_for_thruster_datasheet="",
        thruster_mapping=[7, 6, 5, 4, 3, 2, 1, 0],
        thruster_direction=[1, 1, 1, 1, 1, 1, 1, 1],
        thruster_pwm_offset=[0, 0, 0, 0, 0, 0, 0, 0],
        pwm_min=[1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100],
        pwm_max=[1900, 1900, 1900, 1900, 1900, 1900, 1900, 1900],
        coeffs=None,
    ) -> None:
        # Initialice the I2C communication
        self.bus = None
        try:
            self.bus = smbus2.SMBus(i2c_bus)
        except Exception as errorCode:
            print(f"ERROR: Failed connection I2C bus nr {self.bus}: {errorCode}")
        self.PICO_I2C_ADDRESS = pico_i2c_address

        # Set mapping, direction and offset for the thrusters
        self.THRUSTER_MAPPING = thruster_mapping
        self.THRUSTER_DIRECTION = thruster_direction
        self.THRUSTER_PWM_OFFSET = thruster_pwm_offset
        self.PWM_MIN = pwm_min
        self.PWM_MAX = pwm_max

        # Convert SYSTEM_OPERATIONAL_VOLTAGE to a whole even number to work with
        # This is because we have multiple files for the behaviour of the thrusters depending on the voltage of the drone
        if system_operational_voltage < 11.0:
            self.SYSTEM_OPERATIONAL_VOLTAGE = 10
        elif system_operational_voltage < 13.0:
            self.SYSTEM_OPERATIONAL_VOLTAGE = 12
        elif system_operational_voltage < 15.0:
            self.SYSTEM_OPERATIONAL_VOLTAGE = 14
        elif system_operational_voltage < 17.0:
            self.SYSTEM_OPERATIONAL_VOLTAGE = 16
        elif system_operational_voltage < 19.0:
            self.SYSTEM_OPERATIONAL_VOLTAGE = 18
        elif system_operational_voltage >= 19.0:
            self.SYSTEM_OPERATIONAL_VOLTAGE = 20

        # Get the full path to the ROS2 package this file is located at
        self.ROS2_PACKAGE_NAME_FOR_THRUSTER_DATASHEET = (
            ros2_package_name_for_thruster_datasheet
        )

        self.coeffs = coeffs

    def _interpolate_forces_to_pwm(self, thruster_forces_array) -> list:
        # Read the important data from the .csv file
        # thrusterDatasheetFileData = pandas.read_csv(
        #     f"{self.ROS2_PACKAGE_NAME_FOR_THRUSTER_DATASHEET}/resources/T200-Thrusters-{self.SYSTEM_OPERATIONAL_VOLTAGE}V.csv",
        #     usecols=[" PWM (µs)", " Force (Kg f)"],
        # )

        # Convert Newtons to Kg as Thruster Datasheet is in Kg format
        for i, thruster_forces in enumerate(thruster_forces_array):
            thruster_forces_array[i] = thruster_forces / 9.80665

        # Select the appropriate pair of coeffs based on the operational voltage
        left_coeffs = self.coeffs[self.SYSTEM_OPERATIONAL_VOLTAGE]["LEFT"]
        right_coeffs = self.coeffs[self.SYSTEM_OPERATIONAL_VOLTAGE]["RIGHT"]

        # Calculate the interpolated PWM values using the polynomial coefficients
        interpolated_pwm = []
        for i, force in enumerate(thruster_forces_array):
            if force < 0:
                # use the left coefficients
                pwm = numpy.polyval(left_coeffs, force)
            elif force == 0.00:
                pwm = 1500 - self.THRUSTER_PWM_OFFSET[i]
            else:
                # use the right coefficients
                pwm = numpy.polyval(right_coeffs, force)

            interpolated_pwm.append(pwm)

        # Convert PWM signal to integers as they are interpolated and can have floats
        interpolated_pwm = [int(pwm) for pwm in interpolated_pwm]

        return interpolated_pwm

    def _send_data_to_escs(self, thruster_pwm_array) -> None:
        i2c_data_array = []

        # Divide data into bytes as I2C only sends bytes
        # We have 8 values of 16 bits
        # Convert them to 16 values of 8 bits (ie 1 byte)
        for i in range(len(thruster_pwm_array)):
            msb = (thruster_pwm_array[i] >> 8) & 0xFF
            lsb = (thruster_pwm_array[i]) & 0xFF
            i2c_data_array.extend([msb, lsb])

        # Send the whole array through I2C
        # OBS!: Python adds an extra byte at the start that the Microcotroller that is receiving this has to handle
        self.bus.write_i2c_block_data(self.PICO_I2C_ADDRESS, 0, i2c_data_array)

    def drive_thrusters(self, thruster_forces_array) -> list:
        # Apply thruster mapping and direction
        thruster_forces_array = [
            thruster_forces_array[i] * self.THRUSTER_DIRECTION[i]
            for i in self.THRUSTER_MAPPING
        ]

        # Convert Forces to PWM
        thruster_pwm_array = self._interpolate_forces_to_pwm(thruster_forces_array)

        # Apply thruster offset
        for ESC_channel, thruster_pwm in enumerate(thruster_pwm_array):
            thruster_pwm_array[ESC_channel] = (
                thruster_pwm + self.THRUSTER_PWM_OFFSET[ESC_channel]
            )

        # Apply thruster offset and limit PWM if needed
        for ESC_channel in range(len(thruster_pwm_array)):
            # Clamping pwm signal in case it is out of range
            if thruster_pwm_array[ESC_channel] < self.PWM_MIN[ESC_channel]:  # To small
                thruster_pwm_array[ESC_channel] = self.PWM_MIN[ESC_channel]
            elif thruster_pwm_array[ESC_channel] > self.PWM_MAX[ESC_channel]:  # To big
                thruster_pwm_array[ESC_channel] = self.PWM_MAX[ESC_channel]

        # Send data through I2C to the microcontroller that then controls the ESC and extension the thrusters
        try:
            self._send_data_to_escs(thruster_pwm_array)
        except Exception as errorCode:
            print(f"ERROR: Failed to send PWM values: {errorCode}")

        return thruster_pwm_array
