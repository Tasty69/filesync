#!/usr/bin/python3
import os
import subprocess
from os import path
from datetime import datetime
import argparse
import dnf

def parse_args():
    parser = argparse.ArgumentParser(description="Set fan speed on Dell PowerEdge via IPMI")
    parser.add_argument("-d", "--drac", default="r510", choices=["r510", "r710"])
    parser.add_argument("-s","--speed", default="low", choices=["low","medium","high"])
    parser.add_argument("-u", "--username", default="root")
    parser.add_argument("-p", "--password", default="calvin")

    return parser.parse_args()

def main():
    args = parse_args()

    # Define Drac IP
    if args.drac == "r510":
        IPAddress = '192.168.165.48'
    elif args.drac == "r710":
        IPAddress = '192.168.165.49' 

    # Define Fan Speed
    if args.speed == "low":
        hex_speed = "0x02 0xff 0x00"
    elif args.speed == "medium":
        hex_speed = "0x02 0xff 0x05"
    elif args.speed == "high":
        hex_speed = "0x02 0xff 0x10"


    # Set Fan Control to Manual
    os.system(f'/bin/ipmitool -H {IPAddress} -U {args.username} -P {args.password} raw 0x30 0x30 0x01 0x00')
    print(f'[INFO] Set fan control for {args.drac} to manual')

    # Set Fan Speed
    os.system(f'/bin/ipmitool -H {IPAddress} -U {args.username} -P {args.password} raw 0x30 0x30 {hex_speed}')
    print(f'[INFO] Set fan speed for {args.drac} to {args.speed}')

if __name__ == "__main__":
    main()