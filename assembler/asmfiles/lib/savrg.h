
.saveRegs
	#save lr to tr before any function call
	MOV TR,LR

	JAL push	#R0

	MOV R0,R1
	JAL push	#R1

	MOV R0,R2
	JAL push	#R2

	MOV R0,R3
	JAL push	#R3

	MOV R0,R4
	JAL push	#R4

	#restore lr
	MOV LR,TR

	RET

.restoreRegs
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
