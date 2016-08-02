# 此脚本用于获取主机基本信息
# 使用方法如下：
1，在hostlist文件中写入需要获取主机信息的IP地址
2，在sourcedir目录中的hostsource文件中加入主机的IP地址及对应的口令，IP地址及口令用空格分隔
3，运行脚本：main_get.py < hostlist，等待结束，结果都会保存在output目录中的xls文件中
4，errlog目录中会存放没有收集到主机信息的报错日志
