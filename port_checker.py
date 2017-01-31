#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Dependencies:
# to install notification read instructions here
# https://github.com/ltpitt/python-simple-notifications

import socket
import time

try:
    import notification
except ImportError:
    print "Warning:"
    print "Notification module is missing, no notifications will be sent."
    print
    print "You can download python-simple-notifications here:"
    print "https://github.com/ltpitt/python-simple-notifications.git"
    print

# Customize those variables to meet your needs
max_error_limit = 100
host = '127.0.0.1'
port = 80

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
    if error_count == max_error_limit:
        # Send email, pushover, slack or do any other fancy stuff
        ko_message = "Port " + str(port) + " is not listening"
        print(ko_message)
        try:
            notification.send_pushover_notification(ko_message)
        except NameError:
            pass
        reset_error_counter()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2) 

reset_error_counter()

result = 'start'
while(result != 'done'):
    result = sock.connect_ex((host,port))
    if result == 0:
        ok_message = "Port " + str(port) + " is now listening"
        print (ok_message)
        try:
            notification.send_pushover_notification(ok_message)
        except NameError:
            pass
        result = 'done'
    else:
        print ("Port is not open")
        increase_error_count()
    time.sleep(5)
