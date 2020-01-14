#second pass
import sys
keywords={  "NOP":"00000",
            
            "NOT":["00001","0000"],
            "AND":["00001","0001"],
            "OR":["00001","0010"],
            "NAND":["00001","0011"],
            "NOR":["00001","0100"],
            "XOR":["00001","0101"],
            "ADD":["00001","0110"],
            "SUB":["00001","0111"],
            "MUL":["00001","1000"],
            "DIV":["00001","1001"],
            "REM":["00001","1010"],
            "LSL":["00001","1011"],
            "LSR":["00001","1100"],
            "ASL":["00001","1101"],
            "ROL":["00001","1110"],
            "ROR":["00001","1111"],

            "ANDI":["00010","0001"],
            "ORI":["00010","0010"],
            "NANDI":["00010","0011"],
            "NORI":["00010","0100"],
            "XORI":["00010","0101"],
            "ADI":["00010","0110"],
            "SBI":["00010","0111"],
            "MUI":["00010","1000"],
            "DIVI":["00010","1001"],
            "REMI":["00010","1010"],
            "LSLI":["00010","1011"],
            "LSRI":["00010","1100"],
            "ASLI":["00010","1101"],
            "ROLI":["00010","1110"],
            "RORI":["00010","1111"],
            
            "ADC":["00011","0110"],
            "SBB":["00011","0111"],
            
            "LDR":"00100",
            "STR":"00101",          
            "LDRG":"00110",            
            "STRG":"00111",            
            "LDI":"01000",            
            "MOV":"01001",            
            "SVPC":"01010",            
            "STPC":"01011",

            "CMP":"01100",
            "CMI":"01101",

            "J":["01110","000"],
            "JEQ":["01110","001"],
            "JNQ":["01110","010"],
            "JLT":["01110","011"],
            "JGT":["01110","100"],
            "JLE":["01110","101"],
            "JGE":["01110","110"],
            "JAL":["01110","000"],
            "JEQL":["01110","001"],
            "JNQL":["01110","010"],
            "JLTL":["01110","011"],
            "JGTL":["01110","100"],
            "JLEL":["01110","101"],
            "JGEL":["01110","110"],
            "RET":"01111","RETR":"01111",

            "IOS":"10000",
            "IOR":"10001",
            "CLF":"10100",

            "RST":"11100",
            "SLP":"11101",
            "SLR":"11110",
            "HLT":"11111"
           
        }

def error(txt): #DISPLAYS ERROR MESSAGE AND EXITS
    sys.exit("\n- Pass2 error :- "+txt+"---\n\nfile assembling unsuccessful...")


def tobin(bits,val):        #CONVERS HEX/BIN/DEC TO "n" BIT BINARY NUMBER
    val=str(val)
    val=(val.replace('[','')).replace(']','')
    Val=""
    if '0x' in val:     #hex
        val=val.replace("0x","")
        for i in range(0,len(val)):
            if val[i]=='0':
                Val=Val+"0000"
            elif val[i]=='1':
                Val=Val+"0001"
            elif val[i]=='2':
                Val=Val+"0010"
            elif val[i]=='3':
                Val=Val+"0011"
            elif val[i]=='4':
                Val=Val+"0100"
            elif val[i]=='5':
                Val=Val+"0101"
            elif val[i]=='6':
                Val=Val+"0110"
            elif val[i]=='7':
                Val=Val+"0111"
            elif val[i]=='8':
                Val=Val+"1000"
            elif val[i]=='9':
                Val=Val+"1001"
            elif val[i]=='a' or val[i]=='A':
                Val=Val+"1010"
            elif val[i]=='b' or val[i]=='B':
                Val=Val+"1011"
            elif val[i]=='c' or val[i]=='C':
                Val=Val+"1100"
            elif val[i]=='d' or val[i]=='D':
                Val=Val+"1101"
            elif val[i]=='e' or val[i]=='E':
                Val=Val+"1110"
            elif val[i]=='f' or val[i]=='F':
                Val=Val+"1111"

    elif '0b' in val: #already in bin
        Val=val.replace("0b","") 
        
    else:              #decimal
        Val=str(bin(int(val))).replace("0b","")

    l=len(Val)
    fval=""
    if bits>l:
        for i in range(0,bits-l):
            fval="0"+fval
        fval=fval+Val
        return fval
    elif bits<l:
        for i in range(0,bits):
            fval=Val[l-1]+fval
            l-=1
        return fval
    else:
        return Val 



