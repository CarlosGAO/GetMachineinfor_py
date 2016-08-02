#!/usr/bin/python

from __future__ import division

class Handler():
###GET OS VERTION##########################################
    def os_ver(self,datasrc):
        self.f = open(datasrc, 'r')
        for line in self.f:
            line = line.strip()
            if line.startswith('Description:'):
                self.os = line.split(':')[1].strip()
            else:
                continue
        self.f.close()
        return self.os
###GET PRODUCTION INFORMATION##############################
    def production_info(self,datasrc):
        self.f = open(datasrc, 'r')
        self.production = None
	self.sn = None
        for line in self.f:
            line = line.strip()
            if line.startswith('Product Name'):
                self.production = line.split(':')[1].strip()
            elif line.startswith('Serial Number'):
                self.sn = line.split(':')[1].strip()
            else:
                continue
        self.f.close()
        return self.production,self.sn

###GET CPU INFORMAITON#####################################
    def cpu_info(self,datasrc):
        self.cpu_mod = False
        self.cpu_count = 0
        self.f = open(datasrc,'r')
        for data in self.f:
            if data.startswith('model name'):
                if not self.cpu_mod:
                    self.cpu_mod = data.split(':')[1].strip()
                self.cpu_count += 1
        self.f.close()
        return ''.join(self.cpu_mod.split()),int(self.cpu_count)

###GET MEMORY INFORMAITON##################################
    def mem_info(self,datasrc):
        self.f = open(datasrc,'r')
        for line in self.f:
            if line.startswith('MemTotal:'):
                self.mem_total = int(line.split()[1])
            elif line.startswith('MemFree:'):
                self.mem_free = int(line.split()[1])
            elif line.startswith('Buffers:'):
                self.mem_buffers = int(line.split()[1])
            elif line.startswith('Cached:'):
                self.mem_cache = int(line.split()[1])
            else:
                continue
        self.f.close()
        self.usege_percent = '%.2f%%' % float((self.mem_total-self.mem_free-self.mem_buffers-self.mem_cache)/self.mem_total*100)
        self.mem_total = '%.2fG' % float(self.mem_total/1024/1024)
        return self.mem_total,self.usege_percent

###GET DISK INFORMATION####################################
    def disk_info(self,datasrc):
        self.f = open(datasrc,'r')
        for line in self.f:
            if line.startswith('/dev/'):
                yield line.split()
            else:
                continue
        self.f.close()
    def disk_data(self,diskhandler,datasrc):
        self.used_total = 0
        self.disk_total = 0
        for disk_data in diskhandler(datasrc):
            Total = '%.2f%s' % (float(int(disk_data[1])/1024),"G")
            Used = '%.2f%s' % (float(int(disk_data[2])/1024),"G")
            self.used_total += float(int(disk_data[2])/1024)
            self.disk_total += float(int(disk_data[1])/1024)
        self.used_total = '%.2f%s' % (self.used_total,"G")
        self.disk_total = '%.2f%s' % (self.disk_total,"G")
        return self.used_total,self.disk_total
