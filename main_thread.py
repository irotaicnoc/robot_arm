# import time
# import warnings
# import threading

import args
# from oled import OLED
# from light import Light
import global_constants as gc
# from joystick import Joystick
from robot_body import RobotBody
from robot_head import RobotHead
# from gpio_pin_control import GpioLed


def main_loop(**kwargs):
    parameters = args.import_args(yaml_path=gc.CONFIG_FOLDER_PATH + 'main_thread.yaml', **kwargs)

    robot_body = RobotBody(address=parameters['address'], verbose=parameters['verbose'])
    robot_head = RobotHead()
    # LIGHTS
    # gpio_led = GpioLed()

    # # JOYSTICK
    # joystick_kwargs = {
    #     'robot_body': robot_body,
    #     'robot_head': robot_head,
    #     # 'gpio_led': gpio_led,
    #     'verbose': parameters['verbose'],
    # }
    # thread_joystick = threading.Thread(target=task_joystick, name='task_joystick', kwargs=joystick_kwargs)
    # thread_joystick.start()

    # screen_kwargs = {
    #     'robot_body': robot_body,
    #     'robot_head': robot_head,
    #     'verbose': parameters['verbose'],
    # }
    # # "daemon = True" means that when this is the only thread running, (or when only other daemonic threads remain)
    # # the containing thread (the main) will exit. The oled screen is daemonic, if there are no more joystick and/or
    # # vision_agent left, then the main can stop.
    # thread_screen = threading.Thread(target=task_screen, name='task_screen', kwargs=screen_kwargs, daemon=True)
    # thread_screen.start()

    # notify the robot is ready
    robot_body.set_beep(50)


# # USB gamepad
# def task_joystick(**kwargs):
#     js = Joystick(**kwargs)
#     while True:
#         state = js.joystick_handle()
#         if state != js.STATE_OK:
#             if state == js.STATE_KEY_BREAK:
#                 break
#             time.sleep(1)
#             js.reconnect()


# # oled screen
# def task_screen(**kwargs):
#     try:
#         oled = OLED(clear=False, **kwargs)
#         while True:
#             state = oled.main_program()
#             oled.clear(True)
#             if state:
#                 del oled
#                 print('---OLED CLEARED!---')
#                 break
#             time.sleep(1)
#     except KeyboardInterrupt as e:
#         del oled
#         print('Oled Error:')
#         print(e)
#         print(e.__traceback__)


if __name__ == '__main__':
    main_loop()
