#!/usr/bin/python

import pexpect

class ssh_con():
    user = 'root'
    def connection(self,ipaddr,passwd,datasrc):
        self.ip = ipaddr
        self.passwd = passwd
        self.datasrc = datasrc
        self.child = pexpect.spawn('/usr/bin/ssh',[self.user+'@'+self.ip],10)
        self.fout = file(self.datasrc,'w')
        self.child.logfile = self.fout
        try:
            self.child.expect('\(yes/no\)\?')
            self.child.sendline('yes')
        except:
            self.tmpfile = open('/tmp/known_hosts.log','a+')
            print>>self.tmpfile,self.ip + ' is known host'
            self.tmpfile.close()
        self.child.expect('(?i)password:')
        self.child.sendline(self.passwd)
        self.child.expect('.#')
        self.child.sendline('lsb_release -a')
        self.child.expect('.#')
        self.child.sendline('dmidecode  | grep "Product Name:" | sed -n "1p"')
        self.child.expect('.#')
        self.child.sendline('dmidecode  | grep "Serial Number" | sed -n "1p"')
        self.child.expect('.#')
        self.child.sendline('cat /proc/cpuinfo')
        self.child.expect('.#')
        self.child.sendline('cat /proc/meminfo ')
        self.child.expect('.#')
        self.child.sendline('df -lmP | grep "^/dev"')
        self.child.expect('.#')
        self.child.sendline('exit')
        self.fout.close()
        return True
