import os

import global_constants as gc
from kill_process import kill_process_


def pretty_print_dict(data, _level: int = 0) -> None:
    if isinstance(data, dict):
        if _level > 0:
            print()
        for key in data:
            for i in range(_level + 1):
                print('\t', end='')
            print(f'{key}: ', end='')
            pretty_print_dict(data[key], _level=_level + 1)
    else:
        print(data)


def activate_hotspot(hotspot_ip: str, verbose: int = 0):
    if verbose >= 1:
        print('Starting Hotspot...', end='')
    os.system('sleep 2')
    os.system('systemctl stop wpa_supplicant')
    os.system('ip addr flush dev wlan0')
    os.system('sleep 0.5')
    os.system('ifconfig wlan0 down')
    os.system('sleep 1')
    os.system('ifconfig wlan0 up')
    os.system(f'hostapd -B {gc.MAIN_FOLDER_PATH}network_connections/hostapd.conf')
    os.system(f'ifconfig wlan0 {hotspot_ip} netmask 255.255.255.0')
    os.system('systemctl start isc-dhcp-server')
    if verbose >= 1:
        print('Done.')


def deactivate_hotspot(verbose: int = 0):
    if verbose >= 1:
        print('Stopping Hotspot...', end='')
    kill_process_(process_name='hostapd', verbose=verbose)
    os.system('systemctl stop isc-dhcp-server')
    os.system('ip addr flush dev wlan0')
    os.system('sleep 0.5')
    os.system('ifconfig wlan0 down')
    os.system('sleep 1')
    os.system('ifconfig wlan0 up')
    os.system('systemctl start wpa_supplicant')
    if verbose >= 1:
        print('Done.')


# def activate_ros2(verbose: int = 0):
#     if verbose >= 1:
#         print('Starting ROS2...', end='')
#     # os.system(f'{gc.SCRIPT_FOLDER_PATH}start_ros2.sh')
#     os.system('gnome-terminal -- bash -c "source /opt/ros/foxy/setup.bash;cd /root/marco_ros2_ws/;'
#               'source install/local_setup.bash;ros2 launch ros_tcp_endpoint endpoint_launch.py;exec bash"')
#     # os.system('wait')
#     # os.system('exit 0')
#     if verbose >= 1:
#         print('Done.')
#
#
# def deactivate_ros2(verbose: int = 0):
#     # TODO: it does not really kill the process in the separate console
#     if verbose >= 1:
#         print('Stopping ROS2...', end='')
#     kill_process_(process_name='ros2', verbose=verbose)
#     if verbose >= 1:
#         print('Done.')
