.data
	num1:	.word 12
	num2:  	.word 2
	result:	.word 0
	status: .word 0

.text
.globl main

main:

	#load the variables
	lw $t0, num1	#load num1 in $t0
	lw $t1, num2	#load num2 in $t1
	lw $t2, result	#load res in $t2
	lw $t3, status	#load status in $t3
	
	# zero the result
	li $t2, 0
	
	# https://stackoverflow.com/questions/48619934/mips-overflow-detection-printing-the-result

	multi:
		# taking the Least Significant Bit of num 2
		andi $t5, $t1, 1
		beq $t5, $zero, skipMulti
		
		add $t2, $t2, $t0
	
	skipMulti:
		# 
		sll $t0, $t0, 1
		bne $t1, $zero, multi
		
	

	# print the result in console
	li $v0, 1
	move $a0, $t2
	syscall
	
end:

	
