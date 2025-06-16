#!/usr/bin/env python3
import argparse
import serial
import time
import sys
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='串口数据接收工具（处理\r\n格式数据包）')
    parser.add_argument('-p', '--port', required=True, help='串口号（如 COM1 或 /dev/ttyUSB0）')
    parser.add_argument('-b', '--baudrate', type=int, default=9600, help='波特率（默认 9600）')
    parser.add_argument('-t', '--timeout', type=float, default=1, help='超时时间（秒，默认 1）')
    parser.add_argument('--hex', action='store_true', help='以十六进制格式显示数据')
    args = parser.parse_args()

    try:
        ser = serial.Serial(
            port=args.port,
            baudrate=args.baudrate,
            timeout=args.timeout
        )
        print(f"已连接到 {args.port}，波特率 {args.baudrate}")
        print("按 Ctrl+C 退出...")

        buffer = bytearray()  # 用于累积数据的缓冲区
        last_refresh_time = time.time()
        refresh_interval = 0.1

        while True:
            if ser.in_waiting:
                # 读取所有可用数据
                data = ser.read(ser.in_waiting)
                buffer.extend(data)

                # 查找完整的数据包（以\r开头，\n结尾）
                while True:
                    # 查找\r的位置
                    start_idx = buffer.find(b'\r')
                    if start_idx == -1:
                        break  # 没有找到\r，继续积累数据

                    # 查找对应的\n（从\r之后开始找）
                    end_idx = buffer.find(b'\n', start_idx + 1)
                    if end_idx == -1:
                        break  # 没有找到完整的\r...\n，继续积累数据

                    # 提取完整数据包（包括\r和\n）
                    packet = buffer[start_idx:end_idx + 1]
                    # 从缓冲区中移除已处理的数据
                    buffer = buffer[end_idx + 1:]

                    # 处理数据包内容（去掉首尾的\r和\n）
                    payload = packet[1:-1]  # 去掉\r和\n

                    # 格式化显示
                    if args.hex:
                        display_data = payload.hex()
                    else:
                        try:
                            display_data = payload.decode('utf-8', errors='replace')
                        except UnicodeDecodeError:
                            display_data = payload.decode('gbk', errors='replace')

                    # 添加时间戳并显示
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    line = f"[{timestamp}] {display_data}"

                    # 控制刷新频率
                    current_time = time.time()
                    if current_time - last_refresh_time >= refresh_interval:
                        sys.stdout.write("\033[K")  # 清除当前行
                        sys.stdout.write(f"\r{line}")
                        sys.stdout.flush()
                        last_refresh_time = current_time

            time.sleep(0.01)

    except serial.SerialException as e:
        print(f"串口连接失败: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n程序已退出")
    finally:
        if ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()