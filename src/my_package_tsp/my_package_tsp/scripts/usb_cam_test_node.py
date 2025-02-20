# usb_cam_test_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from usb_cam import UsbCam

class UsbCamTestNode(Node):
    def __init__(self):
        super().__init__('usb_cam_test_node')
        self.declare_parameter('video_device', '/dev/video9')  # 默认设备路径
        video_device = self.get_parameter('video_device').get_parameter_value().string_value

        self.get_logger().info(f'Using video device: {video_device}')
        self.usb_cam = UsbCam(self, video_device)
        self.usb_cam.create_publisher(Image, 'image_raw', 10)

def main():
    rclpy.init()
    node = UsbCamTestNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

