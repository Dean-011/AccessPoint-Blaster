import getpass
from netmiko import ConnectHandler
import logging
import time
import os
import sys
import datetime
import logging

date = datetime.datetime.now()
date = datetime.datetime.now()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)




myswitch = []

#Above is the switch IP list, every switch ip that is listed in here is going to get SSH'd into. 

def ssh(username, password, myswitch):
    show_vlan = ("show vlan | inc xxx")

    device_type = 'cisco_ios'
    net_connect = ConnectHandler(host=myswitch, username=username, password=password, device_type=device_type)
    logger.info(myswitch)
    print("Establishing Connection to : "+myswitch)
    time.sleep(10)
    print("Checking for WAPS")
    wap_check = net_connect.send_command(show_vlan)
    logger.info(wap_check)
    port = wap_check[wap_check.find("Gi"):]
    port = port[:port.find("\n")]
    port = port.split(',')
    for gig_port in port:
        print('Checking if the port is a Trunk.')
        trunk_chk = net_connect.send_command("show interfaces trunk | inc "+ gig_port)
        logger.info(trunk_chk)
        print(trunk_chk)

        if not "trunking" in trunk_chk:
            flash_port = ('int '+gig_port, 'shutdown','no shutdown')
            print("Shutting port : "+gig_port+" on switch : "+myswitch)
            time.sleep(5)
            shut = net_connect.send_config_set(flash_port)
            logger.info(shut)
            print(shut)
            time.sleep(1)
            status = net_connect.send_command('show int status | inc '+gig_port)
            logger.info(status)
            #print(status)
            time.sleep(1)


username = ('')
password = ('')


for i, d in enumerate(myswitch):
    ssh(username, password, d)
