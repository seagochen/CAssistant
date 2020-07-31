#!/bin/env python3
# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Jul 26, 2020
# Modified: Jul 28, 2020

"""
Tora database
"""

from siki.basics import FileUtils
from siki.basics import Hashcode
from siki.basics import TimeTicker
from siki.basics import Exceptions

import pandas

TORA_CSV = ".tora/data.csv"
TORA_TEMP = ".tora/temp"


class ToraDatabase(object):

    def __init__(self, data=TORA_CSV):
        # create empty folder if not exists
        if not FileUtils.exists(".tora"):
            FileUtils.mkdir(".tora")

        # create empty csv file if not exists
        if not FileUtils.exists(data):
            FileUtils.touch_file(data)

        # trying to load data from csv
        self.frame = pandas.read_csv(data, names=['project', 'filename', 'hash', 'date'])

        print(self.frame)

        # flag
        self.updated = False

    def update_file_info(self, project, file):
        if not FileUtils.isfile(file):
            raise Exceptions.NoAvailableResourcesFoundException("The file does not exist")

        # 计算文件的hash值
        code = Hashcode.compute_file_md5(file)

        # 只保留文件名
        _, leaf = FileUtils.root_leaf(file)
        file = leaf

        # 查找数据同时满足列名为file，和project的数据
        original_column = self.frame.loc[(self.frame['filename'] == file) & (self.frame['project'] == project), 'hash']

        # 没有查找到该文件的原信息
        if len(original_column) <= 0:
            self.frame = self.frame.append({'project': project, 'filename': file,
                                            'hash': code, 'date': TimeTicker.time_now_with_foramt()},
                                           ignore_index=True)
            self.updated = True
            return True

        # 查找到数据，对数据进行比对
        original_code = original_column.values
        original_code = original_code[0]

        # 当前的文件信息跟先前的已经不一致，对数据进行更新
        if code != original_code:
            original_column[original_column.index] = code
            self.frame.update(original_column)
            self.updated = True
            return True

        # 信息是一致的，不做任何操作
        return False

    def save_and_close(self, data=TORA_CSV):
        if self.updated:
            self.frame.to_csv(data, header=False)
