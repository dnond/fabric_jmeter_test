# -*- coding: utf-8 -*-

import time
import datetime

from fabric.contrib.files import exists
from fabric.api import run

from ClassException import ClassException

from Debug import Debug


class ExecConfig(object):
    jmeter_path = '/usr/local/apache-jmeter/bin/jmeter'
    
    jmx_filename = 'test.jmx'
    jmx_dir = '/tmp/jmx'
    
    log_filename = 'test_log'
    log_dir = '/tmp/jmeter'
    log_file = None
    log_file_extension = '.log'
    
    run_log = '/tmp/jmeter.log'
    
    thread = 1
    rampup = 1
    loop = 1
    
    test_name = 'test'
    
    options_dic = {'-n':''}

    def __init__(self, jmx_filename=None, jmx_dir=None, log_dir=None):
        pass
    
    def setConfig(self, *args, **kwargs ):
        for key, value in kwargs.items():
            if hasattr(ExecConfig, key):
                setattr(self, key, value)

    def setupAuto(self, test_name=None):
        if test_name is None:
            splited = self.jmx_filename.split('.jmx')
            self.test_name = splited[0]
        
        datestr = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
        self.log_filename = "%s_T%s_R%s_L%s_%s" % (self.test_name, self.thread, self.rampup, self.loop, datestr)
        
        Debug.prt( 'log_filename: %s' % ( self.log_filename ))

        log_file = "%s/%s-01%s" % ( self.log_dir, self.log_filename ,self.log_file_extension)
        
        Debug.prt( 'log_file: %s' % ( log_file ))
        
        find_flg = False
        if exists( log_file ):
            for i in xrange( 2, 99 ):
                log_file = "%s/%s-%02d%s" % ( self.log_dir, self.log_filename ,i ,self.log_file_extension)
                if not exists( log_file ):
                    find_flg = True
                    break
        else:
            find_flg = True
            
        if not find_flg == True:
            raise ClassException( message='Error:Fix logfile')
        
        self.log_file = log_file

    def __makeDir(self):
        if not exists(self.jmx_dir):
            run('mkdir %s' % (self.jmx_dir))
            
        if not exists(self.log_dir):
            run('mkdir %s' % (self.log_dir))
            
        
            
    def getExecCmd(self):
        self.__makeDir()
        
        cmd = ''
        
        cmd += self.jmeter_path
        cmd += ' '
        
        for key,value in self.options_dic.items():
            if value == '':
                cmd += "%s" % ( key )
            else:
                cmd += "%s=%s" % ( key, value )
        cmd += ' '
        
        cmd += "-l "
        if self.log_file is None:
            cmd += "%s/%s" % ( self.log_dir, self.log_filename )
        else:
            cmd += self.log_file
            
        cmd += ' '
        
        cmd += ' -j %s ' % ( self.run_log)
        cmd += ' '
        
        cmd += ' -t %s/%s' % ( self.jmx_dir, self.jmx_filename )
        cmd += ' '
        
        cmd += ' -Jthread %s' % ( self.thread)
        cmd += ' '
        
        cmd += ' -Jrampup %s' % ( self.rampup)
        cmd += ' '
        
        cmd += ' -Jloop %s' % ( self.loop)
        cmd += ' '
        
        Debug.prt( 'cmd: %s' % ( cmd ))
        
        return cmd
            