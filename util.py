# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 09:49:14 2020

@author: Chan Chak Tong
"""

import os

class Utility:
    @staticmethod
    def save_data(data, data_path=r'./data.txt'):
        assert isinstance(data, (list, tuple)), 'Invalid type of data'
        with open(data_path, 'w') as streamer:
            for (name, path) in data:
                streamer.write('%s-!-%s\n' % (name, path))
    
    @classmethod
    def load_data(self, data_path=r'./data.txt'):
        if not os.path.isfile(data_path):
            self.save_data([])
        with open(data_path, 'r') as streamer:
            data = streamer.read().splitlines()
        return list(map(lambda s: s.split('-!-'), data))