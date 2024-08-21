import re
import os
import shutil
import sys

def get_title_infos():
    title=input("题目:")
    author=input("作者:")
    date=input("日期:（英文空格隔开）（都没有就直接回车）").replace(" ","-")
    pe_flag=0
    while pe_flag == 0:
        pe=input("p or e (poem or essay):")
        if pe == "e":
            poem_or_essay = "essay"
            pe_flag=1
        elif pe == "p":
            poem_or_essay = "poem"
            pe_flag=1
    filename=input("filename(no .txt prefix inside!):")
    url=input("网页链接：（最好是archive后的）")
    title_infos = {
        '<Your-Title>':title,
        '<Your-Author>':author,
        '<Your-Date>':date,
        'poem_or_essay':poem_or_essay,
        'filename':filename,
        '<Your-Url>':url,
    }
    return title_infos

if __name__ == '__main__':
    title_info_dict = get_title_infos()
    