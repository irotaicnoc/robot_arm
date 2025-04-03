import time
import smbus


class RobotBody(object):

    def __init__(self, address, verbose: int = 0):
        self.address = address
        self.verbose = verbose
        self.bus = smbus.SMBus(1)

    # Set the bus servo angle interface: id: 1-6 (0 is to send 6 servos) angle: 0-180
    # Set the angle to which the servo should move
    def arm_serial_servo_write(self, id, angle, duration):
        if id == 0:  # This is the control of all servos

            self.arm_serial_servo_write6(angle, angle, angle, angle, angle, angle, duration)
        elif id == 2 or id == 3 or id == 4:  # Opposite angle to reality
            angle = 180 - angle
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            # pos = ((pos << 8) & 0xff00) | ((pos >> 8) & 0xff)
            value_h = (pos >> 8) & 0xFF
            value_l = pos & 0xFF
            time_h = (duration >> 8) & 0xFF
            time_l = duration & 0xFF
            try:
                self.bus.write_i2c_block_data(self.address, 0x10 + id, [value_h, value_l, time_h, time_l])
            except:
                print('arm_serial_servo_write I2C error')
        elif id == 5:
            pos = int((3700 - 380) * (angle - 0) / (270 - 0) + 380)
            # pos = ((pos << 8) & 0xff00) | ((pos >> 8) & 0xff)
            value_h = (pos >> 8) & 0xFF
            value_l = pos & 0xFF
            time_h = (duration >> 8) & 0xFF
            time_l = duration & 0xFF
            try:
                self.bus.write_i2c_block_data(self.address, 0x10 + id, [value_h, value_l, time_h, time_l])
            except:
                print('arm_serial_servo_write I2C error')
        else:
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            # pos = ((pos << 8) & 0xff00) | ((pos >> 8) & 0xff)
            value_h = (pos >> 8) & 0xFF
            value_l = pos & 0xFF
            time_h = (duration >> 8) & 0xFF
            time_l = duration & 0xFF
            try:
                self.bus.write_i2c_block_data(self.address, 0x10 + id, [value_h, value_l, time_h, time_l])
            except:
                print('arm_serial_servo_write I2C error')

    # Set any bus servo angle interface: id: 1-250 (0 is group sending) angle: 0-180 means 900 3100 0 - 180
    def arm_serial_servo_write_any(self, id, angle, duration):
        if id != 0:
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            value_h = (pos >> 8) & 0xFF
            value_l = pos & 0xFF
            time_h = (duration >> 8) & 0xFF
            time_l = duration & 0xFF
            try:
                self.bus.write_i2c_block_data(self.address, 0x19, [id & 0xff, value_h, value_l, time_h, time_l])
            except:
                print('arm_serial_servo_write_any I2C error')
        elif id == 0:  # This is the control of all servos
            pos = int((3100 - 900) * (angle - 0) / (180 - 0) + 900)
            # pos = ((pos << 8) & 0xff00) | ((pos >> 8) & 0xff)
            value_h = (pos >> 8) & 0xFF
            value_l = pos & 0xFF
            time_h = (duration >> 8) & 0xFF
            time_l = duration & 0xFF
            try:
                self.bus.write_i2c_block_data(self.address, 0x17, [value_h, value_l, time_h, time_l])
            except:
                print('arm_serial_servo_write_any I2C error')

    # Set the bus servo neutral offset with one key, move it to the neutral position after power-on, and then
    # send the following function, id: 1-6 (set), 0 (restore initial)
    def arm_serial_servo_write_offset_switch(self, id):
        try:
            if 0 < id < 7:
                self.bus.write_byte_data(self.address, 0x1c, id)
            elif id == 0:
                self.bus.write_byte_data(self.address, 0x1c, 0x00)
                time.sleep(.5)
        except:
            print('arm_serial_servo_write_offset_switch I2C error')

    # Read the status of one-key setting of the bus servo's median offset, 0 means that the corresponding servo ID
    # cannot be found, 1 means success, 2 means failure out of range
    def arm_serial_servo_write_offset_state(self):
        try:
            self.bus.write_byte_data(self.address, 0x1b, 0x01)
            time.sleep(.001)
            state = self.bus.read_byte_data(self.address, 0x1b)
            return state
        except:
            print('arm_serial_servo_write_offset_state I2C error')
        return None

    # Set the bus servo angle interface: array
    def arm_serial_servo_write6_array(self, joints, duration):
        s1, s2, s3, s4, s5, s6 = joints[0], joints[1], joints[2], joints[3], joints[4], joints[5]
        if s1 > 180 or s2 > 180 or s3 > 180 or s4 > 180 or s5 > 270 or s6 > 180:
            print("The parameter input range is not within 0-180!")
            return
        try:
            pos = int((3100 - 900) * (s1 - 0) / (180 - 0) + 900)
            value1_h = (pos >> 8) & 0xFF
            value1_l = pos & 0xFF

            s2 = 180 - s2
            pos = int((3100 - 900) * (s2 - 0) / (180 - 0) + 900)
            value2_h = (pos >> 8) & 0xFF
            value2_l = pos & 0xFF

            s3 = 180 - s3
            pos = int((3100 - 900) * (s3 - 0) / (180 - 0) + 900)
            value3_h = (pos >> 8) & 0xFF
            value3_l = pos & 0xFF

            s4 = 180 - s4
            pos = int((3100 - 900) * (s4 - 0) / (180 - 0) + 900)
            value4_h = (pos >> 8) & 0xFF
            value4_l = pos & 0xFF

            pos = int((3700 - 380) * (s5 - 0) / (270 - 0) + 380)
            value5_h = (pos >> 8) & 0xFF
            value5_l = pos & 0xFF

            pos = int((3100 - 900) * (s6 - 0) / (180 - 0) + 900)
            value6_h = (pos >> 8) & 0xFF
            value6_l = pos & 0xFF
            time_h = (duration >> 8) & 0xFF
            time_l = duration & 0xFF

            data = [value1_h, value1_l, value2_h, value2_l, value3_h, value3_l,
                    value4_h, value4_l, value5_h, value5_l, value6_h, value6_l]
            time_arr = [time_h, time_l]
            s_id = 0x1d
            self.bus.write_i2c_block_data(self.address, 0x1e, time_arr)
            self.bus.write_i2c_block_data(self.address, s_id, data)
        except:
            print('arm_serial_servo_write6 I2C error')

    # Set the bus servo angle interface: s1~S4 and s6: 0-180, S5: 0~270, duration is the running time
    def arm_serial_servo_write6(self, s1, s2, s3, s4, s5, s6, duration):
        if s1 > 180 or s2 > 180 or s3 > 180 or s4 > 180 or s5 > 270 or s6 > 180:
            print("The parameter input range is not within 0-180!")
            return
        try:
            pos = int((3100 - 900) * (s1 - 0) / (180 - 0) + 900)
            value1_h = (pos >> 8) & 0xFF
            value1_l = pos & 0xFF

            s2 = 180 - s2
            pos = int((3100 - 900) * (s2 - 0) / (180 - 0) + 900)
            value2_h = (pos >> 8) & 0xFF
            value2_l = pos & 0xFF

            s3 = 180 - s3
            pos = int((3100 - 900) * (s3 - 0) / (180 - 0) + 900)
            value3_h = (pos >> 8) & 0xFF
            value3_l = pos & 0xFF

            s4 = 180 - s4
            pos = int((3100 - 900) * (s4 - 0) / (180 - 0) + 900)
            value4_h = (pos >> 8) & 0xFF
            value4_l = pos & 0xFF

            pos = int((3700 - 380) * (s5 - 0) / (270 - 0) + 380)
            value5_h = (pos >> 8) & 0xFF
            value5_l = pos & 0xFF

            pos = int((3100 - 900) * (s6 - 0) / (180 - 0) + 900)
            value6_h = (pos >> 8) & 0xFF
            value6_l = pos & 0xFF
            time_h = (duration >> 8) & 0xFF
            time_l = duration & 0xFF

            data = [value1_h, value1_l, value2_h, value2_l, value3_h, value3_l,
                    value4_h, value4_l, value5_h, value5_l, value6_h, value6_l]
            time_arr = [time_h, time_l]
            s_id = 0x1d
            self.bus.write_i2c_block_data(self.address, 0x1e, time_arr)
            self.bus.write_i2c_block_data(self.address, s_id, data)
        except:
            print('arm_serial_servo_write6 I2C error')

    # Read the specified servo angle, id: 1-6 returns 0-180, read error returns None
    def arm_serial_servo_read(self, id):
        if id < 1 or id > 6:
            print("id must be 1 - 6")
            return None
        try:
            self.bus.write_byte_data(self.address, id + 0x30, 0x0)
            time.sleep(0.003)
            pos = self.bus.read_word_data(self.address, id + 0x30)
        except:
            print('arm_serial_servo_read I2C error')
            return None
        if pos == 0:
            return None
        pos = (pos >> 8 & 0xff) | (pos << 8 & 0xff00)
        # print(pos)
        if id == 5:
            pos = int((270 - 0) * (pos - 380) / (3700 - 380) + 0)
            if pos > 270 or pos < 0:
                return None
        else:
            pos = int((180 - 0) * (pos - 900) / (3100 - 900) + 0)
            if pos > 180 or pos < 0:
                return None
        if id == 2 or id == 3 or id == 4:
            pos = 180 - pos
        # print(pos)
        return pos

    # Read the bus servo angle, id: 1-250 return 0-180
    def arm_serial_servo_read_any(self, id):
        if id < 1 or id > 250:
            print("id must be 1 - 250")
            return None
        try:
            self.bus.write_byte_data(self.address, 0x37, id)
            time.sleep(0.003)
            pos = self.bus.read_word_data(self.address, 0x37)
        except:
            print('arm_serial_servo_read_any I2C error')
            return None
        # print(pos)
        pos = (pos >> 8 & 0xff) | (pos << 8 & 0xff00)
        # print(pos)
        pos = int((180 - 0) * (pos - 900) / (3100 - 900) + 0)
        # print(pos)
        return pos

    # Read the servo status, return 0xda normally, return 0x00 if no data is read, other values are servo error
    def arm_ping_servo(self, id):
        data = int(id)
        if data > 0 and data <= 250:
            reg = 0x38
            self.bus.write_byte_data(self.address, reg, data)
            time.sleep(.003)
            value = self.bus.read_byte_data(self.address, reg)
            times = 0
            while value == 0 and times < 5:
                self.bus.write_byte_data(self.address, reg, data)
                time.sleep(.003)
                value = self.bus.read_byte_data(self.address, reg)
                times += 1
                if times >= 5:
                    return None
            return value
        else:
            return None

    # Read the hardware version number
    def arm_get_hardware_version(self):
        try:
            self.bus.write_byte_data(self.address, 0x01, 0x01)
            time.sleep(.001)
            value = self.bus.read_byte_data(self.address, 0x01)
        except:
            print('arm_get_hardware_version I2C error')
            return None
        version = str(0) + '.' + str(value)
        # print(version)
        return version

    # Torque switch 1: open torque 0: close torque (can be broken)
    def arm_serial_set_torque(self, onoff):
        try:
            if onoff == 1:
                self.bus.write_byte_data(self.address, 0x1A, 0x01)
            else:
                self.bus.write_byte_data(self.address, 0x1A, 0x00)
        except:
            print('arm_serial_set_torque I2C error')

    # Set the number of the bus servo
    def arm_serial_set_id(self, id):
        try:
            self.bus.write_byte_data(self.address, 0x18, id & 0xff)
        except:
            print('arm_serial_set_id I2C error')

    # Set the current product color 1~6, the corresponding color of the RGB light is on
    def arm_product_select(self, index):
        try:
            self.bus.write_byte_data(self.address, 0x04, index & 0xff)
        except:
            print('arm_product_select I2C error')

    # Set the specified color of the RGB light
    def arm_rgb_set(self, red, green, blue):
        try:
            self.bus.write_i2c_block_data(self.address, 0x02, [red & 0xff, green & 0xff, blue & 0xff])
        except:
            print('arm_rgb_set I2C error')

    # Set K1 key mode, 0: default mode 1: learning mode
    def arm_button_mode(self, mode):
        try:
            self.bus.write_byte_data(self.address, 0x03, mode & 0xff)
        except:
            print('arm_button_mode I2C error')

    # Restart the driver board
    def arm_reset(self):
        try:
            self.bus.write_byte_data(self.address, 0x05, 0x01)
        except:
            print('arm_reset I2C error')

    # PWD servo control id: 1-6 (0 controls all servos) angle: 0-180
    def arm_pwm_servo_write(self, id, angle):
        try:
            if id == 0:
                self.bus.write_byte_data(self.address, 0x57, angle & 0xff)
            else:
                self.bus.write_byte_data(self.address, 0x50 + id, angle & 0xff)
        except:
            print('arm_pwm_servo_write I2C error')

    # clear action group
    def arm_clear_action(self):
        try:
            self.bus.write_byte_data(self.address, 0x23, 0x01)
            time.sleep(.5)
        except:
            print('arm_clear_action I2C error')

    # In learning mode, record the current action once
    def arm_action_study(self):
        try:
            self.bus.write_byte_data(self.address, 0x24, 0x01)
        except:
            print('arm_action_study I2C error')

    # action group running mode 0: Stop running 1: Single running 2: Cyclic running
    def arm_action_mode(self, mode):
        try:
            self.bus.write_byte_data(self.address, 0x20, mode & 0xff)
        except:
            print('arm_clear_action I2C error')

    # Read the number of saved action groups
    def arm_read_action_num(self):
        try:
            self.bus.write_byte_data(self.address, 0x22, 0x01)
            time.sleep(.001)
            num = self.bus.read_byte_data(self.address, 0x22)
            return num
        except:
            print('arm_read_action_num I2C error')

    # Turn on the buzzer, the default delay is 0xff, and the buzzer keeps ringing
    # delay=1~50, the buzzer will be automatically turned off after delay*100 milliseconds after the buzzer is turned
    # on, and the maximum delay time is 5 seconds.
    def set_beep(self, delay=0xff):
        try:
            if delay != 0:
                self.bus.write_byte_data(self.address, 0x06, delay & 0xff)
        except:
            print('set_beep I2C error')

    # turn off the buzzer
    def stop_beep(self):
        try:
            self.bus.write_byte_data(self.address, 0x06, 0x00)
        except:
            print('stop_beep I2C error')

    def bus_servo_control(self, id, num, duration=1000):
        try:
            # if num > 4000 or num < 96:
            #     print("bus_servo_control error, num must be [96, 4000]")
            #     return

            time_h = (duration >> 8) & 0xFF
            time_l = duration & 0xFF

            if id == 1 or id == 6:
                if num > 3100 or num < 900:
                    print("bus_servo_control error, num must be [900, 3100]")
                    return
                pos = int(num)
                value_h = (pos >> 8) & 0xFF
                value_l = pos & 0xFF
            elif id == 2 or id == 3 or id == 4:  # 与实际相反角度  Opposite angle to actual
                if num > 3100 or num < 900:
                    print("bus_servo_control error, num must be [900, 3100]")
                    return
                pos = int(3100 - num + 900)
                value_h = (pos >> 8) & 0xFF
                value_l = pos & 0xFF
            elif id == 5:
                if num > 4200 or num < 900:
                    print("bus_servo_control error, num must be [900, 4200]")
                    return
                pos = int(num - 514)
                value_h = (pos >> 8) & 0xFF
                value_l = pos & 0xFF
            else:
                print("bus_servo_control error, id must be [1, 6]")
                return
            self.bus.write_i2c_block_data(self.address, 0x10 + id, [value_h, value_l, time_h, time_l])
        except:
            print('bus_servo_control error')

    @staticmethod
    def _change_value(value):
        try:
            val = 3100 - int(value) + 900
            return int(val)
        except:
            return None

    def bus_servo_control_array6(self, array, duration=1000):
        try:
            if len(array) != 6:
                print("bus_servo_control_array6 input error")
                return

            s1, s2, s3, s4, s5, s6 = array[0], array[1], array[2], array[3], array[4], array[5]
            if s1 > 3100 or s2 > 3100 or s3 > 3100 or s4 > 3100 or s5 > 4200 or s6 > 3100:
                print("bus_servo_control_array6 input error")
                return
            elif s1 < 900 or s2 < 900 or s3 < 900 or s4 < 900 or s5 < 900 or s6 < 900:
                print("bus_servo_control_array6 input error")
                return

            pos = int(s1)
            value1_h = (pos >> 8) & 0xFF
            value1_l = pos & 0xFF

            s2 = self._change_value(s2)
            pos = int(s2)
            value2_h = (pos >> 8) & 0xFF
            value2_l = pos & 0xFF

            s3 = self._change_value(s3)
            pos = int(s3)
            value3_h = (pos >> 8) & 0xFF
            value3_l = pos & 0xFF

            s4 = self._change_value(s4)
            pos = int(s4)
            value4_h = (pos >> 8) & 0xFF
            value4_l = pos & 0xFF

            s5 = s5 - 514
            pos = int(s5)
            value5_h = (pos >> 8) & 0xFF
            value5_l = pos & 0xFF

            pos = int(s6)
            value6_h = (pos >> 8) & 0xFF
            value6_l = pos & 0xFF

            time_h = (duration >> 8) & 0xFF
            time_l = duration & 0xFF

            data = [value1_h, value1_l, value2_h, value2_l, value3_h, value3_l,
                    value4_h, value4_l, value5_h, value5_l, value6_h, value6_l]
            time_arr = [time_h, time_l]
            s_id = 0x1d
            self.bus.write_i2c_block_data(self.address, 0x1e, time_arr)
            self.bus.write_i2c_block_data(self.address, s_id, data)
        except:
            print('bus_servo_control_array6 I2C error')
