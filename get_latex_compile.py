# for Large not large.

# with open("mm.txt","r",encoding="utf-8") as f:
#     full_page_str=f.read()
#
# full_page_len=hans_count(full_page_str)
# print("full page:",full_page_len)

import re
import os
import shutil
import sys

# large 状态下经常出格，不知道怎么办才好
# 试过多次是这个16 21 最合适
proper_essay_word_cnt=380
# proper_article_line_cnt_firstpage=16-3
# proper_article_line_cnt=21-3

# essay_too_short=15
# poem_too_short=5
essay_word_per_line=23
# proper_article_line_cnt_firstpage=17-2
# proper_article_line_cnt=23-2

# poem_word_per_line=11
poem_word_per_line=23

# proper_article_line_cnt_firstpage=proper_article_line_cnt_firstpage
# proper_article_line_cnt=proper_article_line_cnt

proper_article_line_cnt_firstpage=17-2
proper_article_line_cnt=23-2


poem_or_essay=""

essay_insert=open("./stable/essay_insert.txt","r",encoding="utf-8").read()
essay_head=open("./stable/essay_head.txt","r",encoding="utf-8").read()
poem_inserts=open("./stable/poem_insert.txt","r",encoding="utf-8").readlines()
poem_insert=open("./stable/poem_insert.txt","r",encoding="utf-8").read()
poem_head=open("./stable/poem_head.txt","r",encoding="utf-8").read()
poem_bottom=open("./stable/poem_bottom.txt","r",encoding="utf-8").read()

poem_insert=essay_insert
# poem_insert=open("./stable/poem_insert3.txt","r",encoding="utf-8").read()
poem_head="\setlength\parindent{0pt}\n\n"+essay_head
poem_bottom=""

std_xml_pack=open("./stable/std_audio_pack.xml","r",encoding="utf-8").read()

# thank you so much for your wonderful help!
# https://github.com/skygongque/tts
#  
tts_py_path="./tts/python_cli_demo/tts.py"

def xml_pack(words):
    return std_xml_pack.replace("<Your-Words>", words)

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

