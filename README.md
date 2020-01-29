# Covert-transmission-based-on-ICMP
#【receiving terminal】
      隐蔽传输接收端Python运行代码
			主程序：rcv.py
			功能：接收有预定特征的ICMP报文 -> 提取二进制信息 -> BCH纠错译码 -> 生成二进制文件 -> Huffman压缩译码 -> 得到源文件
			输入：无输入，直接运行即可

【transmitting terminal】隐蔽传输发送端Python运行代码
			主程序：send.py
			功能：文件 -> Huffman压缩编码 -> 提取二进制值 -> BCH纠错编码 -> 生成一系列携带隐藏信息的ICMP报文 -> 发送
			输入：①待发送的文件名，例如 lena.bmp ②发送对象的ip，例如 192.168.1.11 ③丢包率(0~1)，例如 0.03

【文件传输测试用例】	实验中隐蔽传输测试用文件

【依赖】		收发端代码运行所需的第三方库
			【nmap-7.70-setup.exe】	Windows系统必须安装，Linux系统可不需要	[包含scapy在Windows下运行的必要组件Npcap]
			【scapy-master.zip】	进入解压后的目录，在命令行中输入 python ./setup.py install 进行安装	[Python网络编程第三方库，注意python指令应与运行程序的Python版本相对应]

【其他说明】		①发送端发送的文件，应与send.py置于同一目录
			②建议收发端Python版本均不低于3.7
See more detail at https://blog.csdn.net/a675115471/article/details/104098505
