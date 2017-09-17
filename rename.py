# -*- coding: utf-8 -*-

import os
import os.path

def tagsModify(old):
    new = old.replace('categories', 'tags')
    new = new.replace('"', '[', 1)
    new = new.replace('"', ']', 1)
    return new

path = 'hexo/source/_posts'

for root, dirs, filenames in os.walk(path):
    pass

for filename in filenames:
    article = open(path + '/' + filename, 'r')
    lines = article.readlines()
    article.close()
    article = open(path + '/' + filename, 'w')
    for line in lines:
        if line.startswith('categories'):
            line = tagsModify(line)
        article.write(line)
    article.close()
