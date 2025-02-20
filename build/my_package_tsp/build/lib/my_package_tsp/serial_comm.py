# serial_comm.py

import serial

# 串口配置（使用宏定义进行规范）
SERIAL_PORT = '/dev/ttyS3'  # 串口设备路径
BAUD_RATE = 115200  # 串口波特率
TIMEOUT = 0  # 超时时间

class SerialComm:
    def __init__(self, port=SERIAL_PORT, baud_rate=BAUD_RATE, timeout=TIMEOUT):
        """
        初始化串口通信对象
        
        :param port: 串口设备路径
        :param baud_rate: 串口波特率
        :param timeout: 读取串口数据的超时时间
        """
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None

    def open(self):
        """
        打开串口
        """
        if self.ser is None or not self.ser.is_open:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            if self.ser.is_open:
                print(f"串口 {self.port} 已打开，波特率：{self.baud_rate}")
            else:
                print(f"无法打开串口 {self.port}")
    
    def send(self, data):
        """
        向串口发送数据
        
        :param data: 需要发送的数据
        """
        if self.ser is None or not self.ser.is_open:
            print("串口未打开")
            return
        
        self.ser.write(data.encode('utf-8'))  # 将字符串编码为字节发送
        
    def close(self):
        """
        关闭串口
        """
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"串口 {self.port} 已关闭")

