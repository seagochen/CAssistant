#!/bin/env python3

from convert import ListConvert
import os

def read_config(config_file="./Tora/project.conf"):
    import configparser
    config = configparser.RawConfigParser()
    config.read(config_file)
    return config


def search_output(config_dict):
    o_temp = config_dict['temp']['tmp_path']
    o_type = config_dict['gen']['type']
    o_output = config_dict['gen']['output']
    o_compiler = config_dict['gen']['compiler']

    if o_type == 'static':
        return "ar -rcs {} {}/*.o".format(o_output, o_temp)

    if o_type == 'share':
        return "{} -shared -fPIC {}/*.o -o lib{}".format(o_compiler, o_temp, o_output)

    if o_type == 'exe':
        return "{} {}/*.o -o {}".format(o_compiler, o_temp, o_temp)


if __name__ == "__main__":
    config = read_config()
    cmd = search_output(config)
    os.system(cmd)
    print("exec", cmd)
    