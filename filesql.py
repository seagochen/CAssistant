#!/bin/env python3
"""
Tora database
"""

# siki
from siki.basics.FileUtils import *
from siki.basics.Exceptions import *
from siki.basics.Hashcode import *

# self-defined
from utilities import *

# defaults
import csv
import os

def create_tora_db():
    config = read_config()
    db_config = config['conf']['toradb']

    # invalid check
    if db_config is None:
        raise InvalidParamException('db config is invalid')

    # create if not exists
    if not os.path.isfile(db_config):
        touch_file(db_config)



def load_tora_db():
    """
    load tora db
    """
    config = read_config()
    db_config = config['conf']['toradb']

    # invalid check
    if db_config is None:
        raise InvalidParamException('db config is invalid')

    # load data from db
    db = {}
    with open(db_config, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            db[row[0]] = row[1]

    # return to caller
    return db


def update_file_hash_code(filename, db):
    """
    load data from file, and generate file hash code
    """
    # calculate file md5
    md5 = compute_file_md5(filename)

    # check original filename md5
    omd5 = ""
    if filename in db.keys():
        omd5 = db[filename]

    # not record this file
    if omd5 is None:
        db[filename] = md5
        return True
    if md5 != omd5:
        db[filename] = md5
        return True
    
    return False



def write_tora_db(db):
    """
    write update back to file
    """

    config = read_config()
    db_config = config['conf']['toradb']

    # invalid check
    if db_config is None:
        raise InvalidParamException('db config is invalid')

    # write back
    with open(db_config, 'w') as f:
        writer = csv.writer(f)
        for key, val in db.items():
            writer.writerow([key, val])