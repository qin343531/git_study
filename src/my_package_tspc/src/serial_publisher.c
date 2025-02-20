#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <rcl/rcl.h>
#include <std_msgs/msg/string.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include "serial_comm.c"  // 引入串口操作模块

// 监听回调
void listener_callback(const void *msgin) {
    const std_msgs__msg__String *msg = (const std_msgs__msg__String *)msgin;
    printf("Received: \"%s\"\n", msg->data.data);

    // 创建串口通信对象并发送数据
    SerialComm serial = {SERIAL_PORT, BAUD_RATE, TIMEOUT, -1};
    if (open_serial(&serial) == 0) {
        send_data(&serial, msg->data.data);
        close_serial(&serial);
    }
}

int main(int argc, char *argv[]) {
    rcl_ret_t ret;
    rclc_support_t support;
    rcl_node_t node;
    rcl_subscription_t subscription;
    rclc_executor_t executor;
    std_msgs__msg__String msg;

    // 初始化ROS客户端库
    ret = rclc_support_init(&support, argc, (const char * const*)argv, NULL);
    if (ret != RCL_RET_OK) {
        printf("rclc_support_init failed\n");
        return -1;
    }

    // 创建节点
    ret = rclc_node_init_default(&node, "serial_publisher", "", &support);
    if (ret != RCL_RET_OK) {
        printf("rclc_node_init_default failed\n");
        return -1;
    }

    // 创建订阅者
    ret = rclc_subscription_init_default(&subscription, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, String), "chatter");
    if (ret != RCL_RET_OK) {
        printf("rclc_subscription_init_default failed\n");
        return -1;
    }

    // 创建执行器
    ret = rclc_executor_init(&executor, &support.context, 1, NULL);
    if (ret != RCL_RET_OK) {
        printf("rclc_executor_init failed\n");
        return -1;
    }

    // 添加订阅者到执行器
    rclc_executor_add_subscription(&executor, &subscription, &msg, &listener_callback, (rclc_executor_handle_invocation_t)0);

    // 执行ROS2节点
    printf("串口发布者节点已启动...\n");
    rclc_executor_spin(&executor);

    // 清理
    (void)rcl_subscription_fini(&subscription, &node);
    (void)rcl_node_fini(&node);
    (void)rclc_executor_fini(&executor);
    (void)rclc_support_fini(&support);

    return 0;
}

