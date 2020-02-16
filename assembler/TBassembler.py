import firstpass as p1
import secondpass as p2
import sys
import os

HEADER="v3.0 hex words addressed\n"
LABELS={}
VARIABLES={}


#--------------------------------------------------------------------------------------
def error(txt): #DISPLAYS ERROR MESSAGE AND EXITS
    sys.exit("\n---"+txt+"---\n\nfile assembling unsuccessful...")

def generatefile(txt,name): #GENERATES O/P FILE
    name=name.replace(".txt","")
    f_out=open(name+"_bytecode.txt","w+")
    f_out.write(txt)
    f_out.close()
    sys.exit("\nAssembling sucessful: bytecode generated....\n\nOutput file:"+name+"_bytecode.txt")
    return True       



#--------------------------------------------------------------------------------------
debugflag=0
Aflag=0

if len(sys.argv)<2:
    error("assembler error: filename missing in argument---\n use \n>>>python Tbassembler <filename>.txt\n     or\n>>>python Tbassembler <filepath/filename>.txt"     )
elif len(sys.argv)>3:
    error("assembler error: too many arguments---")
else:
    filename=sys.argv[1]
    
    if len(sys.argv)==3:
        if sys.argv[2]=='-d':
            debugflag=1
        else:
            error(' '+sys.argv[2]+': unidentified argument')
    
    print("filename: "+filename)
    
    try:
        f=open(filename,"r")
        code=f.readlines()
        f.close
        
        [code,LABELS,VARIABLES]=p1.firstpass(code) 
        if debugflag==1:
            print('----------------pass1---------------------')
            print('\ncode: ')
            for x in code:
                ad=int((x.split(' ')[0]).strip())
                hexad=hex(ad)
                print(hexad+x.replace(str(ad),''))  #prints address in hex
            print('\nvariables: ')
            print(VARIABLES)
            print('\nLABELS:')
            print(LABELS)
          
        code=p2.secondpass(code,LABELS,VARIABLES)
        code=HEADER+code
        if debugflag==1:
            print("----------------pass2---------------------\n")
            print(code)
        generatefile(code,filename)

    except IOError:
        error("assembler error: file not found or is inaccessable---")


