import args

import global_constants as gc


class RobotHead:
    def __init__(self, **kwargs):
        parameters = args.import_args(
            yaml_path=gc.CONFIG_FOLDER_PATH + 'robot_head.yaml',
            **kwargs,
        )
        # hotspot and ROS2 parameters
        self.hotspot_status = 'inactive'
        self.hotspot_ip = parameters['hotspot_ip']
        self.ros2_status = 'inactive'

        # motion parameters
        self.speed_coefficient = parameters['speed_coefficient']
        self.verbose = parameters['verbose']

    def increase_speed_coefficient(self):
        self.speed_coefficient = min(1.0, self.speed_coefficient + 0.1)
        if self.verbose >= 2:
            print(f'Speed coefficient: {self.speed_coefficient}')

    def decrease_speed_coefficient(self):
        self.speed_coefficient = max(0.1, self.speed_coefficient - 0.1)
        if self.verbose >= 2:
            print(f'Speed coefficient: {self.speed_coefficient}')
