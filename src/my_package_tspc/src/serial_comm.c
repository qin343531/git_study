#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <rclc/rclc.h>


#define SERIAL_PORT "/dev/ttyS3"  // 串口设备路径
#define BAUD_RATE B115200  // 波特率
#define TIMEOUT 0  // 超时时间，单位为秒

// 串口通信结构体
typedef struct {
    char *port;
    speed_t baud_rate;
    int timeout;
    int fd;  // 串口文件描述符
} SerialComm;

// 打开串口
int open_serial(SerialComm *serial) {
    serial->fd = open(serial->port, O_RDWR | O_NOCTTY | O_NDELAY);
    if (serial->fd == -1) {
        perror("无法打开串口");
        return -1;
    }

    struct termios options;
    tcgetattr(serial->fd, &options);

    // 设置波特率
    cfsetispeed(&options, serial->baud_rate);
    cfsetospeed(&options, serial->baud_rate);

    // 设置8位数据位、1位停止位、无校验位
    options.c_cflag &= ~PARENB;  // 无校验位
    options.c_cflag &= ~CSTOPB;  // 1位停止位
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;      // 8位数据位

    options.c_cflag |= (CLOCAL | CREAD);  // 允许接受数据
    options.c_iflag &= ~(IXON | IXOFF | IXANY);  // 禁用流控制
    options.c_iflag &= ~ICANON;  // 禁用规范模式
    options.c_iflag &= ~ECHO;    // 禁用回显
    options.c_iflag &= ~ECHOE;   // 禁用回显（输入时不显示字符）
    options.c_iflag &= ~ISIG;    // 禁用信号

    tcsetattr(serial->fd, TCSANOW, &options);  // 应用设置

    // 设置超时
    struct timeval tv;
    tv.tv_sec = serial->timeout;
    tv.tv_usec = 0;
    setsockopt(serial->fd, SOL_SOCKET, SO_RCVBUF, &tv, sizeof(tv));

    printf("串口 %s 已打开，波特率：%d\n", serial->port, serial->baud_rate);
    return 0;
}

// 向串口发送数据
int send_data(SerialComm *serial, const char *data) {
    if (serial->fd == -1) {
        printf("串口未打开\n");
        return -1;
    }
    int len = strlen(data);
    if (write(serial->fd, data, len) != len) {
        perror("写入串口失败");
        return -1;
    }
    return 0;
}

// 关闭串口
void close_serial(SerialComm *serial) {
    if (serial->fd != -1) {
        close(serial->fd);
        printf("串口 %s 已关闭\n", serial->port);
    }
}
