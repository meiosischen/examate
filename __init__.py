#!/usr/bin/python
# -*- coding: utf-8 -*-

__title__ = 'examate'
__version__ = '0.1.0'
__author__ = 'Meiosis Chen'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Meiosis Chen'

import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='myapp.log',
    filemode='w')
