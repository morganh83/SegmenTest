#!/usr/bin/env python3
# Author: Morgan Habecker 
import sys
import subprocess
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Perform a network segmentation test against a client network or networks')
    parser.add_argument('-i', '--ip', help='Test a Single IP')
    parser.add_argument('-c', '--cidr', help='CIDR address to test')
    parser.add_argument('-f', '--file', help='File containing IP addresses in CIDR or single format')
    parser.add_argument('-s', '--stop', help='Stop the script after the first failed test', action='store_true')
    parser.add_argument('-v', '--verbose', help='Display the IP addresses of the hosts that responded to the tests', action='store_true')
    args = parser.parse_args()
    return args

def ping_sweep(ip):
    args = parse_args()
    print("Performing ping sweep on IP address(es) " + ip + "\n")
    ping_sweep_results = subprocess.run(["nmap", "-sn", ip], stdout=subprocess.PIPE)
    ping_sweep_results = ping_sweep_results.stdout.decode('utf-8')
    ping_sweep_results = ping_sweep_results.split('Nmap scan report for ')
    ping_sweep_results.pop(0)
    ping_sweep_results = [i.split(' ')[0] for i in ping_sweep_results]
    ping_sweep_results = [i.split('\n')[0] for i in ping_sweep_results]
    ping_sweep_results = [i for i in ping_sweep_results if i != '']
    if ping_sweep_results:
        if args.verbose:
            if ping_sweep_results:
                print("\033[91mFAIL: The following IP address(es) responded to the ping sweep:\033[0m")
                for i in ping_sweep_results:
                    print("\033[91m" + i + "\033[0m")
        elif args.stop:
            if ping_sweep_results:
                for i in ping_sweep_results:
                    print("\033[91mFAIL: " + i + " Moving on the next IP Address(es)\033[0m\n")
                    # move on to the next IP address
                    return
        else:
            print("\033[91mFAIL: Hosts responded to the ICMP requests. The network is not properly segmented!\033[0m\n")
    else:
        print("\033[92mPASS: No hosts responded to the ping sweep\033[0m")
    with open('ping_sweep.txt', 'w') as f:
        for i in ping_sweep_results:
            f.write(i + '')
    print('\n')
    return ping_sweep_results

def port_scan(ip):
    args = parse_args()
    print("Performing port scan on IP address(es) " + ip + "\n")
    port_scan_results = subprocess.run(["nmap", "-sS", ip], stdout=subprocess.PIPE)
    port_scan_results = port_scan_results.stdout.decode('utf-8')
    port_scan_results = port_scan_results.split('Nmap scan report for ')
    port_scan_results.pop(0)
    port_scan_results = [i.split(' ')[0] for i in port_scan_results]
    port_scan_results = [i.split('\n')[0] for i in port_scan_results]
    port_scan_results = [i for i in port_scan_results if i != '']
    if port_scan_results:
        if args.verbose:
            if port_scan_results:
                print("\033[91mFAIL: The following IP address(es) responded to the port scan:\033[0m")
                for i in port_scan_results:
                    print("\033[91m" + i + "\033[0m")
        elif args.stop:
            if port_scan_results:
                for i in port_scan_results:
                    print("\033[91mFAIL: " + i + " Moving on the next IP Address(es)\033[0m\n")
                # move on to the next IP address
                return
        else:
            print("\033[91mFAIL: Hosts responded to the port scan. The network is not properly segmented!\033[0m\n")
    else:
        print("\033[92mPASS: No hosts responded to the port scan!\033[0m")    
    with open('port_scan.txt', 'w') as f:
        for i in port_scan_results:
            f.write(i + '')
    print('\n')
    return port_scan_results

def main():
    args = parse_args()
    parser = argparse.ArgumentParser()
    if args.ip:
        ip = args.ip
        ping_sweep(ip)
        port_scan(ip)
    elif args.cidr:
        ip = args.cidr
        ping_sweep(ip)
        port_scan(ip)
    elif args.file:
        with open(args.file) as f:
            ip_list = f.read().splitlines()
        for ip in ip_list:
            ping_sweep(ip)
            port_scan(ip)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()

