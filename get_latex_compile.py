# for Large not large.

# with open("mm.txt","r",encoding="utf-8") as f:
#     full_page_str=f.read()
#
# full_page_len=hans_count(full_page_str)
# print("full page:",full_page_len)
# # maxmimum: 442 字数

## 诗歌数了一下大概最多是26行

import re
import os
import shutil

proper_essay_word_cnt=380
proper_poem_line_cnt=16
essay_too_short=15
poem_too_short=5

poem_or_essay=""

def hans_count(str):
    # 数一数中文字数
    hans_total = 0
    for s in str:
        if '\u4e00' <= s <= '\u9fef':
            hans_total += 1
    return hans_total

def idx_comp(poem_or_essay,str,idx1,idx2):
    assert idx1<=idx2
    substr=str[idx1:idx2]
    if poem_or_essay == "poem":
        if hans_count(substr) <= poem_too_short:
            return idx1
        else:
            return idx2
    elif poem_or_essay == "essay":
        if hans_count(substr) <= essay_too_short:
            return idx1
        else:
            return idx2

def process(poem_or_essay,filename):
    if poem_or_essay == "essay":
        with open ("./text_files/{}.txt".format(filename), "r", encoding="utf-16-le") as f:
            full_article_str = f.read ()
        head_idx=0
        essay_insert=open("./stable/essay_insert.txt","r",encoding="utf-8").read()
        # idxs=[]
        new_str=""
        para_idxs=[m.start() for m in re.finditer('\n\n', full_article_str)]
        for idx,word in enumerate(full_article_str):
            my_slice=full_article_str[head_idx:idx]
            new_str+=word
            if hans_count(my_slice) >= proper_essay_word_cnt:
                print("head:{}\tnow:{}".format(head_idx,idx))
                new_str+=essay_insert
                # idxs.append(idxs)
                head_idx=idx
        essay_head=open("./stable/essay_head.txt","r",encoding="utf-8").read()
        new_str=essay_head+new_str
        with open("./text_files/{}-2.txt".format(filename),"w",encoding="utf-8") as f:
            f.write(new_str)

    if poem_or_essay == "poem":
        with open("./text_files/{}.txt".format(filename),"r",encoding="utf-16-le") as f:
            lines=f.readlines()

        head_idx=0
        new_lines=[]
        poem_insert=open("./stable/poem_insert.txt","r",encoding="utf-8").readlines()
        for idx,line in enumerate(lines):
            line=line.replace("\n"," \\\\\n")
            cnt=idx-head_idx
            new_lines.append(line)
            if cnt >= proper_poem_line_cnt:
                new_lines.extend(poem_insert)
                head_idx=idx
        new_lines_s="".join(new_lines)
        # print(new_lines_s)
        poem_head=open("./stable/poem_head.txt","r",encoding="utf-8").read()
        poem_bottom=open("./stable/poem_bottom.txt","r",encoding="utf-8").read()
        new_lines_s=poem_head+new_lines_s+poem_bottom
        with open("./text_files/{}-2.txt".format(filename),"w",encoding="utf-8") as f:
            f.write(new_lines_s)


# process("essay","ee")
# os._exit(0)

if __name__ == "__main__":
    title=input("题目:")
    author=input("作者:")
    date=input("日期:(英文空格隔开)").replace(" ","-")
    pe=input("p or e (poem or essay):")
    if pe == "e":
        print("e")
        poem_or_essay = "essay"
    elif pe == "p":
        print("p")
        poem_or_essay = "poem"
    filename=input("filename:")
    print(poem_or_essay)
    process(poem_or_essay,filename)

    with open("./stable/poem_essay_template.tex","r",encoding="utf-8") as f:
        lines_s=f.read()

    with open("./text_files/{}-2.txt".format (filename), "r", encoding="utf-8") as f:
        content=f.read()

    new_s=lines_s
    new_s1=new_s.replace("<Your-Title>",title)
    # print(new_s1)
    new_s2=new_s1.replace("<Your-Author>",author)
    new_s3=new_s2.replace("<Your-Date>",date)
    new_s4=new_s3.replace("<Your-Content>",content)

    # print(new_s4)

    with open("./text_files/output.tex","w", encoding="utf-8") as f:
        f.write(new_s4)
    
    record_name="{}-{}".format(title,author)

    ori_dir=os.getcwd()
    os.chdir("records")
    os.mkdir(record_name)
    os.chdir(record_name)

    shutil.copyfile("../../text_files/{}.txt".format(filename),"{}.txt".format(title))
    shutil.copyfile("../../text_files/output.tex","{}.tex".format(title))

    os.chdir(ori_dir)
    os.system("cd ./text_files && xelatex output.tex && move output.pdf ../ && del output* *.txt")
    shutil.copyfile("output.pdf", "records/{}/{}.pdf".format(record_name,title))

    print("done.")
    # os.system("cd ./text_files")