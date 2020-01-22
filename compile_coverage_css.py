import re
import os
from collections import defaultdict
import pprint

# TODO:
# input_dir= <replace with directory containing used CSS files>
# output_dir= <replace with directory where you want to save cleaned.css>
css_by_file=defaultdict() # dictionary containing {<url>: <used css>}

files=os.listdir(input_dir)
for fname in files:
    fpath= input_dir + fname
    print('======================= ',fname,' =======================')
    cssDict = defaultdict()
    mergedCSS=defaultdict(list)
    with open(fpath, 'r') as f:
        i = 0
        css = ''.join(f.readlines())
        comments=[] # optional var saving puppeteer log (contains url of all requested stylesheets)
        for line in re.findall('([^}]+)', css):
            i += 1
            # print(line)
            if '{' in line:
                k, v0 = line.split('{')
                k = k.strip(' \n')
                v = ''.join([b.strip('\n ') for b in re.split('/', v0) if not b[0] == '*' and len(b.strip('\n ')) > 0]) #remove comments
                vals = [w.strip('\n ') for w in v.split(';') if len(w.strip('\n ')) > 0]
                innerKey = {}
                [innerKey.update({a[0]: a[1]}) for a in [z.split(': ') if ': ' in z else z.split(':') for z in vals]]
                cssDict[k] = innerKey
                if i % 10 == 0:
                    print(v0)
                    print('innerKey: ', innerKey)
            else:
                comments.append(line)
    print(len(cssDict.items()))
    css_by_file[fname]=cssDict

# merge dicts without overwriting:
from itertools import chain

dicts=[]
for f, css in css_by_file.items():
    dicts.append(css)
dd = defaultdict(list) 
for k, v in chain(*[x.items() for x in dicts]):
    dd[k].append(v)

cleanDict=defaultdict()
for selector, styleList in dd.items():
    tempDict = defaultdict(list)
    for k, v in chain(*[x.items() for x in styleList]):
        if v not in tempDict[k]:
            tempDict[k].append(v)
    cleanDict[selector]=tempDict

# check for overwritten styles
for selectors, properties in cleanDict.items():
    for prop,val in properties.items():
        if len(val)>1:
            print(prop, val)


# rebuild clean CSS file
cssFile=''
for selectors, properties in cleanDict.items():
    cssFile+='\n'+selectors+' {'
    for prop,val in properties.items():
        cssFile+='\n    '+prop+':'
        cssFile+= ' '+ val[0]+';' # uses the first defined style, if multiple conflicting style definitions exist
    cssFile += '\n}'

output_file=os.path.join(output_dir, 'cleaned.css')
with open(output_file, 'w') as f:
    f.write(cssFile)
