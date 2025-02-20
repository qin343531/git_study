#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>
#include <termios.h>
#include <unistd.h>
#include <iostream>

class KeyboardPublisher : public rclcpp::Node
{
public:
    KeyboardPublisher() : Node("keyboard_publisher")
    {
        // 创建发布者
        publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);
        RCLCPP_INFO(this->get_logger(), "Keyboard Publisher Node is running...");

        // 启动读取键盘输入的线程
        keyboard_input_loop();
    }

private:
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;

    // 读取单个字符
    char read_key()
    {
        struct termios oldt, newt;
        char ch;
        tcgetattr(STDIN_FILENO, &oldt);
        newt = oldt;
        newt.c_lflag &= ~(ICANON | ECHO); // 禁用缓冲区模式和回显
        tcsetattr(STDIN_FILENO, TCSANOW, &newt);
        ch = getchar();
        tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
        return ch;
    }

    // 键盘输入循环
    void keyboard_input_loop()
    {
        while (rclcpp::ok())
        {
            char key = read_key(); // 获取输入的字符
            if (key == 'q') // 如果按下 'q' 就退出
            {
                RCLCPP_INFO(this->get_logger(), "Exiting keyboard publisher...");
                break;
            }

            // 创建并发布消息
            auto msg = std_msgs::msg::String();
            msg.data = std::string(1, key);
            publisher_->publish(msg);
            RCLCPP_INFO(this->get_logger(), "Published: \"%s\"", msg.data.c_str());
        }
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<KeyboardPublisher>());
    rclcpp::shutdown();
    return 0;
}

