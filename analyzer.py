from scapy.all import *
import socket
import ipaddress
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
            if not self.analyze_packet(packet):
                print("Found potential leak VPN traffic issue in connection scenario type {}".format(self.connection_scenario.type))

    def analyze_packet(self,packet):
        if (ipaddress.ip_address(packet[scapy.IP].src).is_private and packet[scapy.IP].src != self.default_gateway_ip) or (ipaddress.ip_address(packet[scapy.IP].dst).is_private and packet[scapy.IP].dst != self.default_gateway_ip):
            return True
        if packet[scapy.IP].src == self.default_gateway_ip or packet[scapy.IP].dst == self.default_gateway_ip:
            return False
        if packet[scapy.IP].src not in self.vpn_servers_ips or packet[scapy.IP].dst not in self.vpn_servers_ips:
            return False