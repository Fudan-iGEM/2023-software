"""
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@File : pack.py
@Author : Zhiyue Chen
@Time : 2023/7/21 19:41
"""
import os
import shutil

print('moving files...')
dir_list = ["webUI/template", "webUI/static"]
for dir_name in dir_list:
    try:
        shutil.rmtree(dir_name)
    except:
        pass
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
for file in os.listdir("webUI/dist"):
    if ".html" in file:
        shutil.move(os.path.join("webUI/dist", file), "webUI/template")
for file in os.listdir("webUI/dist"):
    shutil.move(os.path.join("webUI/dist", file), "webUI/static")
shutil.rmtree("webUI/dist")