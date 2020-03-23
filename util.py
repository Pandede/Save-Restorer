# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 09:49:14 2020

@author: Chan Chak Tong
"""

class Utility:
    @staticmethod
    def save_data(data, data_path=r'./data.txt'):
        assert isinstance(data, (list, tuple)), 'Invalid type of data'
        with open(data_path, 'w') as streamer:
            for (name, path) in data:
                streamer.write('%s-!-%s\n' % (name, path))
    
    @staticmethod
    def load_data(data_path=r'./data.txt'):
        with open(data_path, 'r') as streamer:
            data = streamer.read().splitlines()
        return list(map(lambda s: s.split('-!-'), data))