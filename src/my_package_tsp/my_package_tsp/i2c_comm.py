import smbus

# I2C 设备相关配置
I2C_BUS_NUMBER = 2        # 使用的 I2C 总线编号，i2c-2
DEVICE_ADDRESS = 0x68     # 设备地址
REG_STATUS = 0x00         # 设备状态寄存器
REG_CONTROL = 0x01        # 控制寄存器
REG_SENSOR_DATA = 0x02    # 假设有一个传感器数据寄存器

# 操作模式定义
WRITE_MODE = 0x00
READ_MODE = 0x01

class I2CDevice:
    def __init__(self, bus_number=I2C_BUS_NUMBER, device_address=DEVICE_ADDRESS):
        """
        初始化 I2C 设备对象
        :param bus_number: I2C 总线编号
        :param device_address: 设备地址
        """
        self.bus = smbus.SMBus(bus_number)  # 创建 I2C 总线实例
        self.device_address = device_address

    def write_byte(self, register, value):
        """
        向设备寄存器写入一个字节
        :param register: 寄存器地址
        :param value: 写入的字节值
        """
        try:
            self.bus.write_byte_data(self.device_address, register, value)
            print(f"Written {hex(value)} to register {hex(register)} of device {hex(self.device_address)}")
        except Exception as e:
            print(f"Error writing to device {hex(self.device_address)}: {e}")

    def read_byte(self, register):
        """
        从设备寄存器读取一个字节
        :param register: 寄存器地址
        :return: 读取到的字节值
        """
        try:
            value = self.bus.read_byte_data(self.device_address, register)
            print(f"Read {hex(value)} from register {hex(register)} of device {hex(self.device_address)}")
            return value
        except Exception as e:
            print(f"Error reading from device {hex(self.device_address)}: {e}")
            return None

    def close(self):
        """关闭 I2C 总线"""
        self.bus.close()
        print(f"I2C bus at {self.device_address} closed.")

# 上层功能实现：例如控制设备，读取数据等
def read_sensor_data(device):
    """
    从设备读取传感器数据
    :param device: I2C 设备实例
    :return: 传感器数据
    """
    sensor_data = device.read_byte(REG_SENSOR_DATA)
    if sensor_data is not None:
        print(f"Sensor data: {sensor_data}")
        return sensor_data
    return None

def control_device(device, control_value):
    """
    控制设备状态
    :param device: I2C 设备实例
    :param control_value: 控制信号
    """
    device.write_byte(REG_CONTROL, control_value)
