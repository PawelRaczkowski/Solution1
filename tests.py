import requests
import time
import subprocess

class Test():
    def __init__(self) -> None:
        self.domain_to_test = "google.com"
        self.public_ip_to_ping = "18.66.233.44" #public ip of server where onet.pl is hosted
        self.time_interval = 0.1 # 0.1 second interval between next request to not  Dos the target
        self.no_probes = 20 # no of requests/ICMP packets to send
        self.available_test_types = ["DNS", "IP"]

    def run_test(self,test):
        if test == "all":
            for test_type in self.available_test_types:
                self.run_leak_test(test_type)
        else:
            self.run_leak_test(test)

    def run_leak_test(self,test_type):
        command = None
        if test_type == "DNS":
            command = ["nslookup" , self.domain_to_test]
        elif test_type == "IP":
            command = ["ping", "-c", "3", self.public_ip_to_ping]
        for i in range(self.no_probes):
            subprocess.run(command,stdout=subprocess.PIPE)
            time.sleep(self.time_interval)
    

