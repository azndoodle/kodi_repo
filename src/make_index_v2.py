#!/usr/local/bin/python

""" Build index from directory listing

make_index.py </path/to/directory> [--header <header text>]
"""
from __future__ import print_function
from datetime import datetime

# Install mako template library "pip install mako"
from mako.template import Template

import os.path, time
import os
import argparse

INDEX_TEMPLATE = r"""

<html>
    <head>
        <title>Index of ${header}</title>
    </head>
    <body bgcolor="white">
        <h1>Index of ${header}</h1>
        <hr/>
            <table>
                <tr><td><a href="../">../</a></td></tr>
                
                % for name in dirnames:
                <tr>
                    <td><a href="${name}/index.html">${name}/</a></td>
                    <td>${time}</td>
                    <td>-</td>
                </tr>
                % endfor

                % for file in filenames_n_date_n_size:
                <tr>
                    <td><a href="${file[0]}">${file[0]}</a></td>
                    <td>${file[1]}</td>
                    <td>${file[2]}B</td>
                </tr>
                % endfor
            </table>
        <hr/>
    </body>
</html>
"""

EXCLUDED = ['index.html', 'make_index.py','.DS_Store']


now = datetime.now()
curent_time = now.strftime('%d-%b-%Y %H:%M') 

def fun(dir,rootdir):
    print('Processing: '+dir)
    filename = [fname for fname in sorted(os.listdir(dir))
              if fname not in EXCLUDED and os.path.isfile(dir+fname)]
    filenames_with_date_size = [[fname, time.strftime('%d-%b-%Y %H:%M', time.localtime(os.stat(dir+fname).st_mtime)), str(os.stat(dir+fname).st_size)] for fname in sorted(os.listdir(dir))
              if fname not in EXCLUDED and os.path.isfile(dir+fname)]
    dirnames = [fname for fname in sorted(os.listdir(dir))
            if fname not in EXCLUDED ]
    dirnames = [fname for fname in dirnames 
            if fname not in filename]
    
#    header = os.path.basename(dir)
    f = open(dir+'/index.html','w')
       
    print(Template(INDEX_TEMPLATE).render(dirnames=dirnames,filenames_n_date_n_size=filenames_with_date_size, header=dir,ROOTDIR=rootdir,time=curent_time),file=f)
    f.close()
    for subdir in dirnames:
        try:
            fun(dir+subdir+"/",rootdir+'../')
        except:
            pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--header")
    args = parser.parse_args()
    fun(args.directory+'/','../')

if __name__ == '__main__':
    main()