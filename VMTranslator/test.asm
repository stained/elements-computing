	// set up

	// SP
	@256
	D=A
	@SP
	M=D

	// LCL
	@300
	D=A
	@LCL
	M=D

	// ARG
	@400
	D=A
	@ARG
	M=D

	// THIS
	@3000
	D=A
	@THIS
	M=D

	// THAT
	@3010
	D=A
	@THAT
	M=D

	// push constant 10
	@10		// constant value
	D=A 	// set to D

	@SP		// load stack pointer
	A=M		// load pointer
	M=D		// push
	M=M+1	

	// pop local 0
	@0		// offset 
	D=A 	
	@LCL	
	D=D+M 	// pointer to LCL memory + offset
	@R13	// store mem address in R13 temp
	M=D
	@SP		// decrement stack pointer
	M=M-1
	A=M		// load pointer
	D=M		// pop value into D
	@R13
	A=M 	// load LCL + offset mem address
	M=D 	// set value 

	// test increment 
	M=D+1

	// push local 0
	@0		// offset 
	D=A 	
	@LCL	
	A=D+M 	// pointer to LCL memory + offset
	D=M   	// get value = 11?

	@SP		// load stack pointer
	A=M		// load pointer
	M=D		// push
	@SP		// increment stack pointer
	M=M+1	

	// push constant 12
	@12		// constant value
	D=A 	// set to D
	@SP		// load stack pointer
	A=M		// load pointer
	M=D		// push
	@SP		// increment stack pointer
	M=M+1	

	// add
	@SP		// decrement stack pointer
	M=M-1
	A=M		// load pointer
	D=M		// pop value into D
	@SP		// decrement stack pointer
	M=M-1	
	A=M	
	M=D+M 	// add!
	@SP		// increment stack pointer
	M=M+1	



