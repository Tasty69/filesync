#!/usr/bin/env python3
"""
This script syncs two directories
"""

import argparse  
import datetime
import dirsync
import logging
import os
import sys
import typing   


def parse_args() -> typing.Any:
    parser = argparse.ArgumentParser(description="Sync source and destination directories")
    parser.add_argument("-v","--verbose", action="store_true")
    parser.add_argument("-p","--purge", action="store_true")
    parser.add_argument("-c","--create", action="store_true")
    parser.add_argument("-s","--source", default="/Users/sam/source_test")
    parser.add_argument("-d","--destination", default="/Users/sam/destination_test")
    parser.add_argument("-a","--action", default="sync", choices=["sync","diff","update"])

    return parser.parse_args()


def init_logging(script_name) -> None:
    now = datetime.datetime.now()
    time_stamp = now.strftime("%d%m%Y_%H%M%S")
    script_log_dir = f'/scriptlogs/{script_name}'
    log_file = f'{script_log_dir}/{script_name}_{time_stamp}.log'

    if not os.path.exists(script_log_dir):
        try:
            os.makedirs(script_log_dir)
            print(f'[INFO] Created {script_log_dir}')
        except Exception as error:
            print(f'[ERROR] Failed to create {script_log_dir}. {error}')
            sys.exit(1)
    if not os.path.exists(log_file):
        try:
            with open(log_file, 'w') as f:
                f.write('')
                f.close()
            print(f'[INFO] Created {log_file}')
        except Exception as error:
            print(f'[ERROR] Failed to create {log_file}. {error}') 
            sys.exit(1)
 
    logging.basicConfig(
    filename=log_file,
    encoding='utf-8',
    level=logging.DEBUG
    )


def main(args) -> int:

    init_logging('filesync')

    if args.create != True and os.path.exists(args.destination) != True:
        print(f'[ERROR] Destination "{args.destination}" does not exist and create "-c" option not selected')
        logging.error(f'Destination "{args.destination}" does not exist and create "-c" option not selected')
        sys.exit(1)
    elif os.path.exists(args.source) != True:
        print(f'[ERROR] Source "{args.source}" - Does not exist!')
        logging.error(f'Source "{args.source}" - Does not exist!') 
        sys.exit(1)
    else:
        try:
            dirsync.sync(
                args.source,
                args.destination,
                args.action,
                verbose=args.verbose,
                purge=args.purge,
                create=args.create,
                logger=logging
            )
        except Exception as error:
            print(f'Dirsync failed. {error}')
            sys.exit(1)    


if __name__ == "__main__":
    args = parse_args()
    main(args)  
    sys.exit(main(args))



    

  



