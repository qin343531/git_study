cmake_minimum_required(VERSION 3.5)
project(my_package_tspc)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Set the ROS 2 workspace path
set(CMAKE_PREFIX_PATH "/opt/ros/foxy" ${CMAKE_PREFIX_PATH})

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclc REQUIRED)
find_package(rclcpp REQUIRED)
find_package(OpenCV REQUIRED)
find_package(std_msgs REQUIRED)


# 查找 libmicrohttpd 库
find_package(PkgConfig REQUIRED)
pkg_check_modules(MHD REQUIRED libmicrohttpd)

# 包含 libmicrohttpd 的头文件路径
include_directories(${MHD_INCLUDE_DIRS})

# Add executable
add_executable(pub_node src/pub_node.cpp)
add_executable(sub_node src/sub_node.cpp)
add_executable(usb_cam_test src/usb_cam_test.cpp)
add_executable(serial_publisher src/serial_publisher.c)
add_executable(keyboard_pub src/keyboard_pub.cpp)

ament_target_dependencies(pub_node rclcpp std_msgs)
ament_target_dependencies(sub_node rclcpp std_msgs)
ament_target_dependencies(usb_cam_test rclcpp rclc)
ament_target_dependencies(serial_publisher rclcpp rclc)
ament_target_dependencies(keyboard_pub rclcpp std_msgs)

# 链接 OpenCV 和 libmicrohttpd 库
target_link_libraries(usb_cam_test ${OpenCV_LIBS} ${MHD_LIBRARIES})

add_compile_options(-Wno-unused-result)

# Testing
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

# 安装可执行文件
install(TARGETS pub_node sub_node usb_cam_test serial_publisher keyboard_pub DESTINATION lib/${PROJECT_NAME})

ament_package()

