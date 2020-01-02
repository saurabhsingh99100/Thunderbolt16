#---------implementation of stack library----------------
#
.push
    SBI R7,R7,1     #DECREMENT SP
    STRG TR,R7      #STORE AT SP
    RET

.pop
    LDRG TR,R7
    ADI R7,R7,1
    RET

.peek
    LDRG TR,R7
    RET
    

#------------SINGLE REGISTER OPS-------------------

.pushPC
    MOV TR,PC
    JAL push    

.pushLR
    MOV TR,LR
    JAL push
    










.pushRegs
                	#save lr to tr before any function call

    MOV TR,LR   #LR (R6)
    JAL push

    MOV TR,R0
	JAL push	#R0

	MOV TR,R1
	JAL push	#R1

	MOV TR,R2
	JAL push	#R2

	MOV TR,R3
	JAL push	#R3

	MOV TR,R4
	JAL push	#R4

	RET

.popRegs
                	#save lr to tr before any function call
	MOV TR,LR

	JAL pop		#R4
	MOV R4,R0

	JAL pop		#R3
	MOV R3,R0

	JAL pop		#R2
	MOV R2,R0

	JAL pop		#R1
	MOV R1,R0

	JAL pop		#R0

	#restore lr
	MOV LR,TR

	RET

.pushPc
                #pushes program counter onto stack
