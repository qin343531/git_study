# serial_publisher.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from my_package_tsp.serial_comm import SerialComm  # 导入串口通信模块

class SerialPublisher(Node):
    def __init__(self):
        super().__init__('serial_publisher')
        
        # 创建串口通信对象
        self.serial_comm = SerialComm()
        self.serial_comm.open()  # 打开串口

        # 创建订阅者
        self.subscription = self.create_subscription(
            String,
            'chatter',  # 订阅 "chatter" 话题
            self.listener_callback,
            10)
        self.subscription  # 保持订阅者对象

    def listener_callback(self, msg):
        """
        回调函数，接收到消息时调用
        
        :param msg: 接收到的消息
        """
        self.get_logger().info(f'Received: "{msg.data}"')
        
        # 将接收到的消息发送到串口
        self.serial_comm.send(msg.data)

    def destroy_node(self):
        """关闭串口通信"""
        self.serial_comm.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SerialPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

