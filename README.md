这是一个简单python项目  
目的是实现一个python脚本，能在命令行里用单行快速刷新单片机传输过来的快速刷新的串口数据（串口数据以\r开头 \n结尾）。  
参数:  
    parser.add_argument('-p', '--port', required=True, help='串口号（如 COM1 或 /dev/ttyUSB0）')  
    parser.add_argument('-b', '--baudrate', type=int, default=9600, help='波特率（默认 9600）')  
    parser.add_argument('-t', '--timeout', type=float, default=1, help='超时时间（秒，默认 1）')  
    parser.add_argument('--hex', action='store_true', help='以十六进制格式显示数据')  
