import os
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from chardet import detect
import pytesseract

import matplotlib.pyplot as plt 

from cnocr import CnOcr

# img_fp = './docs/examples/huochepiao.jpeg'
# ocr = CnOcr()  # 所有参数都使用默认值
# out = ocr.ocr(img_fp)

# print(out)

# from unidecode import unidecode

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
tessdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'

if os.path.exists("./text_files/output.txt"):
    open("./text_files/output.txt","w",encoding="utf-8").close()

if os.path.exists("./text_files/output2.txt"):
    open("./text_files/output2.txt","w",encoding="utf-8").close()

def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']

def get_text2(img_path):
    return pytesseract.image_to_string(Image.open(img_path),lang="chi_sim",config=tessdata_dir_config)

def get_text(img_path):
    ocr = CnOcr()  # 所有参数都使用默认值
    out = ocr.ocr(img_path)
    # print("out:",out)
    # out = [dict(text="",score="",position="")]
    lines=[]
    cur_distance=-1000
    for pack in out:
        print(pack)
        print("\n\n** ** **\n\n")
        text=pack["text"]
        left_distance=pack["position"][0][0]
        # assert left_distance!=None
        if cur_distance==-1000:
            print("cur_dist is None.")
            # text="par"+text
            # cur_distance=left_distance
            # flag=-1
        delta_distance=left_distance-cur_distance
        # >100 是指分页，分页的一般是直接接过去就行
        if delta_distance>=30 and abs(delta_distance)<=100:
            text="par"+text
        print(text)
        print("current distance:",cur_distance)
        print("left distance:",left_distance)
        print("delta distance:",delta_distance)
        print("\n=== === ===\n")
        lines.append(text)
        cur_distance=left_distance
        # print(left_distance)
    lines_s="".join(lines)
    return lines_s

def get_new_pdf(ori_pdf_path,start,end):
    # 填写绝对页数而非相对页数
    with open(ori_pdf_path,"rb") as infile:
        rd=PdfFileReader(infile)
        wt=PdfFileWriter()
        # print("g.")

        for i in range(start-1,end):
            wt.addPage(rd.getPage(i))

        with open("input.pdf","wb") as outfile:
            wt.write(outfile)

def get_format_text(raw_str):
    eng_chi_dict={
        ",":"，",
        ".":"。",
        "?":"？",
        ";":"；",
        "!":"！",
        "(":"（",
        ")":"）",
        "<":"《",
        ">":"》",
        ":":"：",
        "[":"【",
        "]":"】",
        # " ":"",
        # "\n\n":"par",
                }
    format_chars=[]
    for each in raw_str:
        if each in eng_chi_dict.keys():
            format_chars.append(eng_chi_dict[each])
        else:
            format_chars.append(each)
    format_str="".join(format_chars)
    # format_str=format_str.replace("\n\n", "par")
    # format_str=format_str.replace("\n", "")
    format_str=format_str.replace("par", "\n\n")
    return format_str

# print(get_format_string("三三制,呜呜之. 时 时勤拂 拭? 郭攸 之; nm d! (oqjwn)<bwbsja>pqjw:"))
# os._exit(0)
# get_new_pdf("wangyuedehu.pdf",78,95)

cwd=r"D:\auto_article_latex"

print(cwd)

os.chdir(cwd)

flag=1
while flag:
    for each in os.listdir("."):
        if each.endswith(".pdf"):
            choose=input("if sure press y:\n{}\t\t".format(each))
            if choose == "y":
                ori_pdf=each
                flag=0
                break
                

# ori_pdf_path=sorted([each for each in os.listdir(".") if each.endswith(".pdf")],key=lambda x: os.path.getctime(x))[0]
ori_pdf_path=cwd+os.sep+ori_pdf
print(ori_pdf_path)

# os._exit(0)

# print(ori_pdf_path)

print("以下填写的均为绝对页数而非目录页数！")
start_num=int(input("起始页数: "))
end_num=int(input("末尾页数: "))

get_new_pdf(ori_pdf_path,start_num,end_num)

os.system("pdftoppm input.pdf -jpeg input")

imgs=sorted([each for each in os.listdir(".") if each.startswith("input") and each.endswith(".jpg")],key=lambda x:int(x.replace("input-","").replace(".jpg","")))

for img in imgs:
    img_path=os.getcwd()+os.sep+img
    img_obj=Image.open(img_path)
    # os._exit(0)
    # print(img_obj.size)
    width,height=img_obj.size
    # box=(10,10,10,10)
    # 这个参数是我好不容易才试出来的，不要动！！
    # box1=(0,height/12,width,height-height/12+height/24)
    # box1=(0,height/12,width,height-height/12-height/48)
    box1=(0,0,0,0)
    new_img_obj=img_obj
    if box1 != (0,0,0,0):
        new_img_obj=img_obj.crop(box1)
    # plt.imshow(new_img_obj)
    new_img_obj.save(img_path)
    # plt.show()
    # break

# os.system("del input*")

# os._exit(0)

for img in imgs:
    img_path=os.getcwd()+os.sep+img
    # print(img_path)
    raw_text=get_text(img_path)
    new_text=get_format_text(raw_text)
    # new_text=raw_text.replace("par", "\n\n")
    # print(new_text)
    # break
    # 非要utf-8 真没辙，又是一堆要改
    # update 2022-11-20: 保存成utf8bom，然后用下面那段代码。
    with open("./text_files/output2.txt","a",encoding="utf-8-sig") as f:
        f.write(new_text)
        # f.write("\n\n")
    # break
    # print("one done.")

# os._exit(0)

with open("./text_files/output2.txt","rb") as src_file:
    with open("./text_files/output.txt","w+b") as des_file:
        contents=src_file.read()
        des_file.write(contents.decode("utf-8").encode("utf-16-le"))

# os._exit(0)

filename=input("filename:")

if os.path.exists("./text_files/{}.txt".format(filename)):
    os.remove("./text_files/{}.txt".format(filename))
if os.path.exists("{}.pdf".format(filename)):
    os.remove("{}.pdf".format(filename))

os.rename("./text_files/output.txt","./text_files/{}.txt".format(filename))
os.rename("input.pdf", "{}-截取版.pdf".format(filename))

# from_codec=get_encoding_type("./text_files/output.txt")
#
# print(from_codec)
#
# with open("./text_files/output.txt",encoding=from_codec) as f:
#     content=f.read()
# with open("./text_files/{}.txt".format(filename),"w",encoding="utf-16-le") as g:
#     g.write(content)

# print("格式给我手动保存成 utf-16-le！")
# print("格式给我手动保存成 utf-16-le！")
# print("格式给我手动保存成 utf-16-le！")

print("done.")

os.startfile(os.getcwd()+"/text_files/{}.txt".format(filename))
# os.startfile(os.getcwd()+"/{}.pdf".format(filename))

os.system("del input*")
# os.remove("./text_files/output.txt")
