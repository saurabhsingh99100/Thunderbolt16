#first pass 
import os
import sys

LABELS={}
VARIABLES={}
libpath="/home/frozenalpha/Desktop/Thunderbolt/Tbassembler/asmfiles/lib/"

#pseudo operations $x mean xth parameter given when calling (x=0 is first parameter)
PSOP={  'INC':['ADI $0,$0,1'],
        'DCR':['SBI $0,$0,1'],

        'PUSH':['STRG $0,SP','SBI SP,SP,1'],
        'POP':['ADI SP,SP,1','LDRG $0,SP'],
        'PUSHI':['LDI TR,$0','STRG TR,SP','SBI SP,SP,1'],

        'PUSHREGS':['STRG R4,SP','SBI SP,SP,1',
                    'STRG R3,SP','SBI SP,SP,1',
                    'STRG R2,SP','SBI SP,SP,1',
                    'STRG R1,SP','SBI SP,SP,1',
                    'STRG R0,SP','SBI SP,SP,1',
                    'STRG LR,SP','SBI SP,SP,1',],

        'POPREGS': ['ADI SP,SP,1','LDRG LR,SP',
                    'ADI SP,SP,1','LDRG R0,SP',
                    'ADI SP,SP,1','LDRG R1,SP',
                    'ADI SP,SP,1','LDRG R2,SP',
                    'ADI SP,SP,1','LDRG R3,SP',
                    'ADI SP,SP,1','LDRG R4,SP',],

        'CALL':    ['STRG R4,SP','SBI SP,SP,1',
                    'STRG R3,SP','SBI SP,SP,1',
                    'STRG R2,SP','SBI SP,SP,1',
                    'STRG R1,SP','SBI SP,SP,1',
                    'STRG R0,SP','SBI SP,SP,1',
                    'STRG LR,SP','SBI SP,SP,1',
                    'JAL $0',
                    'ADI SP,SP,1','LDRG LR,SP',
                    'ADI SP,SP,1','LDRG R0,SP',
                    'ADI SP,SP,1','LDRG R1,SP',
                    'ADI SP,SP,1','LDRG R2,SP',
                    'ADI SP,SP,1','LDRG R3,SP',
                    'ADI SP,SP,1','LDRG R4,SP',],
        'CMP':['CLF','CP $0,$1'],
        'CMI':['CLF','CI $0,$1'],

        'BOOT':['LDI LR,0','LDI SP,0xfff0'],
        
        'PRINT':['IOS $0,0'],
        'SCAN': ['IOR $0,1'],
        'SWAP': ['MOV TR,$0','MOV $0,$1','MOV $1,TR']

    }



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
    print(code)
    while(i<len(code)):
        if '.' in code[i] or 'import' in code[i]:
            pass
        else:
            Length+=1
        i+=1
    Length+=len(PSOP['BOOT'])-1
    return Length

def include(Target):
    #print(Target)
    if Target[-1]=='*':
        Target=Target.replace('*','')
        files=os.listdir(libpath+Target)
        txt=[]
        for i in files:
            if '.fun' in i:
                f=open(str(libpath+Target+i),"r")
                txt=txt+f.readlines()
                txt=preprocess(txt)
                f.close
        #print(txt)
    else:
        try:
            f=open(str(libpath+Target+'.fun'),"r")
            txt=txt+f.readlines()
            txt=preprocess(txt)
            f.close
        except IOError:
            error(Target+' library not found')

    return txt


def psop(code):
    l=len(code)
    a=0
    #print code
    while(a<l):
        line=code[a]
        #print line
        if '.' in line or '=' in line:
            a+=1
            continue
        else:
            line=line.split(' ')
            
            if len(line)>1:
                line[1]=line[1].split(',')
                
                if line[0] in PSOP.keys():
                    cde=PSOP[line[0]]
                    stmnts=[]
                    
                    for b in range(0,len(cde)):
                        stmt=cde[b]
                        stmt=stmt.split(' ')
                        if len(stmt)==1:
                            stmnts=stmnts+[stmt[0]]
                        else:
                            stmt[1]=stmt[1].split(',')
                            for d in range(0,len(stmt[1])):
                                c=stmt[1][d]
                                if '$' in c:
                                    c=int(c.replace('$',''))
                                    c=line[1][c]
                                    stmt[1][d]=c
                            # convert to str
                            statement=stmt[0]+' '
                            for c in stmt[1]:
                                statement=statement+c+','
                            statement=statement[0:len(statement)-1]# remove extra comma
                            stmnts=stmnts+[statement]

                    code=code[0:a]+stmnts+code[a+1:l]
                    l=l+len(stmnts)-1

            else: #len=1
                if line[0] in PSOP.keys():
                    cde=PSOP[line[0]]
                    code=code[0:a]+cde+code[a+1:l]
                    l=l+len(cde)-1
            #print code
            
            a+=1
            
    return code


def saveLabel(label,add):
    label=str(label).replace('.','')
    add=int(add)
    LABELS.update([[label,add]])

def saveVariable(varname,add,val):
    varname=str(varname)
    add=int(add)
    VARIABLES.update([[varname,[add,val]]])

def procesStr(txt):
    print(txt)
    
def assignAddresses(code,l):
    address=0
    i=0
    flag=0
    TexT=''
    stringflag=0
    #print(l)
    while(i<len(code)):

        if '=' in code[i]: #it is a variable
            tmp=code[i].split('=')
            saveVariable(tmp[0],address,tmp[1])

        if '=' and '"' in code[i]: #it is a string
            if address%2!=0: #string will always begin at even address
               address+=1
            tmp=code[i].split('=')
            TexT=tmp[1].replace('"','')
            #TexT=procesStr(TexT)



            stringflag=1
            saveVariable(tmp[0],address,TexT+'\n')
        
        if '.' in code[i]: #it is a label
            l+=1
            saveLabel(code[i],address)
            #dont increment address
        else:
            code[i]=str(address)+' '+code[i]
        
        if i==l:
           flag=0
           

        if '.data' in code[i]:
            flag=1
        
        #print [i,l]
        #print code[i]


       # print(code[i]+str(stringflag)+str(flag))
        
        if ('.' not in code[i]) and (flag==1):
            if stringflag==1:
                #print(len(TexT))
                if(len(TexT)%2==0): # even len
                    address+=int((len(TexT)/2))+1
                else:
                    address+=int((len(TexT)+1)/2)+1
                TexT=''
                stringflag=0
                    
            else:
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

    if code[0]!='BOOT': #addboot
        code=['BOOT']+code


    #add hault if not present
    code=addHault(code)         
    
    #get length without lib
 
    l=getlen(code)
    #print(l)
    #print(code)
    #if l%2==0: #length of code not even it wil give wrong addresses to library code after .data since .data section has address incremeent of 1 instead of 2
    #    code=code+['DUMVAR=0']
    #    l+=1
    #include libraries
    flag=1 #assume it has import
    while flag==1:
        for line in code:
            if 'import' in line:
                Target=(line.replace("import","")).strip()
                additionalcode=include(Target)
                code=code+additionalcode
                code.remove(line)
                flag=0
                break

        #check for 'import' in whole code
        for line in code:
            if 'import' in line:
                flag=1
                break
            else:
                flag=0
        
    code=psop(code)


    #assign addresses #save labels and variables
    code=assignAddresses(code,l)
    #print(code)

    #remove labels
    code=removeLabels(code)
    #print(code)

    return [code,LABELS,VARIABLES]