#!/usr/bin/env python3

from logging import getLogger,ERROR
getLogger('scapy.runtime').setLevel(ERROR)

##WARN THINGS
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn



from scapy.all import TCP,IP,sr1
from threading import Thread
from time import sleep, time
from ipaddress import IPv4Network
from signal import SIGINT,SIG_DFL,signal
from argparse import ArgumentParser
from termcolor import colored




class zombie_scanner():
    
    
    def __init__(self,target):
        self.target = target


    
    def zombie_check(self):
        start_id = 0
        end_id = 0
        difference = 0
        
        try:
            
            pkt = sr1(IP(dst=self.target)/TCP(dport=80,flags='SA'),verbose=False,timeout=2)
            start_id = int(pkt[IP].id)

            pkt = sr1(IP(dst=self.target)/TCP(dport=80,flags='SA'),verbose=False,timeout=2)
            end_id = int(pkt[IP].id)
            
            difference = end_id - start_id
            
            
            if difference == 1 or difference == 2:
                return True
            
            
            
        except TypeError:
            pass







if __name__ == '__main__':

    thread = []
    zombie_found = []
    start = time()
    
    pars = ArgumentParser(prog='./zombie_check')
    
    pars.add_argument('-t',dest='target', required=True,
                help='set the host to check for idle')
    
    arg = pars.parse_args()
    
    

    def zombie_check(possible_zombie):
        start_id = 0
        end_id = 0
        difference = 0
        
        try:
            
            pkt = sr1(IP(dst=possible_zombie)/TCP(dport=80,flags='SA'),verbose=False,timeout=4)
            start_id = int(pkt[IP].id)

            pkt = sr1(IP(dst=possible_zombie)/TCP(dport=80,flags='SA'),verbose=False,timeout=4)
            end_id = int(pkt[IP].id)
            
            difference = end_id - start_id
            
            
            if difference == 1 or difference == 2:
                print(colored(f'[+] host: {possible_zombie} is a crawler RUN!! ','green'))
            
            
        except TypeError:
            sleep(1)    
        
        
        


    signal(SIGINT, SIG_DFL) 
    print(colored(f'[*] time to find some crawler','yellow'))
    
    
    
    for ip in IPv4Network(arg.target).hosts():
        t = Thread(target=zombie_check,args=(str(ip),))
        thread.append(t)
        t.start()
        sleep(0.2)
        
    for i in thread:
        i.join()
       
       
    print(colored(f'\ntime {time()-start:.5}\n','yellow'))
    
    
    
    