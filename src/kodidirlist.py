#!/usr/bin/python3

import os

def print_sizes(root):
    for name in sorted(os.listdir(root)):
        if os.listdir(root) != None and name.find('.zip') == -1:
            continue
        #print '<tr><td><a href="%s">%s</a></td><td>%dB</td></tr>' % (name, name, os.stat(name).st_size)
        print('      <tr><td><a href="' + name + '">' + name + '</a></td><td>' + str(os.stat(name).st_size) + 'B</td></tr>')


print ('<html>')
print ('  <body>')
print ('    <table>')
print_sizes('.')
print ('    </table>')
print ('  </body>')
print ('</html>')