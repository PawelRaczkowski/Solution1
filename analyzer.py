from scapy.all import *
import socket
class Analyzer():
    def __init__(self,connection_scenario = None, analyze_file = None) -> None:
        self.connection_scenario = connection_scenario
        if analyze_file is None:
            self.analyze_file = self.connection_scenario.output_file
        else:
            self.analyze_file = analyze_file
        self.vpn_servers_ips = []
        self.default_gateway_ip = "192.168.0.1" # my case - to consider- what happens in container
        for vpn_server in self.connection_scenario.vpn_servers:
            self.vpn_servers_ips.append(socket.gethostbyname(vpn_server)) ## analyze based on IPs not on FQDns
        
        
    
    def run_analyzer(self):
        scapy_cap = rdpcap(self.analyze_file)
        for packet in scapy_cap:
            if (packet[scapy.IP].src not in self.vpn_servers_ips) or (packet[scapy.IP].dst not in self.vpn_servers_ips) or (packet[scapy.IP].src == self.default_gateway_ip
                                                                                                                            or (packet[scapy.IP].dst) == self.default_gateway_ip):
                print("Found leak in VPN Traffic in case of Connection Scenario Type: {}".format(self.connection_scenario.type))
