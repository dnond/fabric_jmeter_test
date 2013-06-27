# -*- coding: utf-8 -*-

from fabric.api import run

from ExecConfig import ExecConfig


class ExecJmeter(object):

    def execTest(self, cExecConfig ):
        cmd = cExecConfig.getExecCmd()
        run( cmd )