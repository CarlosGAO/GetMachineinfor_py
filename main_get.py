#!/usr/bin/python

import csv
import os
import sys
import time
from xlwt import *
from util import *
from getsource import *
from handlers import *


sshkey = '/root/.ssh/known_hosts'
if os.path.exists(sshkey):
    os.remove(sshkey)

class main_gets():
    def __init__(self,getsource,handler):
        self.getsource = getsource
        self.handler = handler
        self.datasrc = '/tmp/datasrc'
        self.hostslist = 'sourcedir/' + 'hostsource'
        self.ipsource = 'sourcedir/' + 'ipsource_' + time.strftime('%Y%m%d%H%M')
        self.nopasswd = 'logdir/' + 'nopasswd_' + time.strftime('%Y%m%d%H%M') + '.log'
        self.errhostlog = 'logdir/' + 'errhost_' + time.strftime('%Y%m%d%H%M') + '.log'
        self.output_file = 'output/' + 'hosts_' + time.strftime('%Y%m%d%H%M') + '.xls'
        self.hostslistobj = open(self.hostslist,'r')
        self.ipsourceobj = open(self.ipsource,'w') 
        self.nopasswdobj = open(self.nopasswd,'w')
        self.xlsfile = Workbook() 
        self.xlsobj = self.xlsfile.add_sheet('hostdata')
        self.datavalue = ['IP_Adress','OS','Product_name','Serial_Number','CPU_counts','CPU_module','MEM_total','MEM_usage','DISK_total','DISK_usage']

    def login(self):
        self.rowxls = 0
        self.ipsourceobj = open(self.ipsource,'r')
        self.xlsobj.row(0).set_style(easyxf('font: height 270'))
        self.xlstyle0 = easyxf("pattern: pattern solid, fore_color yellow; borders: left 1,right 1,top 1,bottom 1; font: bold 1,height 240,name Times New Roman; align: vert centre,horiz center")
        for col1 in range(0,len(self.datavalue)):
            self.xlsobj.col(col1).width=256*16
            self.xlsobj.write(self.rowxls,col1,self.datavalue[col1],self.xlstyle0)
        self.xlsobj.col(1).width=256*48
        self.xlsobj.col(2).width=256*24
        self.xlsobj.col(3).width=256*20
        self.xlsobj.col(5).width=256*36
        self.rowxls = 1
        for ip,passwd in user(self.ipsourceobj):
            try:
                self.getsource.connection(ip,passwd,self.datasrc)
                self.ip = ip
                self.os = self.handler.os_ver(self.datasrc)
                self.product,self.sn = self.handler.production_info(self.datasrc)
                self.cpu,self.count = self.handler.cpu_info(self.datasrc)
                self.mem,self.usage = self.handler.mem_info(self.datasrc)
                self.disk,self.total = self.handler.disk_data(self.handler.disk_info,self.datasrc)
                self.datalist = [self.ip,self.os,self.product,self.sn,self.count,self.cpu,self.mem,self.usage,self.total,self.disk]
                self.xlstyle1 = easyxf("borders: left 1,right 1,top 1,bottom 1; align: horiz left; font: name Times New Roman")
                for col2 in range(0,len(self.datalist)):
                    self.xlsobj.write(self.rowxls,col2,self.datalist[col2],self.xlstyle1)
                self.rowxls +=1
                os.remove(self.datasrc)
            except:
                print>>open(self.errhostlog,'a+'),'%s%s' % ("Error: PASSWORD is wrong or SSH service is down->",ip)
        self.xlsfile.save(self.output_file)
        open(self.errhostlog,'a+').close()
        self.ipsourceobj.close()
        return True

    def get_passwd(self,file):
        self.passwddict = {}
        self.iplist = []
        for line in lines(self.hostslistobj):
            if line.strip():
                self.iplist = line.split()
                self.passwddict[self.iplist[0]] = self.iplist[1]
                self.iplist = []
        for line in lines(file):
            if line.strip():
                line = line.strip('\n')
                if self.passwddict.get(line):
                    line = line + '\t' + self.passwddict.get(line) + '\n'
                    self.ipsourceobj.write(line)
                else:
                    line = line + ' has no passwd' + '\n'
                    self.nopasswdobj.write(line)
        self.ipsourceobj.close()
        self.nopasswdobj.close()

if __name__ == '__main__':
    print 'Please Wait a moment......'
    getsrc = ssh_con()
    handler = Handler() 
    fmt = main_gets(getsrc,handler)
    fmt.get_passwd(sys.stdin)
    fmt.login()
