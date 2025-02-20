import spidev
import time

# SPI设备类
class SPIDevice:
    def __init__(self, bus=0, device=0, max_speed_hz=50000, mode=0b00):
        """
        初始化SPI设备
        :param bus: SPI总线号，通常为0或1
        :param device: 设备编号，通常为0或1
        :param max_speed_hz: SPI最大时钟频率
        :param mode: SPI模式（0, 1, 2, 3）
        """
        self.bus = bus
        self.device = device
        self.max_speed_hz = max_speed_hz
        self.mode = mode

        # 初始化SPI设备
        self.spi = spidev.SpiDev()
        self.spi.open(self.bus, self.device)  # 打开SPI设备
        self.spi.max_speed_hz = self.max_speed_hz  # 设置最大时钟频率
        self.spi.mode = self.mode  # 设置SPI模式

    def write_byte(self, data):
        """
        向SPI设备写入一个字节
        :param data: 要写入的字节数据
        """
        try:
            self.spi.xfer2([data])
            print(f"Written {hex(data)} to SPI device on bus {self.bus}, device {self.device}")
        except Exception as e:
            print(f"Error writing to SPI device: {e}")

    def write_bytes(self, data_list):
        """
        向SPI设备写入多个字节
        :param data_list: 要写入的字节数据列表
        """
        try:
            self.spi.xfer2(data_list)
            print(f"Written {data_list} to SPI device on bus {self.bus}, device {self.device}")
        except Exception as e:
            print(f"Error writing to SPI device: {e}")

    def read_byte(self):
        """
        从SPI设备读取一个字节
        :return: 读取到的字节数据
        """
        try:
            data = self.spi.readbytes(1)
            print(f"Read {hex(data[0])} from SPI device on bus {self.bus}, device {self.device}")
            return data[0]
        except Exception as e:
            print(f"Error reading from SPI device: {e}")
            return None

    def read_bytes(self, num_bytes):
        """
        从SPI设备读取多个字节
        :param num_bytes: 要读取的字节数
        :return: 读取到的字节数据列表
        """
        try:
            data = self.spi.readbytes(num_bytes)
            print(f"Read {data} from SPI device on bus {self.bus}, device {self.device}")
            return data
        except Exception as e:
            print(f"Error reading from SPI device: {e}")
            return None

    def close(self):
        """关闭SPI设备"""
        self.spi.close()
        print(f"SPI device on bus {self.bus}, device {self.device} closed.")


# 上层功能实现：例如控制SPI设备，读取数据等
def control_device(spi_device, data):
    """
    控制SPI设备（例如发送控制命令）
    :param spi_device: SPI设备实例
    :param data: 要发送的控制数据
    """
    spi_device.write_byte(data)


def read_sensor_data(spi_device):
    """
    读取SPI设备的传感器数据
    :param spi_device: SPI设备实例
    :return: 传感器数据
    """
    sensor_data = spi_device.read_byte()
    if sensor_data is not None:
        print(f"Sensor data: {sensor_data}")
        return sensor_data
    return None

def main(args=None):
    spi_device = SPIDevice(bus=0, device=0, max_speed_hz=50000, mode=0b00)

    # 控制设备（假设发送控制命令）
    control_device(spi_device, 0x01)

    # 读取传感器数据
    read_sensor_data(spi_device)

    # 关闭SPI设备
    spi_device.close()

# 测试程序
if __name__ == "__main__":
    main()
    
