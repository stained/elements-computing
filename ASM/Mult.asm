// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// i = 1;
// R2 = 0;

// for (i=0; i > R1; i++) {
// 		R2 = R2 + R0;
//	}

// Put your code here.
	@i
	M=1

	@R2
	M=0

(LOOP)	
	// check whether i is greater than R1

	// load i into D
	@i
	D=M

	// load memory value R1 and subtract from D (i)
	@R1
	D=D-M

	// compare against 0
	@END
	D;JGT				// jump to end if i - R1 > 0

	// nope, so continue

	// load R0
	@R0
	D=M

	// load current sum
	@R2
	M=D+M 				// Increment R2 by R0

	// increment i
	@i
	M=M+1

	@LOOP 				// loop!
	0;JMP

(END)
	@END
	0;JMP				// infinite loop

