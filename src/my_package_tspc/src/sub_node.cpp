#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>

class SubscriberNode : public rclcpp::Node
{
public:
    // 构造函数接受一个话题名称参数
    SubscriberNode(const std::string & topic_name) : Node("subscriber_node")
    {
        // 使用传入的话题名称创建订阅者
        subscription_ = this->create_subscription<std_msgs::msg::String>(
            topic_name, 10, std::bind(&SubscriberNode::topic_callback, this, std::placeholders::_1)
        );
    }
    
private:
    // 回调函数处理接收到的消息
    void topic_callback(const std_msgs::msg::String::SharedPtr msg) const
    {
        RCLCPP_INFO(this->get_logger(), "Received message: '%s'", msg->data.c_str());
    }

    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
    // 初始化 ROS 2 系统
    rclcpp::init(argc, argv);

    // 如果提供了话题名称作为参数，就使用它
    std::string topic_name = "topic"; // 默认话题
    if (argc > 1) {
        topic_name = argv[1]; // 从命令行参数中获取话题名称
    }

    // 创建节点对象并传递话题名称
    rclcpp::spin(std::make_shared<SubscriberNode>(topic_name));

    // 清理 ROS 2 系统
    rclcpp::shutdown();
    return 0;
}