def tokenize(txt):
    lst=list(txt.split(' '))
    
    if len(lst)==3: #all usual operations
        lst[2]=list(lst[2].split(','))
    elif len(lst)==2: # variables and operations like HLT
        if '=' in lst[1]:   #vars
            lst[1]=lst[1].split('=')    
        else:       # ops like HLT and NOP
            pass

    return lst

def substitute(line,VARIABLES,LABELS):
 

    if len(line)==3:     #usual ops all other cases will never contain var/label
        #search
        

        for i in range(0,len(line[2])):
            if line[2][i] in VARIABLES.keys():
                line[2][i]=VARIABLES[line[2][i]][1]
            elif (line[2][i].replace('[','')).replace(']','') in VARIABLES.keys():
                line[2][i]=(line[2][i].replace('[','')).replace(']','')
                line[2][i]=VARIABLES[line[2][i]][0]
        
        for i in range(0,len(line[2])):
            if line[2][i] in LABELS.keys():
                line[2][i]=LABELS[ line[2][i] ]
    return line

def regToBin(txt):
    if txt in ['SP','LR','TR']:
        
        if txt=='SP':
            return '111'
        elif txt=='LR':
            return '110'
        elif txt=='TR':
            return '101'

    else:
        reg=int((txt.replace('R','')).replace('r',''))    
        if reg>=5:
            print('pass2 Warning: in '+txt+' : Reg>5 should be used carefully.')
        return tobin(3,reg)



def immToBin(txt):
    #condition for imm
    return tobin(16,txt)