def process2(poem_or_essay,filename):
    if poem_or_essay=="essay":
        word_cnt=2
        article_word_per_line=essay_word_per_line
        article_insert=essay_insert
        article_head=essay_head
        article_bottom=""
        # proper_article_line_cnt_firstpage=proper_article_line_cnt_firstpage
        # proper_article_line_cnt=proper_article_line_cnt
    elif poem_or_essay=="poem":
        word_cnt=0
        article_word_per_line=poem_word_per_line
        article_insert=poem_insert
        article_head=poem_head
        article_bottom=poem_bottom
        # proper_article_line_cnt_firstpage=proper_article_line_cnt_firstpage
        # proper_article_line_cnt=proper_article_line_cnt

    try:
        with open ("./text_files/{}.txt".format(filename), "r", encoding="utf-16-le") as f:
            full_article_str = f.read ()
    except Exception:
        with open ("./text_files/{}.txt".format(filename), "r", encoding="utf-8") as f:
            full_article_str = f.read ()
    head_idx=0
    
    # idxs=[]
    new_str=""
    para_idxs=[m.start() for m in re.finditer('\n\n', full_article_str)]

    # 开头空两格
    article_lines=[]
    last_idx=0
    print(para_idxs)
    cur_line=""
    ori_word_cnt=word_cnt
    print(full_article_str)
    for idx,word in enumerate(full_article_str):
        word_cnt+=1
        cur_line+=word
        # print(cur_line)
        if word_cnt % article_word_per_line == 0:
            article_line=full_article_str[last_idx:idx]
            article_lines.append(article_line)
            last_idx=idx
            cur_line=""
            
        if idx in para_idxs or word=="\n":
            article_line=full_article_str[last_idx:idx]
            if idx in para_idxs:
                article_line=article_line+r" \par "
                article_lines.append("\n")
            if not article_line in article_lines:
                article_lines.append(article_line)
            word_cnt=ori_word_cnt
            last_idx=idx
            cur_line=""
    
    if cur_line!="":
        print("bottom:",cur_line)
        # 尾部的人赶紧上车
        article_line=cur_line
        article_lines.append(article_line)
    
    new_lines=[]
    for i,al in enumerate(article_lines,1):
        print(al,"\t",i)
        if poem_or_essay == "poem":
            # print(al.find("\n\n"))
            # al=al.replace("\n\n", r" \par ")
            al=al.replace("\n", "\\\\\n") if al!="\n" else al
        if i - proper_article_line_cnt_firstpage == 0 or (i - proper_article_line_cnt_firstpage) % proper_article_line_cnt == 0:
            new_al=al+article_insert
            new_lines.append(new_al)
        else:
            new_lines.append(al)
    
    # for i,al in enumerate(new_lines):
    #     # if poem_or_essay=="poem":
    #     #     if hans_count(al)!=0:
    #             new_al=al.replace("\n"," \\\\\n") if  al!="\n" else al
    #             new_lines[i]=new_al
        # print(al,"\t"*3,i+1)
    # sys.exit(0)
    new_str="".join(new_lines)

    # 前三个是给poem的，最后一个是给essay 的
    new_str=new_str.replace("\\par \n\\\\", "\\\\ \n\n")
    new_str=new_str.replace("\\par \\\\", "\\\\ \n\n")
    new_str=new_str.replace("\n\\newpage\n\\\\", "\\\\\n\\newpage\n")
    new_str=new_str.replace("\\par \n", "\n\n")
    new_str=new_str.replace("\\par ", "\n\n")

        # new_str.replace(" \par ", "\n\n")
        

        # new_str=article_head+new_str+article_bottom
        # with open("./text_files/{}-2.txt".format(filename),"w",encoding="utf-8") as f:
        #     f.write(new_str)
        # sys.exit(0)

        # if poem_or_essay == "poem":
        #     para_idxs=[]
        #     print("para-idx:",para_idxs)
        #     new_lines2=new_str.split("\n")
        #     for i,nl2 in enumerate(new_lines2):
        #         if hans_count(nl2)>0:
        #             new_nl2=nl2+" \\\\\n"
        #             new_lines2[i]=new_nl2
        #         if i in para_idxs:
        #             new_lines2[i]=new_lines2[i]+"\n\n"
        #     new_str="".join(new_lines2)
        # print(new_lines[0:20])
        #     print(el,"\t",i)
        # print(repr(essay_lines[35]),repr(essay_lines[36]),repr(essay_lines[37]),sep="\n")
        # sys.exit(0)

        # for idx,word in enumerate(full_article_str):
        #     my_slice=full_article_str[head_idx:idx]
        #     new_str+=word
        #     if hans_count(my_slice) >= proper_essay_word_cnt:
        #         print("head:{}\tnow:{}".format(head_idx,idx))
        #         new_str+=essay_insert
        #         # idxs.append(idxs)
        #         head_idx=idx
        # sys.exit(0)
    new_str=article_head+new_str+article_bottom
    with open("./text_files/{}-2.txt".format(filename),"w",encoding="utf-8") as f:
        f.write(new_str)
        
        # sys.exit(0)

# # def process(poem_or_essay,filename):
#     if poem_or_essay == "essay":
#         with open ("./text_files/{}.txt".format(filename), "r", encoding="utf-16-le") as f:
#             full_article_str = f.read ()
#         head_idx=0
        
#         # idxs=[]
#         new_str=""
#         para_idxs=[m.start() for m in re.finditer('\n\n', full_article_str)]

#         # 开头空两格
#         word_cnt=2
#         essay_lines=[]
#         last_idx=0
#         print(para_idxs)
#         cur_line=""
#         for idx,word in enumerate(full_article_str):
#             word_cnt+=1
#             cur_line+=word
#             # print(cur_line)
#             if word_cnt % essay_word_per_line == 0:
#                 essay_line=full_article_str[last_idx:idx]
#                 essay_lines.append(essay_line)
#                 last_idx=idx
#                 cur_line=""
                
#             if idx in para_idxs:
#                 essay_line=full_article_str[last_idx:idx]
#                 if not essay_line in essay_lines:
#                     essay_lines.append(essay_line)
#                 word_cnt=2
#                 last_idx=idx
#                 cur_line=""
        
