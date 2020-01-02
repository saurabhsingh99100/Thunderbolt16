#first pass
import os
import sys

LABELS={}
VARIABLES={}

def error(txt): #DISPLAYS ERROR MESSAGE AND EXITS
    sys.exit("\n- Pass1 error:- "+txt+": file assembling unsuccessful...")


def preprocess(txt):
    txt=removeComments(txt)         #removes comments (text after '$')
    txt=removeIndent(txt)           #removes Indentation 
    txt=removeBlankLines(txt)       #removes blank lines 
    return txt


def removeIndent(txt):  #REMOVES INDENTATION BY STRIPPING FROM BOTH SIDES
    for i in range(0,len(txt)):
        txt[i]=txt[i].strip()
    return txt


def removeComments(txt): #REMOVES COMMENTS BY CHECKING FOR SYMBOL "#"
    flag=0
    for j in range(0,len(txt)):
        line=txt[j]
        #comment identification
        comment=""
        for i in range(0,len(line)):
            if line[i]=='#':
                flag=1
            if flag==1:
                comment=comment+line[i]
        flag=0
        #comment removal
        line=line.replace(comment,"")
        txt[j]=line
        #print(line+"i\n")
    return txt

def removeBlankLines(lst): #REMOVES EMPTY/BLANK LINES
    i=0
    if "" in lst:
        while(i<len(lst)):
            if lst[i]=="":
                lst.pop(i)
                i=0
            else:
                i+=1    
        return lst
    else:
        
        return lst

def addHault(code):
    if not('HLT' in code):
        if '.data' in code:
            code.insert(code.index('.data'),'HLT')
        else:
            code=code+['HLT']
    return code


def getlen(code):
    Length=0
    i=0
    while(i<len(code)):
        if '.' in code[i] or '#include' in code[i]:
            pass
        else:
            Length+=1
        i+=1
    return Length

def include(Target):
    try:
        f=open(str(os.getcwd())+"/asmfiles/lib/"+Target,"r")
        txt=f.readlines()
        txt=preprocess(txt)
        f.close
    except IOError:
        error(Target+' library not found')
    return txt

def saveLabel(label,add):
    label=str(label).replace('.','')
    add=int(add)
    LABELS.update([[label,add]])

def saveVariable(varname,add,val):
    varname=str(varname)
    add=int(add)
    VARIABLES.update([[varname,[add,val]]])

def assignAddresses(code,l):
    address=0
    i=0
    flag=0
    #print l
    while(i<len(code)):
        
        if '=' in code[i]:
            tmp=code[i].split('=')
            saveVariable(tmp[0],address,tmp[1])
        
        if '.' in code[i]: #it is a label
            l+=1
            saveLabel(code[i],address)
            #dont increment address
        else:
            code[i]=str(address)+' '+code[i]


        if '.data' in code[i]:
            flag=1
        if i==l:
            flag=0
        #print [i,l]
        #print code[i]
        if ('.' not in code[i]) and (flag==1):
            address+=1
        elif ('.' not in code[i]) and (flag==0):
            address+=2
        else:
            pass

        i+=1
    return code

def removeLabels(code):
    for i in LABELS.keys():
        x='.'+i
        if x in code:
            code.remove(x)
    return code
#----------------------------------------------
#1) preprocess
#2) add HLT if not present already
#3) assembler directives
#4) replace pseudo ops
#5) assign addresses
#6) create labels table

def firstpass(code):

    #preprocess
    code=preprocess(code)       
    
    #find .main
    if not('.main' in code):        
        error('main label absent')

    #add hault if not present
    code=addHault(code)         
    
    #get length without lib
    l=getlen(code)

    #include libraries
    for line in code:
        if 'import' in line:
            Target=(line.replace("import","")).strip()
            additionalcode=include(Target)
            code=code+additionalcode
            code.remove(line)


    #add pseudo ops here

    #assign addresses #save labels and variables
    code=assignAddresses(code,l)

    #remove labels
    code=removeLabels(code)

    return [code,LABELS,VARIABLES]