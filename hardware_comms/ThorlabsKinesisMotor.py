from hardware_comms.device_interfaces import Motor
from pylablib.devices.Thorlabs import KinesisMotor
from utilities import T_fs_to_dist_um, dist_um_to_T_fs
class ThorlabsKinesisMotor(Motor):
    def __init__(self, serial_no: int):
        # motor should have mm units
        self.motor = KinesisMotor(serial_no, scale="stage")
        self._pos_um : float
        #TODO check scale
    
    @property
    def pos_um(self):
        # default units are (m)
        if self.pos_um is None:
            self.pos_um = 1e6 * self.motor.get_position()
            return self._pos_um
        else:
            return self._pos_um

    @pos_um.setter
    def pos_um(self, loc_um):
        # setting the motor position tells the motor to move in absolute mode
        # and is non-blocking

        # default units are (m) 
        loc_m = loc_um * 1e-6 
        self.motor.move_to(loc_m, scale=True)
        self.pos_um = loc_um


    # TODO
    @property
    def pos_fs(self):
        # pos_fs is taken from pos_um and T0_um
        return dist_um_to_T_fs(self.pos_um - self.T0_um)

    @pos_fs.setter
    def pos_fs(self, value_fs):
        # pos_fs is taken from pos_um, so just set pos_um
        # setting pos_um moves the motor
        self.pos_um = T_fs_to_dist_um(value_fs) + self.T0_um

    def move_by_fs(self, value_fs):
        # obtain the distance to move in micron and meters
        value_um = T_fs_to_dist_um(value_fs)
        value_mm = value_um * 1e-3

        # move the motor to the new position and update the position in micron
        self.motor.move_by(value_mm)

    def move_by_um(self, dist_um):
        dist_m = dist_um * 1e-6

        # move the motor to the new position and update the position in micron
        self.motor.move_by(distance=dist_m)
        self.pos_um = self.pos_um + dist_um

    def value_exceeds_limits(self, value_um):
        predicted_pos_um = value_um + self.pos_um
        max_limit_um = self.motor.max_pos_mm * 1e3
        min_limit_um = self.motor.min_pos_mm * 1e3
        buffer_um = self._safety_buffer_mm * 1e3

        if (predicted_pos_um < min_limit_um + buffer_um) or (
            predicted_pos_um > max_limit_um - buffer_um
        ):
            raise_error(self.error_window, "too close to stage limits (within 1um)")
            return True
        else:
            return False
