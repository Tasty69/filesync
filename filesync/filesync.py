#!/usr/bin/env python3
import os
from os import path
from dirsync import sync
import logging
from datetime import datetime
import argparse     

def parse_args():
    parser = argparse.ArgumentParser(description="Sync source and destination directories")
    parser.add_argument("-v","--verbose", action="store_true")
    parser.add_argument("-p","--purge", action="store_true")
    parser.add_argument("-c","--create", action="store_true")
    parser.add_argument("-s","--source", default="/Users/sam/source_test")
    parser.add_argument("-d","--destination", default="/Users/sam/destination_test")
    parser.add_argument("-a","--action", default="sync", choices=["sync","diff","update"])

    return parser.parse_args()

def init_logfile(ScriptName):
    now = datetime.now()
    timestamp = now.strftime("%d%m%Y_%H%M%S")
    #ScriptName = 'filesync'
    ScriptLogDir = f'/Users/sam/ScriptLogs/{ScriptName}/'
    _LogFile = f'{ScriptLogDir}{ScriptName}_{timestamp}.log'

    if path.exists(ScriptLogDir) != True:
        os.makedirs(ScriptLogDir)

    if path.exists(_LogFile) != True:
        open(_LogFile, 'w')

    logging.basicConfig(
        filename=_LogFile,
        encoding='utf-8',
        level=logging.DEBUG
    )       

def main(args):
    
    init_logfile('filesync')

    if args.create != True and path.exists(args.destination) != True:
        print(f'[ERROR] Destination "{args.destination}" does not exist and create "-c" option not selected')
        logging.error(f'Destination "{args.destination}" does not exist and create "-c" option not selected')
        exit(0)
    elif path.exists(args.source) != True:
        print(f'[ERROR] Source "{args.source}" - Does not exist!')
        logging.error(f'Source "{args.source}" - Does not exist!') 
        exit(0)
    else:
        sync(
            args.source,
            args.destination,
            args.action,
            verbose=args.verbose,
            purge=args.purge,
            create=args.create,
            logger=logging
        )
        
if __name__ == "__main__":
    args = parse_args()
    main(args)  



    

  



