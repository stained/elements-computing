// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// while (1==1) {
// 	// check keypress
// 	if (key_mem == 0) {
// 		// clear screen with white
// 		clearScreen(0);
// 	} else {
// 		// clear screen with black (11111111111)
// 		clearScreen(-1);
// 	}
// }
// 
// function clearScreen(value) {
// 	// we can only set mem 16 bits at a time
//	// so get row	
//	for (row=0;row<8191;row++) {
//		screenmem[row] = value
// 	}
// }

	// reset to 0
	@screenval
	M=0

// Put your code here.
(LOOP)
	// get current keyboard memory value
	@KBD
	D=M

	// if D = 0 (no key), goto SET0
	@SET0
	D;JEQ

	// if D > 0 (keypress), goto SET1
	@SET1
	D;JGT

	// loop
	@LOOP
	0;JMP

(SET0)
	// check current screen val
	// goto loop if already 0
	@screenval
	D=M
	@LOOP
	D;JEQ

	// set screenval to 0
	@screenval
	M=0

	// clear screen
	@CLEAR
	0;JMP

(SET1)
	// check current screen val
	// goto loop if already -1
	@screenval
	D=M
	@LOOP
	D;JLT

	// set screenval to 16x1s (-1)
	@screenval
	M=-1

	// clear screen
	@CLEAR
	0;JMP


(CLEAR)
	// get and store screen memory location into @screenindex
	@SCREEN
	D=A

	@screenindex
	M=D

	// loop 8191 rows (registers)
	@rowindex
	M=0

	(ROWLOOP)
		// get current screen val and put into D
		@screenval
		D=M

		// get current pixel address
		@screenindex
		A=M
		M=D

		// increment screenindex
		@screenindex
		M=M+1

		// increment rowindex
		@rowindex
		M=M+1

 		// check whether we've reached all 8191 rows
		@rowindex
		D=M

		@8192
		D=A-D

		// continue in row loop if 8191 - rowindex > 0
		@ROWLOOP
		D;JGT

	// all done	
	// go back to loop
	@LOOP
	0;JMP


