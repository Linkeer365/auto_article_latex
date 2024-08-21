import re
import os
import shutil
import sys
import time
import datetime

# large 状态下经常出格，不知道怎么办才好
# 试过多次是这个16 21 最合适
proper_essay_word_cnt=380

essay_word_per_line=23
poem_word_per_line=23

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
poem_head="\setlength\parindent{0pt}\n\n"+essay_head
poem_bottom=""

std_xml_pack=open("./stable/std_audio_pack.xml","r",encoding="utf-8").read()

# thank you so much for your wonderful help!
# https://github.com/skygongque/tts
#  
tts_py_path="./tts/python_cli_demo/tts.py"

def xml_pack(words):
    return std_xml_pack.replace("<Your-Words>", words)

def process2(poem_or_essay,filename):
    if poem_or_essay=="essay":
        word_cnt=2
        article_word_per_line=essay_word_per_line
        article_insert=essay_insert
        article_head=essay_head
        article_bottom=""

    elif poem_or_essay=="poem":
        word_cnt=0
        article_word_per_line=poem_word_per_line
        article_insert=poem_insert
        article_head=poem_head
        article_bottom=poem_bottom

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

    new_str="".join(new_lines)

    # 前三个是给poem的，最后一个是给essay 的
    new_str=new_str.replace("\\par \n\\\\", "\\\\ \n\n")
    new_str=new_str.replace("\\par \\\\", "\\\\ \n\n")
    new_str=new_str.replace("\n\\newpage\n\\\\", "\\\\\n\\newpage\n")
    new_str=new_str.replace("\\par \n", "\n\n")
    new_str=new_str.replace("\\par ", "\n\n")

    new_str=article_head+new_str+article_bottom
    with open("./text_files/{}-2.txt".format(filename),"w",encoding="utf-8") as f:
        f.write(new_str)

if __name__ == "__main__":
    # 2022年6月27日 22:52:24 诗歌体的居中就是纯纯sb，每行的字数从9-11字不等你让我玩毛？
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
    filename=input("filename:")
    url=input("网页链接：（最好是archive后的）")
    # filename="ee"
    print(poem_or_essay)
    process2(poem_or_essay,filename)

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
    
    record_name="{}-{}".format(title,author)
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

    try:
        shutil.copyfile("output.pdf", "records/{}/{}.pdf".format(record_name,new_title))
    except FileNotFoundError:
        shutil.copyfile("./text_files/output.pdf", "output.pdf")
        os.system("cd ./text_files && del output*")
        shutil.copyfile("output.pdf", "records/{}/{}.pdf".format(record_name,new_title))

    shutil.copyfile("output.pdf", "pdf-temp/{}.pdf".format(new_title))

    voice_content=content

    audio_comm_patt="edge-tts --voice zh-CN-YunyangNeural --rate=-20% -f \"{}\" --write-media \"{}.mp3\""
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
        # 2023-4-8 21:56:36 因为SSML被微软kill了，所以这里我们采用另一个api文档转语音，就不用xml_pack来包装它了（但是xml还保留，不动它）
        xml_path="{}-{}.xml".format(new_title,i+1)
        with open(xml_path,"w",encoding="utf-8") as f:            
            ap=xml_pack(new_vc)
            f.write(ap)
        # 新的txt文件
        txt_path="{}-{}.txt".format(new_title,i+1)
        with open(txt_path,"w",encoding="utf-8") as f:            
            txt=new_vc
            f.write(txt)
        audio_path="{}-{}".format(new_title,i+1)
        # audio_comm=audio_comm_patt.format(tts_py_path,xml_path,audio_path)
        audio_comm=audio_comm_patt.format(txt_path,audio_path)
        # print("先关掉你的proxy.")
        print("audio comm:",audio_comm)
        cnt=0
        while True:
            res=os.system(audio_comm)
            if res==0:
                break
            elif res==1:
                sleep_time=2+2*cnt
                time.sleep(sleep_time)
                print("=== \nsleep {}s.\n===\n".format(sleep_time))
                cnt+=1
        new_vc="\n\n\n          === Page {} ===                     \n\n\n".format(i+1)+new_vc
        voice_contents[i]=new_vc

    page_sep=""
    voice_contents_s=page_sep.join(voice_contents)
    # voice_contents_s="{}\n{}\n\n".format(title,author)+voice_contents_s
    with open("voice.txt","w",encoding="utf-8") as f:
        f.write(voice_contents_s)
    shutil.copyfile("voice.txt", "records/{}/voice.txt".format(record_name))
    os.system("move *.xml  records/{}".format(record_name))
    os.system("move *.mp3  records/{}".format(record_name))
    os.system("move *.txt  records/{}".format(record_name))

    os.chdir("records/{}".format(record_name))

    time_str=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    simple_video_generate_path="D:/simple_video_generate/{}".format(time_str)
    # print(simple_video_generate_path)
    if not os.path.exists(simple_video_generate_path):
        os.makedirs(simple_video_generate_path)
    os.system("copy *.pdf \"{}\"".format(simple_video_generate_path))
    os.system("copy *.mp3 \"{}\"".format(simple_video_generate_path))
    print(simple_video_generate_path)
    with open("D:/simple_video_generate/svg_paths.txt","a",encoding="utf-8") as f:
        f.write(simple_video_generate_path)
        f.write("\n")
    # os.system("copy *.txt \"{}\"".format(simple_video_generate_path))
    print("done.")
    # os.system("cd ./text_files")