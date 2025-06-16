#!/usr/bin/env python3
import argparse
import serial
import time
import sys
from datetime import datetime

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='串口数据接收工具（单行刷新显示）')
    parser.add_argument('-p', '--port', required=True, help='串口号（如 COM1 或 /dev/ttyUSB0）')
    parser.add_argument('-b', '--baudrate', type=int, default=9600, help='波特率（默认 9600）')
    parser.add_argument('-t', '--timeout', type=float, default=1, help='超时时间（秒，默认 1）')
    parser.add_argument('--hex', action='store_true', help='以十六进制格式显示数据')
    args = parser.parse_args()

    try:
        # 打开串口
        ser = serial.Serial(
            port=args.port,
            baudrate=args.baudrate,
            timeout=args.timeout
        )
        print(f"已连接到 {args.port}，波特率 {args.baudrate}")
        print("按 Ctrl+C 退出...")

        # 记录上次刷新时间
        last_refresh_time = time.time()
        refresh_interval = 0.1  # 最小刷新间隔（秒）

        try:
            while True:
                # 读取串口数据
                if ser.in_waiting:
                    data = ser.read(ser.in_waiting)
                    
                    # 格式化数据
                    if args.hex:
                        display_data = data.hex()
                    else:
                        try:
                            display_data = data.decode('utf-8', errors='replace')
                        except UnicodeDecodeError:
                            display_data = data.decode('gbk', errors='replace')
                    
                    # 清除不可见字符
                    display_data = display_data.replace('\n', ' ').replace('\r', ' ').strip()
                    
                    # 添加时间戳
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    line = f"[{timestamp}] {display_data}"
                    
                    # 控制刷新频率
                    current_time = time.time()
                    if current_time - last_refresh_time >= refresh_interval:
                        # 单行刷新显示
                        sys.stdout.write("\033[K")  # 清除当前行
                        sys.stdout.write(f"\r{line}")
                        sys.stdout.flush()
                        last_refresh_time = current_time

                # 避免 CPU 占用过高
                time.sleep(0.01)

        except KeyboardInterrupt:
            print("\n程序已退出")
        finally:
            ser.close()

    except serial.SerialException as e:
        print(f"串口连接失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()