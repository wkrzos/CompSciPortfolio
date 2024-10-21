.data
prompt1: .asciiz "Enter the first number: "
prompt2: .asciiz "Enter the second number: "
result: .asciiz "The result is: "

licz1: .word 0
licz2: .word 0
wyn: .word 0
status: .word 0

.text
.globl main

main:
    # Prompt the user to enter the first number
    li $v0, 4
    la $a0, prompt1
    syscall

    # Read in the first number
    li $v0, 5
    syscall
    move $t0, $v0

    # Prompt the user to enter the second number
    li $v0, 4
    la $a0, prompt2
    syscall

    # Read in the second number
    li $v0, 5
    syscall
    move $t1, $v0

    # Calculate the product
    li $t2, 0       # Set $t2 to zero, used for storing the result
    li $t3, 1       # Set $t3 to 1 for bit shifting

multiply:
    andi $t4, $t1, 1     # Get the LSB (Least Significant Bit) of $t1 and set $t4 to its value
    beq $t4, $zero, skip # If $t4 is zero, skip the add instruction

    add $t2, $t2, $t0    # Add $t0 to $t2
    

skip:
    sll $t0, $t0, 1     	# Shift $t0 to the left
    srl $t1, $t1, 1     	# Shift $t1 to the right
    sll $t3, $t3, 1     	# Shift $t3 to the left
    bne $t1, $zero, multiply    # If $t1 is not zero, go back to multiply; code continues until it isn't a zero

    # Print the result
    li $v0, 4
    la $a0, result
    syscall

    li $v0, 1
    move $a0, $t2
    syscall

    # Exit the program
    li $v0, 10
    syscall
