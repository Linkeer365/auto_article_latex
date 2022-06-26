import os
# os.system("chcp 65001")
os.system("cd ./text_files && xelatex output.tex && move output.pdf ../ && del *-2.txt")