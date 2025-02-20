#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <opencv2/opencv.hpp>
#include <microhttpd.h>
#include <pthread.h>

// 摄像头设备路径和端口
#define VIDEO_DEVICE "/dev/video0"
#define HTTP_PORT 5000

// 创建 OpenCV 摄像头对象
cv::VideoCapture cap(VIDEO_DEVICE);
bool running = true;

// 用于存储最新的图像数据
std::vector<uchar> latest_frame;
pthread_mutex_t frame_mutex = PTHREAD_MUTEX_INITIALIZER;

// 图像处理函数
void *video_feed(void *arg) {
    while (running) {
        cv::Mat frame;
        cap >> frame;  // 捕获一帧图像

        if (frame.empty()) {
            fprintf(stderr, "无法读取摄像头数据\n");
            break;
        }

        // 将图像编码为 JPEG 格式
        std::vector<uchar> buffer;
        if (!cv::imencode(".jpg", frame, buffer)) {
            fprintf(stderr, "图像编码失败\n");
            break;
        }

        // 使用互斥锁保护对共享数据的访问
        pthread_mutex_lock(&frame_mutex);
        latest_frame = buffer;  // 更新最新的图像
        pthread_mutex_unlock(&frame_mutex);

        // 睡眠一段时间，避免过度占用 CPU
        usleep(10000);  // 10 毫秒
    }
    return NULL;
}

// HTTP 响应回调函数
static int answer_to_connection(void *cls, struct MHD_Connection *connection,
                                 const char *url, const char *method,
                                 const char *version, const char *upload_data,
                                 size_t *upload_data_size, void **con_cls) {

    if (strcmp(url, "/video_feed") == 0) {
        // 启动视频流处理线程
        pthread_mutex_lock(&frame_mutex);
        if (!latest_frame.empty()) {
            struct MHD_Response *response;
            response = MHD_create_response_from_buffer(latest_frame.size(), latest_frame.data(), MHD_RESPMEM_PERSISTENT);
            int ret = MHD_queue_response(connection, MHD_HTTP_OK, response);
            MHD_destroy_response(response);
            pthread_mutex_unlock(&frame_mutex);
            return ret;
        }
        pthread_mutex_unlock(&frame_mutex);
    }

    return MHD_NO;
}

// 启动 HTTP 服务器
void start_http_server() {
    struct MHD_Daemon *daemon;

    daemon = MHD_start_daemon(MHD_USE_THREAD_PER_CONNECTION, HTTP_PORT, NULL, NULL,
                              &answer_to_connection, NULL, MHD_OPTION_END);
    if (daemon == NULL) {
        fprintf(stderr, "无法启动 HTTP 服务器\n");
        exit(1);
    }

    printf("HTTP 服务器启动，监听端口 %d\n", HTTP_PORT);
    printf("请通过以下地址访问视频流:\n");
    printf("本地访问: http://127.0.0.1:5000\n");
    printf("局域网访问: http://<你的IP>:5000\n");
    getchar();  // 阻塞等待用户按键
    MHD_stop_daemon(daemon);
}

// ROS2 节点类的模拟
void *ros2_node(void *arg) {
    printf("USB Camera Test Node started\n");

    // 启动 HTTP 服务器
    start_http_server();

    return NULL;
}

int main(int argc, char *argv[]) {
    // 打开摄像头
    if (!cap.isOpened()) {
        fprintf(stderr, "无法连接到摄像头\n");
        return -1;
    }

    // 启动 ROS2 模拟线程
    pthread_t ros_thread;
    pthread_create(&ros_thread, NULL, ros2_node, NULL);

    // 启动视频流处理线程
    pthread_t video_thread;
    pthread_create(&video_thread, NULL, video_feed, NULL);

    // 等待线程结束
    pthread_join(ros_thread, NULL);
    pthread_join(video_thread, NULL);

    // 释放资源
    cap.release();
    return 0;
}

