import re
import os
import shutil
import sys
from get_title_infos import get_title_infos
from global_used_paths import latex_template_path,txt_file_dir

def save_files(title_info_dict,txt_file_path):
    filename=title_info_dict['filename']
    title=title_info_dict['<Your-Title>']
    author=title_info_dict['<Your-Author>']
    date=title_info_dict['<Your-Date>'].replace("-","")
    if not os.path.exists(f'./records/{title}-{author}-{date}'):
        os.makedirs(f"./records/{title}-{author}-{date}")
    # 保存txt文件（复制）
    shutil.copyfile(txt_file_path,f"./records/{title}-{author}-{date}/{title}-{author}-{date}.txt")
    # 保存tex与pdf文件（剪切）
    os.rename(f"output.tex",f"./records/{title}-{author}-{date}/{title}-{author}-{date}.tex")
    os.rename(f"output.pdf",f"./records/{title}-{author}-{date}/{title}-{author}-{date}.pdf")
    # 删掉剩下的垃圾
    os.system(f"cd \"{os.getcwd()}\" && del output*")

def get_format_tex_content_by_poem_or_essay(content_str,poem_or_essay):
    if poem_or_essay == 'poem':
        tex_file_paras=content_str.split('\n\n')
        for para_idx,para in enumerate(tex_file_paras):
            tex_file_lines_each_para=para.split('\n')
            for line_idx, line in enumerate(tex_file_lines_each_para):
                if line.replace(" ",'').replace("　",'') == '':
                    # 空行一律改成两个中文空格
                    line = '　　'
                line = line.replace("\n",'') + r'\\'+'\n'
                tex_file_lines_each_para[line_idx]=line
            tex_file_paras[para_idx]="".join(tex_file_lines_each_para)
        format_str = '\n\n'.join(tex_file_paras)
    elif poem_or_essay == 'essay':
        format_str = content_str
    return format_str

def get_final_file_str(info_dict:dict,template_path:str,poem_or_essay):
    with open(template_path,'r',encoding='utf-8') as f:
        template_line_s=f.read()
    for key,value in info_dict.items():
        template_line_s=template_line_s.replace(key,value)
    # 最终的文本体现
    final_file_str=template_line_s
    if poem_or_essay == 'essay':
        final_file_str=final_file_str.replace(r"\setlength\parindent{0pt}",'')
    return final_file_str
    
def get_para_list_from_one_file(file_path:str):
    # 读取完整文件内容，存入字符串lines_s
    with open(file_path,'r',encoding='utf-8') as f:
        lines_s=f.read()
    # 设定1：段落必定由两个及以上\n所分割
    para_list=lines_s.split("\n\n")
    return para_list

def get_para_type(para:str):
    # 章节段落单独标记为：crt
    return 'crt' if para.startswith("crtcrtcrt") else 'normal'

def get_latex_file_save_compile(title_info_dict,txt_file_path,template_path,txt_filename):
    para_list = get_para_list_from_one_file(txt_file_path)
    for para_idx,para in enumerate(para_list):
        para_type = get_para_type(para)
        if para_type == 'crt':
            para='\n\n'+r"{\centering\section*{" + para.replace("crtcrtcrt",'').replace("\n",'') + '}}'+'\n\n'
            para_list[para_idx]=para
    paras_s="\n\n".join(para_list)
    content_str=get_format_tex_content_by_poem_or_essay(paras_s,title_info_dict["poem_or_essay"])
    title_info_dict['<Your-Content>']=content_str
    final_file_str=get_final_file_str(title_info_dict,template_path,title_info_dict["poem_or_essay"])
    # 生成编译用txt文件
    with open(f"output.tex",'w',encoding='utf-8') as f:
        f.write(final_file_str)
    # 编译该文件
    os.system(f"xelatex -interaction=nonstopmode output.tex")
    # 保存应该保存的文件
    save_files(title_info_dict,txt_file_path)

if __name__ == '__main__':
    title_info_dict = get_title_infos()
    txt_filename = title_info_dict['filename']
    txt_file_path = txt_file_dir + os.sep + txt_filename + '.txt'
    get_latex_file_save_compile(title_info_dict,txt_file_path,latex_template_path,txt_filename)