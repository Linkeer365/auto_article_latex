import os
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from chardet import detect

import pytesseract
# from unidecode import unidecode

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
tessdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'

if os.path.exists("./text_files/output.txt"):
    open("./text_files/output.txt","w",encoding="utf-8").close()

def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']

def get_text(img_path):
    return pytesseract.image_to_string(Image.open(img_path),lang="chi_sim",config=tessdata_dir_config)

def get_new_pdf(ori_pdf_path,start,end):
    # 填写绝对页数而非相对页数
    with open(ori_pdf_path,"rb") as infile:
        rd=PdfFileReader(infile)
        wt=PdfFileWriter()

        for i in range(start-1,end):
            wt.addPage(rd.getPage(i))

        with open("input.pdf","wb") as outfile:
            wt.write(outfile)

# get_new_pdf("wangyuedehu.pdf",78,95)

print("以下填写的均为绝对页数而非目录页数！")
start_num=int(input("起始页数: "))
end_num=int(input("末尾页数: "))

ori_pdf_path=sorted([each for each in os.listdir(".") if each.endswith(".pdf")],key=lambda x: os.path.getctime(x))[-1]

# print(ori_pdf_path)

get_new_pdf(ori_pdf_path,start_num,end_num)

os.system("pdftoppm input.pdf -jpeg input")

imgs=sorted([each for each in os.listdir(".") if each.startswith("input") and each.endswith(".jpg")],key=lambda x:int(x.replace("input-","").replace(".jpg","")))

for img in imgs:
    img_path=os.getcwd()+os.sep+img
    # print(img_path)
    new_text=get_text(img_path)
    print(new_text)
    # break
    # 非要utf-8 真没辙，又是一堆要改
    with open("./text_files/output.txt","a",encoding="utf-8") as f:
        f.write(new_text)
        f.write("\n\n")
    # break
    print("one done.")

filename=input("filename:")

os.rename("./text_files/output.txt","./text_files/{}.txt".format(filename))
os.rename("input.pdf", "{}.pdf".format(filename))

# from_codec=get_encoding_type("./text_files/output.txt")
#
# print(from_codec)
#
# with open("./text_files/output.txt",encoding=from_codec) as f:
#     content=f.read()
# with open("./text_files/{}.txt".format(filename),"w",encoding="utf-16-le") as g:
#     g.write(content)

print("done.")

os.startfile(os.getcwd()+"/text_files/{}.txt".format(filename))
os.startfile(os.getcwd()+"/{}.pdf".format(filename))

os.system("del input*")
# os.remove("./text_files/output.txt")
