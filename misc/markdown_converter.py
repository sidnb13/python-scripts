import glob, os, shutil, os.path
from os import path
    
SRC = '/Users/sidbaskaran/Desktop/Python Automation Scripts/markdown/test' #markdown source files
OUT = '/Users/sidbaskaran/Desktop/Python Automation Scripts/markdown/html' #destination for html conversion
ONE_LINE = '<link rel="stylesheet" href="../modest.css">\n\n' #markdown style sheet rel. path

os.chdir(SRC)
for file in glob.glob("*.md"):
    with open(file, 'r+') as fp:
        lines = fp.readlines() 
        if (lines[0].__contains__('stylesheet') or lines[0].__contains__("#") == False):
            lines[0] = ONE_LINE
        else:
            lines[0] = ONE_LINE
        fp.seek(0)                 
        fp.writelines(lines)       
    os.system('markdown-it '+file+' -o '+file.replace('.md','.html'))
    
os.chdir(OUT)
for file in glob.glob('*.html'):
    os.remove(file)
    
os.chdir(SRC)
for file in glob.glob('*.html'):
    shutil.move(file,OUT)