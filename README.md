# Covert-transmission-based-on-ICMP
See more detail at https://blog.csdn.net/a675115471/article/details/104098505
# Prerequisites
在运行程序前，你需要先安装第三方库scapy，安装说明详见https://scapy.readthedocs.io/en/latest/installation.html  
`如果你的系统是Windows，你需要先安装nmap，详见https://scapy.readthedocs.io/en/latest/installation.html#windows`
# Installing
分别将【receiving terminal】与【transmitting terminal】拷贝至隐蔽传输通信的发送端和接收端即可  
其中  
## 【receiving terminal】
`隐蔽传输接收端Python运行代码`  
主程序：rcv.py  
功能：接收有预定特征的ICMP报文 -> 提取二进制信息 -> BCH纠错译码 -> 生成二进制文件 -> Huffman压缩译码 -> 得到源文件  
输入：无输入，直接运行即可  
## 【transmitting terminal】
`隐蔽传输发送端Python运行代码`  
主程序：send.py  
功能：文件 -> Huffman压缩编码 -> 提取二进制值 -> BCH纠错编码 -> 生成一系列携带隐藏信息的ICMP报文 -> 发送  
输入：①待发送的文件名，例如 lena.bmp ②发送对象的ip，例如 192.168.1.11 ③丢包率(0~1)，例如 0.03  
## Others
①发送端发送的文件，应与send.py置于同一目录  
②建议收发端Python版本均不低于3.7  
③实验中隐蔽传输测试用文件见【文件传输测试用例】	
			

