#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>

int main(int argc, char *argv[])
{
    // 初始化 ROS 2 节点
    rclcpp::init(argc, argv);
    
    // 创建一个 Node 对象
    auto node = std::make_shared<rclcpp::Node>("hello_ros2_publisher");
    
    // 创建一个 Publisher 对象，发布 std_msgs/String 类型的消息
    auto publisher = node->create_publisher<std_msgs::msg::String>("hello_topic", 10);
    
    // 创建一个 String 类型的消息对象
    std_msgs::msg::String msg;
    msg.data = "Hello ROS2";
    
    // 定时发布消息
    rclcpp::Rate loop_rate(1);  // 设置发布频率为1Hz (每秒发布一次)
    while (rclcpp::ok()) {
        // 发布消息
        RCLCPP_INFO(node->get_logger(), "Publishing: '%s'", msg.data.c_str());
        publisher->publish(msg);
        
        // 等待一段时间
        loop_rate.sleep();
    }
    
    rclcpp::shutdown();
    return 0;
}
