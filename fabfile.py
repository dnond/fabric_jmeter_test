# -*- coding: utf-8 -*-

import os, sys
from fabric.api import env, put
from ExecConfig import ExecConfig
from ExecJmeter import ExecJmeter

from Debug import Debug
from ClassException import ClassException

###########
## ENV

def env_vagrant():
	env.user = 'vagrant'
	env.hosts = ['127.0.0.1:2200']
	env.key_filename = "~/.vagrant.d/insecure_private_key"
		
	env.cExecConfig = ExecConfig()
	env.cExecConfig.setConfig(
							jmx_dir='/home/vagrant/jmx',
							jmx_filename='test.jmx',
							log_dir='/tmp/jmeter',
							thread=50, 
							loop=10
							)
	

###########

"""
実行例
$ fab env_vagrant doTest:jmx=/Users/hoge/Documents/jmx/test.jmx,config=auto,thread=10,loop=10,rampup=10

"""
def doTest(*args, **kwargs):
	Debug.prt(kwargs)
		
	## コマンドライン引数をセットする
	if isinstance(kwargs, dict):
		env.cExecConfig.setConfig(kwargs)
		
	## jmxが指定されていればアップロード
	if 'jmx' in kwargs:
		local_jmx_file = kwargs['jmx']
		Debug.prt(kwargs['jmx'],'jmx')
		
		#jmxが指定されている時のみ、config=autoを使用出来る
		if 'config' in kwargs and kwargs['config'] == 'auto':
			env.cExecConfig.setupAuto()
			
		env.cExecConfig.jmx_file = os.path.basename(local_jmx_file)
 		put(local_jmx_file, "%s/%s" % ( env.cExecConfig.jmx_dir, env.cExecConfig.jmx_file ))

	try:
		# テストを実行
		cExecJmeter = ExecJmeter()
		cExecJmeter.execTest( env.cExecConfig )
	except ClassException, e:
		print e.message