def identify(token):
    code=''
    if token[0] not in keywords:
        error(token[0]+' : Undefined operation')

    y=keywords[token[0]]
    if isinstance(y,list):
        opcode=y[0]
        subOpcode=y[1]
    else:
        opcode=y
        subOpcode=""
    
    if token[0]=="NOP":
        code="00000000000000000000000000000000"
    elif token[0]=='NOT':
        code=opcode + regToBin(token[1][0]) + regToBin(token[1][1]) + "000" + "00000000000000" + subOpcode

    elif token[0] in ['AND','OR','NAND','NOR','XOR','ADD','SUB','MUL','DIV','REM','LSL','LSR','ASL','ROL','ROR']:
        code=opcode + regToBin(token[1][0]) + regToBin(token[1][1]) + regToBin(token[1][2]) + "00000000000000" + subOpcode

    elif token[0] in ['ANDI','ORI','NANDI','NORI','XORI','ADI','SBI','MULI','DIVI','REMI','LSLI','LSRI','ASLI','ROLI','RORI']:
        code=opcode + regToBin(token[1][0]) + regToBin(token[1][1]) + "0" + immToBin(token[1][2]) + subOpcode

    elif token[0] in ['ADC','SBB']:
        code=opcode + regToBin(token[1][0]) + regToBin(token[1][1]) + regToBin(token[1][2]) + "00000000000000" + subOpcode
                    
    elif token[0]=="LDR":
        code=opcode + regToBin(token[1][0]) + "0000" + tobin(16,token[1][1]) + "0000"
    
    elif token[0]=="STR":
        code=opcode + "000" + regToBin(token[1][0]) + "0" + immToBin(token[1][1])+"0000"

    elif token[0]=="LDRG":
        code=opcode + regToBin(token[1][0]) + "000"+regToBin(token[1][1]) +"000000000000000000"
    
    elif token[0]=="STRG":
        code=opcode + "000" + regToBin(token[1][0]) + regToBin(token[1][1]) + "000000000000000000"

    elif token[0]=="LDI":
        code=opcode+regToBin(token[1][0])+"0000"+immToBin(token[1][1])+"0000"
    
    elif token[0]=="MOV":
        code=opcode + regToBin(token[1][0]) + regToBin(token[1][1]) + "000000000000000000000"
    
    elif token[0]=="SVPC":
        code=opcode + regToBin(token[1][0]) + "000000000000000000000000"
    
    elif token[0]=="STPC":
        code=opcode + "000000" + regToBin(token[1][0]) + "000000000000000000"
    
    elif token[0]=="CMP":
        code=opcode + "000" + regToBin(token[1][0]) + regToBin(token[1][1]) + "00000000000000" + "0111"
    
    elif token[0]=="CMI":
        code=opcode + "000" + regToBin(token[1][0]) + "0" + immToBin(token[1][1]) + "0111"
    
    elif token[0] in ['J','JEQ','JNQ','JLT','JGT','JLE','JGE']:
        code=opcode + '0000000' +immToBin(token[1][0]) + "0" + subOpcode

    elif token[0] in ['JAL','JEQL','JNQL','JLTL','JGTL','JLEL','JGEL']:
        code=opcode + '0000000' +immToBin(token[1][0]) + "1" + subOpcode

    elif token[0]=='RET':
        code=opcode +"000000"+"110"+"000000000000000000"
                             #rb=r6
    elif token[0]=='RETR':
        code=opcode +"000000"+regToBin(token[1][0])+"000000000000000000"

    elif token[0]=='IOS':
        code=opcode +'000'+regToBin(token[1][0])+ '00000000000000000' + tobin(5,token[1][1])
    
    elif token[0]=='IOR':
        code=opcode +regToBin(token[1][0])+'00000000000000000000' + tobin(5,token[1][1])
    
        
    elif token[0]=='CLF':
        code=opcode + "0000000000000000000000000000"

    elif token[0]=="RST":
        code=opcode + "0000000000000000000000000000"
    
    elif token[0]=="SLP":
        code=opcode + "0000000" + immToBin(token[1][0]) + "0000"

    elif token[0]=="SLR":
        code=opcode + "000"+ regToBin(token[1][0])+"000000000000000000000"
    
    elif token[0]=="HLT":
        code=opcode + "000000000000000000000000000"
    else:
        error(token[0]+': unidentified operation')

    return code


def convertVar(line):
    val=tobin(16,line[0][1])
    return val

def HEX(code):  #BINARY TO HEX CONVERTER USED IN POSTPROCESSING
    i=0
    out=''
    for i in range(0,len(code),4):
        x=code[i:i+4]
        if x=='0000':
            out=out+'0'
        elif x=='0001':
            out=out+'1'
        elif x=='0010':
            out=out+'2'
        elif x=='0011':
            out=out+'3'
        elif x=='0100':
            out=out+'4'
        elif x=='0101':
            out=out+'5'
        elif x=='0110':
            out=out+'6'
        elif x=='0111':
            out=out+'7'
        elif x=='1000':
            out=out+'8'
        elif x=='1001':
            out=out+'9'
        elif x=='1010':
            out=out+'a'
        elif x=='1011':
            out=out+'b'
        elif x=='1100':
            out=out+'c'
        elif x=='1101':
            out=out+'d'
        elif x=='1110':
            out=out+'e'
        elif x=='1111':
            out=out+'f'
    #print "HEX"+out
    return out


#1#separate address field, opname, parameters 
#2) replace vars and labels
def secondpass(code,LABELS,VARIABLES):

    tmp=[]
    hexcode=''
    for line in code:
        # tokenize format line=[address, opname, [operands]]
        line=tokenize(line)

        # substitute variables and labels
        line=substitute(line,VARIABLES,LABELS)
        
        add=str(hex(int(line[0]))).replace('0x','')
        if type(line[1])==str: #it is a stATEMENT
            # generate bytecode
            binary=identify(line[1:])
        elif type(line[1])==list:
            binary=convertVar(line[1:])
        x=(HEX(binary))
        if len(x)>4:
            x=x[:4]+' '+x[4:]
        #print binary
        hexcode=hexcode+add+': '+x+'\n'
    return hexcode
    