#!/bin/env python3

def read_config(config_file="./Tora/project.conf"):
    import configparser
    config = configparser.RawConfigParser()
    config.read(config_file)
    return config