from pylablib.devices.Thorlabs import kinesis

devices = kinesis.list_kinesis_devices()
print(devices)
motor = kinesis.KinesisMotor(devices[0][0], scale="stage")
# print(motor.get_device_info())
# print(motor.get_scale_units())
# print(motor.get_scale())
# print(motor.get_stage())
#print(motor.get_limit_switch_parameters(scale=True))
print(motor.get_full_info())
motor.move_by(distance=-1)