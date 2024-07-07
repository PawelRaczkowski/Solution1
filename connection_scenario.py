import subprocess
import time
from tests import Test
import os

class ConnectionScenario():
    def __init__(self,type,tests) -> None:
        self.current_server_vpn = "" # will be filled based on the domain name of VPN server
        self.vpn_servers = [] # for analyze purposes
        self.second_server_vpn = "Kenya" #whatever other than Poland
        self.country_code = ""
        self.vpn_servers.append(self.second_server_vpn)
        self.tests = tests
        self.type = type
        self.output_file = ""
        self.test_handler = Test()

    @staticmethod
    def nordvpn_login(self):
        access_token = "e9f2ab0312fc5b6914c2ab938c47c7ecb40e49876bd2a46285ebac5d45fe925a"
        login_command = ["nordvpn", "login", "--token", access_token]
        result = subprocess.run(login_command, stdout=subprocess.PIPE)

    @staticmethod
    def nordvpn_logout(self):
        logout_command = ["nordvpn", "logout"]
        result = subprocess.run(logout_command, stdout=subprocess.PIPE)

    def run_connection_scenario(self):
        if self.type == 1:
            self.run_stable_vpn_test()
        elif self.type == 2:
            self.run_change_gate_to_other_test()
        elif self.type == 3:
            self.run_disconnect_reconnect_test()
    

    def run_stable_vpn_test(self):
        pid_tcpdump, connect_command = self.start_connection_scenario()
        for test in self.tests:
            self.test_handler.run_test(test)
        self.clear_connection_scenario(pid_tcpdump)

    def run_change_gate_to_other_test(self):
        pid_tcpdump, connect_command = self.start_connection_scenario()
        for test in self.tests:
            connect_command.append(self.second_server_vpn)
            result = subprocess.Popen(connect_command,stdout=subprocess.PIPE) # parallelly run connection command and testing cases
            self.test_handler.run_test(test)
        self.clear_connection_scenario(pid_tcpdump)

    def run_disconnect_reconnect_test(self): #to the same vpn server basing on country code
        pid_tcpdump,connect_command = self.start_connection_scenario()
        for test in self.tests:
            disconnect_command = ["nordvpn", "disconnect"]
            result = subprocess.Popen(disconnect_command,stdout=subprocess.PIPE)
            connect_command.append(self.country_code) # make sure that it will connect to the same server
            result = subprocess.Popen(connect_command,stdout=subprocess.PIPE) # parallelly run connection command and testing cases
            self.test_handler.run_test(test)
        self.clear_connection_scenario(pid_tcpdump)

    def run_tcpdump_collector(self): # it is used for each connection scenario as well as to manual checking
        filename = time.strftime("%Y%m%d_%H%M%S")+"_"+self.type
        collector_command = ["sudo", "tcpdump", "-i", "1", "-w", filename]
        result = subprocess.Popen(collector_command,stdout=subprocess.PIPE)
        return result.pid, filename
    
    def get_vpn_server_name(self,result): 
        cleared_result = result.replace('\r',"").replace('\n',"")
        server_name_vpn = cleared_result.split(" ")[-3]
        return server_name_vpn.replace("(","").replace(")","").replace("!","").replace("-","")
    
    def clear_connection_scenario(self, pid_tcpdump):
        os.kill(pid_tcpdump)
        disconnect_command = ["nordvpn", "disconnect"]
        result = subprocess.run(disconnect_command,stdout=subprocess.PIPE)
    
    def start_connection_scenario(self):
        pid_tcpdump, output_file = self.run_tcpdump_collector()
        self.output_file = output_file
        connect_command = ["nordvpn", "connect"]
        result = subprocess.run(connect_command,stdout=subprocess.PIPE)
        vpn_server_name = self.get_vpn_server_name(result.stdout.decode('utf-8'))
        self.country_code = vpn_server_name.split(".")[0] # format country_code.nordvpn.com
        if vpn_server_name not in self.vpn_servers:
            self.vpn_servers.append(vpn_server_name)
        return pid_tcpdump, connect_command