.data
	upper_boundary:	.word	1	# The upper boundary of a randomly generated number

	prompt1_1:	.asciiz	"Welcome to the game! Guess a number between 0 and "
	prompt1_2:	.asciiz	" try to guess the number, the one who's closer to it wins!\n"

	prompt2_1:		.asciiz	"\n===== ROUND "
	prompt2_2:		.asciiz	" ====="

	prompt3:			.asciiz	"Guess the number: "

	prompt4:		.asciiz	"You've won!"
	prompt5:		.asciiz	"You've lost..."

	prompt6_1:		.asciiz	"Your score is "
	prompt6_2:		.asciiz	" points out of "
	prompt6_3:		.asciiz	" rounds."

.text
	main:
		# print the welcoming message
		li $v0, 4 
		la $a0, prompt1_1
		syscall

		li $v0, 1
		lw $a0, upper_boundary
		syscall

		li $v0, 4
		la $a0, prompt1_2
		syscall

		# initialise round number
		add $s0, $zero, $s0

	# ========= ARGUMENTS ============
	# $s0 - round counter
	#
	# $t1 - generated number
	# $t2 - user input, then user input diffrence from generated number
	# $t3 - computer input, then computer input difference from generated number

	loop:

		# increment the round number
		 add $s0, $s0, 1

		# print ===== ROUND ===== 

		li $v0, 4
		la $a0, prompt2_1
		syscall

		li $v0, 1
		add $a0, $zero , $s0
		syscall

		li $v0, 4
		la $a0, prompt2_2
		syscall

		# generate random number within game's set boundaries		

		li $v0, 41
		syscall
		add $t1, $zero, $a0

		# ask for user input
		 
		li $v0, 4
		la $a0, prompt3
		syscall

		li $v0, 5
		syscall
		move $t2, $a0	# use of pseudoinstructions

		# check user input
		sub $t2, $t1, $t2	# difference from generated number

		sra $t5, $t2, 31
		xor $t2, $t2, $t5	# absolute value
		sub $t2, $t2, $t5
		
		# check computer input
		sub $t3, $t1, $t3

		sra $t5, $t3, 31
		xor $t3, $t3, $t5
		sub $t3, $t3, $t5

		# compare both differences
		

	user_wins_round:

	computer_wins_round:

	no_winners_round:
		
	end:

		

		li $v0, 10
		syscall



	

		

		