#         if cur_line!="":
#             print("bottom:",cur_line)
#             # 尾部的人赶紧上车
#             essay_line=cur_line
#             essay_lines.append(essay_line)
        
#         new_lines=[]
#         for i,el in enumerate(essay_lines,1):
#             print(el,"\t",i)
#             if i - proper_article_line_cnt_firstpage == 0 or (i - proper_article_line_cnt_firstpage) % proper_article_line_cnt == 0:
#                 new_el=el+essay_insert
#                 new_lines.append(new_el)
#             else:
#                 new_lines.append(el)
        
#         for i,el in enumerate(new_lines,1):
#             print(el,"\t",i)

#         new_str="".join(new_lines)
#         #     print(el,"\t",i)
#         # print(repr(essay_lines[35]),repr(essay_lines[36]),repr(essay_lines[37]),sep="\n")
#         # sys.exit(0)

#         # for idx,word in enumerate(full_article_str):
#         #     my_slice=full_article_str[head_idx:idx]
#         #     new_str+=word
#         #     if hans_count(my_slice) >= proper_essay_word_cnt:
#         #         print("head:{}\tnow:{}".format(head_idx,idx))
#         #         new_str+=essay_insert
#         #         # idxs.append(idxs)
#         #         head_idx=idx
        
#         new_str=essay_head+new_str
#         with open("./text_files/{}-2.txt".format(filename),"w",encoding="utf-8") as f:
#             f.write(new_str)

#     if poem_or_essay == "poem":
#         with open("./text_files/{}.txt".format(filename),"r",encoding="utf-16-le") as f:
#             lines=f.readlines()

#         head_idx=0
#         new_lines=[]
#         for idx,line in enumerate(lines):
#             line=line.replace("\n"," \\\\\n") if line!="\n" else line
#             cnt=idx-head_idx
#             new_lines.append(line)
#             if cnt - proper_article_line_cnt_firstpage == 0 or (cnt - proper_article_line_cnt_firstpage) % proper_article_line_cnt == 0:
#                 new_lines.extend(poem_inserts)
#                 # head_idx=idx
#         new_lines_s="".join(new_lines)
#         # print(new_lines_s)
#         new_lines_s=poem_head+new_lines_s+poem_bottom
#         with open("./text_files/{}-2.txt".format(filename),"w",encoding="utf-8") as f:
#             f.write(new_lines_s)


# process("essay","ee")
# os._exit(0)

