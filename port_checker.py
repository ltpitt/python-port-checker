#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Dependencies:
# to install notification read instructions here
# https://github.com/ltpitt/python-simple-notifications

import socket
import notification
import time

max_error_count = 100

def reset_error_counter():
    # Reset error counter so it won't flood you with notifications
    file = open('ErrorCount.log', 'w')
    file.write('0')
    file.close()

def increase_error_count():
    # Quick hack to handle false Port not open errors
    with open('ErrorCount.log') as f:
        for line in f:
            error_count = line
    error_count = int(error_count)
    print ("Error counter: " + str(error_count))
    file = open('ErrorCount.log', 'w')
    file.write(str(error_count + 1))
    file.close()
    if error_count == max_error_count:
        # Send email, pushover, slack or do any other fancy stuff
        print ("Sending out notification")
        reset_error_counter()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2) 

reset_error_counter()
result = 'start'

while(result != 'done'):
    result = sock.connect_ex(('127.0.0.1',8123))
    if result == 0:
        print ("Port is open")
        notification.send_pushover_notification("Home Assistant is now Online")
        result = 'done'
    elif result == 50:
        print("Port is still not open after 50 tries")
        notification.send_pushover_notification("Home Assistant is not started yet")
    else:
        print ("Port is not open")
        increase_error_count()
    time.sleep(5)
