import argparse
import re
from enum import Enum

class LineTypes(Enum):
    EMPTY = 0
    HEADER = 1
    PLAINTEXT = 2
    EMPTY_IN_DIV = 3
    LIST_ELEM = 4

def all_dashes(s):
    for c in s:
        if(c != '-'): return False
    return True

def bold(s):
    out='<b>'
    l = len(s.group(0))
    out+=s.group(0)[2:(l-2)]
    out+='</b>'
    return out

def italic(s):
    out='<i>'
    l = len(s.group(0))
    out+=s.group(0)[1:(l-1)]
    out+='</i>'
    return out   

def link(s):
    split = s.group(0).split('](')
    out='<a href=\"'
    out+=split[1].replace(')','').replace('uasatucla.org', 'uas.seas.ucla.edu')
    out+='\">'
    out+=split[0][1:]
    out+='</a>'
    return out

def image(s):
    split = s.group(0).split('](')
    out='<img src='
    out+=split[1].replace(')','')
    out+=' alt=\"'
    out+=split[0][2:]
    out+='\"/>'
    return out

def main():
    parser = argparse.ArgumentParser(description='Convert MD file to our HTML format')
    parser.add_argument('infile', metavar='I', type=str, nargs=1, help='File to be parsed')
    parser.add_argument('outfile', metavar='O', type=str, nargs=1, help='File to be output')
    args=parser.parse_args()
    infile=args.infile[0]
    outfile=args.outfile[0]

    print(f'Converting md file {infile} to html')

    of = open(outfile, 'w')
    template = open('md/input-template-start.html', 'r')
    while (line := template.readline()):
        of.write(line)
    template.close()
    of.write("\n")

    inf = open(infile, 'r')
    reading = False
    found = False
    while (line := inf.readline()):
        clean = line.strip()
        if not reading and all_dashes(clean):
            if found: 
                reading=True
                prev_line = LineTypes.EMPTY
                continue
            else: 
                found=True
        if reading:
            clean = re.sub(r'<!--(.)*-->', '', clean) # Remove any comments
            h_check = clean.replace('#', '')
            if len(h_check) > 0 and len(h_check) != len(clean) and h_check[0] == ' ': # header
                if prev_line == LineTypes.PLAINTEXT or prev_line == LineTypes.EMPTY_IN_DIV:
                    of.write('</div>')
                if prev_line == LineTypes.LIST_ELEM:
                    of.write('/<ul>')
                h_lev = len(clean)-len(h_check)
                of.write(f'<h{h_lev}>')
                of.write(h_check[1:])
                of.write(f'</h{h_lev}>\n')
                prev_line = LineTypes.HEADER
            elif len(clean) == 0:
                if prev_line == LineTypes.LIST_ELEM:
                    of.write('</ul>')
                if prev_line == LineTypes.PLAINTEXT or prev_line == LineTypes.EMPTY_IN_DIV:
                    if len(clean) == 0 and prev_line == LineTypes.PLAINTEXT:
                        of.write('<br>')
                    prev_line = LineTypes.EMPTY_IN_DIV
                else:
                    prev_line = LineTypes.EMPTY
            elif clean[0:1] == '* ' or clean[0] == '-':
                if prev_line == LineTypes.PLAINTEXT or prev_line == LineTypes.EMPTY_IN_DIV:
                    of.write('</div>')
                if prev_line != LineTypes.LIST_ELEM:
                    of.write('<ul>')
                of.write('<li>')
                clean = re.sub('\*\*.*?\*\*', bold, clean[2:])
                clean = re.sub('\[.*?\]\(.*?\)', link, clean)
                of.write(clean)
                of.write('</li>')
                prev_line = LineTypes.LIST_ELEM
            else:
                if clean == '<br>':
                    continue
                if prev_line == LineTypes.LIST_ELEM:
                    of.write('/<ul>')
                if prev_line != LineTypes.PLAINTEXT and prev_line != LineTypes.EMPTY_IN_DIV:
                    of.write('<div class=\"autogen-md\">')
                clean = re.sub('!\[.*?]\(.*?\)', image, clean)
                clean = re.sub('\*\*.*?\*\*', bold, clean)
                clean = re.sub('\*.*?\*', italic, clean)
                clean = re.sub('\[.*?\]\(.*?\)', link, clean)
                of.write(clean)
                prev_line = LineTypes.PLAINTEXT
            #print(clean)

        #print(clean)
    if prev_line == LineTypes.LIST_ELEM: 
        of.write('</ul>')
    elif prev_line == LineTypes.PLAINTEXT:
        of.write('</div>')
    inf.close()

    template = open('md/input-template-end.html', 'r')
    while (line := template.readline()):
        of.write(line)
    template.close()    
    of.close()

if __name__=="__main__":
    main()