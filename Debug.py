# -*- coding: utf-8 -*-

import pprint


class Debug:

    debug_log = ''

    @classmethod
    def prt( self, var, message = '' ):
        pprint.pprint( var )



