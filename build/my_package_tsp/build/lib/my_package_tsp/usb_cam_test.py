import rclpy
from rclpy.node import Node
from flask import Flask, Response
import cv2
import threading

app = Flask(__name__)

# 打开 USB 摄像头，0 是默认的设备 ID
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法连接到摄像头")
    exit()

def generate():
    while True:
        ret, frame = cap.read()  # 读取一帧
        if not ret:
            print("无法读取摄像头数据")
            break

        # 编码图像为 JPEG 格式
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            print("图像编码失败")
            break

        # 将图像转换为字节流，发送给客户端
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return """
        <html>
            <body>
                <h1>USB 摄像头实时视频流</h1>
                <img src="/video_feed">
            </body>
        </html>
    """

def flask_thread():
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

class UsbCamTestNode(Node):

    def __init__(self):
        super().__init__('usb_cam_test_node')
        self.get_logger().info("USB Camera Test Node started")

        # 启动 Flask 服务器
        threading.Thread(target=flask_thread, daemon=True).start()

def main():
    rclpy.init()
    node = UsbCamTestNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()

