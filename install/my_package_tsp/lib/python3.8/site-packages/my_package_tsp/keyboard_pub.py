import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys
import termios
import tty

class KeyboardPublisher(Node):
    def __init__(self):
        super().__init__('keyboard_publisher')
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        self.get_logger().info('Keyboard Publisher Node is running...')
    
    def read_key(self):
        # 读取单个字符而不需要按下回车
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def keyboard_input_loop(self):
        while rclpy.ok():
            key = self.read_key()  # 获取输入的字符
            if key == 'q':  # 如果按下 'q' 就退出
                self.get_logger().info("Exiting keyboard publisher...")
                break
            msg = String()
            msg.data = key
            self.publisher_.publish(msg)
            self.get_logger().info(f'Published: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardPublisher()
    node.keyboard_input_loop()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