if __name__ == "__main__":
    # 2022年6月27日 22:52:24 诗歌体的居中就是纯纯sb，每行的字数从9-11字不等你让我玩毛？
    title=input("题目:")
    author=input("作者:")
    date=input("日期:（英文空格隔开）（都没有就直接回车）").replace(" ","-")
    pe=input("p or e (poem or essay):")
    if pe == "e":
        # print("e")
        poem_or_essay = "essay"
    elif pe == "p":
        # print("p")
        poem_or_essay = "poem"
    filename=input("filename:")
    url=input("网页链接：（最好是archive后的）")
    # filename="ee"
    print(poem_or_essay)
    process2(poem_or_essay,filename)

    # sys.exit(0)

    with open("./stable/poem_essay_template.tex","r",encoding="utf-8") as f:
        lines_s=f.read()

    with open("./text_files/{}-2.txt".format (filename), "r", encoding="utf-8") as f:
        content=f.read()
    
    # print("\n\nContent:{}".format(content))

    url_str="\\footnote{Click to View:\\url{"+url+"}"+"}"

    title_str=title+url_str

    print(title)

    new_s=lines_s
    new_s1=new_s.replace("<Your-Title>",title_str)
    # print(new_s1)
    new_s2=new_s1.replace("<Your-Author>",author)
    new_s3=new_s2.replace("<Your-Date>",date)
    new_s4=new_s3.replace("<Your-Content>",content)

    # print(new_s4)

    with open("./text_files/output.tex","w", encoding="utf-8") as f:
        f.write(new_s4)
    
    record_name="{}".format(title)
    year=date.split("-")[0]
    new_title="{}-{}-{}".format(title,author,year)

    ori_dir=os.getcwd()
    os.chdir("records")
    if not os.path.exists(record_name):
        os.mkdir(record_name)
    os.chdir(record_name)

    shutil.copyfile("../../text_files/{}.txt".format(filename),"{}.txt".format(new_title))
    shutil.copyfile("../../text_files/output.tex","{}.tex".format(new_title))

    os.chdir(ori_dir)
    if os.path.exists("output.pdf"):
        os.remove("output.pdf")
    os.system("cd ./text_files && xelatex -interaction=nonstopmode output.tex && move output.pdf ../ && del output*")
    # os.system("cd ./text_files && xelatex output.tex && move output.pdf ../ ")
    print("jans?")
    try:
        shutil.copyfile("output.pdf", "records/{}/{}.pdf".format(record_name,new_title))
    except FileNotFoundError:
        shutil.copyfile("./text_files/output.pdf", "output.pdf")
        os.system("cd ./text_files && del output*")
        shutil.copyfile("output.pdf", "records/{}/{}.pdf".format(record_name,new_title))

    shutil.copyfile("output.pdf", "D:/Alldowns/{}.pdf".format(new_title))

    print("jsbd")

    # sys.exit(0)
    
    # voice 

    voice_content=content

    audio_comm_patt="python \"{}\" --input \"{}\" --output \"{}\""
    if poem_or_essay == "essay":
        article_insert=essay_insert
        article_head=essay_head
    elif poem_or_essay == "poem":
        article_insert=poem_insert
        article_head=poem_head
    voice_contents=voice_content.split(article_insert)
    for i,vc in enumerate(voice_contents):
        new_vc=vc.replace(article_head, "")
        if r"\\" in new_vc:
            new_vc=new_vc.replace(r"\\", "")
        print(new_vc)
        # os._exit(0)
        if i == 0:
            new_vc="{}\n{}\n\n".format(title,author)+new_vc
        xml_path="{}-{}.xml".format(new_title,i+1)
        with open(xml_path,"w",encoding="utf-8") as f:
            ap=xml_pack(new_vc)
            f.write(ap)
        audio_path="{}-{}".format(new_title,i+1)
        audio_comm=audio_comm_patt.format(tts_py_path,xml_path,audio_path)
        print("audio comm:",audio_comm)
        os.system(audio_comm)

        new_vc="\n\n\n          === Page {} ===                     \n\n\n".format(i+1)+new_vc
        voice_contents[i]=new_vc
    # elif poem_or_essay == "poem":
    #     # print("vc:",voice_content)
    #     voice_contents=voice_content.split(poem_insert)
    #     for i,vc in enumerate(voice_contents):
    #         new_vc=vc.replace(poem_head, "").replace(r" \\", "")
    #         if i == 0:
    #             new_vc="{}\n{}\n\n".format(title,author)+new_vc
    #         xml_path="{}-{}.xml".format(new_title,i+1)
    #         with open(xml_path,"a",encoding="utf-8") as f:
    #             ap=xml_pack(new_vc)
    #             f.write(ap)
    #         audio_path="{}-{}.mp3".format(new_title,i+1)
    #         os.system(audio_comm_patt.format(tts_py_path,xml_path,audio_path))
    #         new_vc="\n\n\n          === Page {} ===                     \n\n\n".format(i+1)+new_vc
    #         voice_contents[i]=new_vc
    page_sep=""
    voice_contents_s=page_sep.join(voice_contents)
    # voice_contents_s="{}\n{}\n\n".format(title,author)+voice_contents_s
    with open("voice.txt","w",encoding="utf-8") as f:
        f.write(voice_contents_s)
    shutil.copyfile("voice.txt", "records/{}/voice.txt".format(record_name))
    os.system("move *.xml  records/{}".format(record_name))
    os.system("move *.mp3  records/{}".format(record_name))

    os.chdir("records/{}".format(record_name))

    simple_video_generate_path="D:/simple_video_generate"

    os.system("copy *.pdf \"{}\"".format(simple_video_generate_path))
    os.system("copy *.mp3 \"{}\"".format(simple_video_generate_path))
    print("done.")
    # os.system("cd ./text_files")