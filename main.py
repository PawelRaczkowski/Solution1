import argparse
from connection_scenario import ConnectionScenario
from analyzer import Analyzer

def main():
    parser = argparse.ArgumentParser(description='Leak Test Script')
    parser.add_argument('tests', help='Tests to perform (IP,DNS,all)', type=lambda s: [item for item in s.split(',')],)
    parser.add_argument("connection_scenario", help='Connection scenario (1- stable VPN, 2 - change VPN to other, 3 - disconnect and reconnect)',
                         type=lambda s: [int(item) for item in s.split(',')])
    parser.add_argument('--analyze', help='Analyze results after test conduction',
                         type=bool)
    parser.add_argument('--analyze_file', help='Analyze results from pcap file',
                         type=str)
    args = parser.parse_args()

    ConnectionScenario.nordvpn_login()
    for scenario in args.connection_scenario:
        cs = ConnectionScenario(scenario,args.tests)
        cs.run_connection_scenario()
        if args.analyze:
            analyzer = Analyzer(connection_scenario=cs)
            analyzer.run_analyzer()
    ConnectionScenario.nordvpn_logout()
    if args.analyze_file:
        analyzer = Analyzer(analyze_file=args.analyze_file)
        analyzer.run_analyzer()

if __name__== "__main__":
    main()