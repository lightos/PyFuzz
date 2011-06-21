from pydbg import *
from pydbg.defines import *
from smtplib import SMTP_SSL

import utils
import threading
import shutil
import os
import time

class pyfuzzer:

    def __init__(self, exe_path, ext, notify):

        self.exe_path       = exe_path
        self.ext            = ext
        self.notify_crash   = notify
        self.crash          = None
        self.send_notify    = False
        self.pid            = None
        self.v_handler      = False
        self.dbg            = None
        self.running        = False
        self.ready          = False
        self.smtpserver     = ''
	self.smtpport	    = 469
        self.recipients     = ['']
        self.sender         = 'Bug Alert!'
	self.iteration      = 0

    def load_file(self):
        
        while 1:
            if not self.running:

                self.test_file = "C:\\Python26\\pyfuzz\\test_cases\\"
                pydbg_thread   = threading.Thread(target=self.start_debugger)
                pydbg_thread.setDaemon(0)
                pydbg_thread.start()
                
                while self.pid == None:
                    time.sleep(1)
                    
                monitor_thread = threading.Thread(target=self.monitor_debugger)
                monitor_thread.setDaemon(0)
                monitor_thread.start()
                self.iteration += 1
                if self.iteration == 35600:
                    quit()
                
            else:
                time.sleep(1)
    
    def start_debugger(self):
        
        print "[*] Starting debugger for iteration: %d" % self.iteration
        self.running = True
        self.dbg = pydbg()
        
        self.dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, self.check_accessv)
        pid = self.dbg.load(self.exe_path, "%s%d.%s" % (self.test_file, self.iteration, self.ext))        
        self.pid = self.dbg.pid
        self.dbg.run()
        
    def check_accessv(self, dbg):
        
        if dbg.dbg.u.Exception.dwFirstChance:
            return DBG_CONTINUE
        
        print "[*] Woot! Handling an access violation!"
        self.v_handler = True
        crash_bin = utils.crash_binning.crash_binning()
        crash_bin.record_crash(dbg)
        self.crash = crash_bin.crash_synopsis()
        
        # Write out the crash information
        crash_fd = open("C:\\Python26\\pyfuzz\\crashes\\crash-%d" % self.iteration, "w")
        crash_fd.write(self.crash)
        
        # Copy the file
        shutil.copy("C:\\Python26\\pyfuzz\\test_cases\\%d.%s" % (self.iteration, self.ext), "crashes\\%d.%s" % (self.iteration, self.ext))
        
        self.dbg.terminate_process()
        self.v_handler = False
        self.running = False
        
        return DBG_EXCEPTION_NOT_HANDLED
    
    def monitor_debugger(self):
        
        counter = 0
        print "[*] Monitor thread for pid: %d waiting." % self.pid
        
        while counter < 3:
            time.sleep(1)
            print counter
            counter += 1
            
        if self.v_handler != True:
            time.sleep(1)
            self.dbg.terminate_process()
            self.pid = None
            self.running = False
        else:
            print "[*] The access violation handler is working. Waiting."
            
            while self.running:
                time.sleep(1)
                
    # Email routine
    def notify(self):
        
        message = "From:%s\r\n\r\nTo:\r\n\r\nIteration:%d\n\nOutput:\n\n%s" % (self.sender, self.iteration, self.crash)
	session = SMTP_SSL()
	session.connect(smtpserver, smtppport)
        session.sendmail(sender, recipients, message)
        session.quit()
        
        return
    
exe_path = None
ext      = None
notify   = False
    
exe_path = 'C:\\Windows\\system32\\notepad.exe'
ext      = 'txt'
    
fuzzer = pyfuzzer(exe_path, ext, notify)
fuzzer.load_file()
    
