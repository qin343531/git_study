# usb_camera_example/launch/usb_cam_launch.py

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package_tsp',
            executable='usb_cam_test_node',
            name='usb_cam_test',
            output='screen',
            parameters=[{'video_device': '/dev/video9'}],  # 根据你的设备路径调整
        ),
    ])

