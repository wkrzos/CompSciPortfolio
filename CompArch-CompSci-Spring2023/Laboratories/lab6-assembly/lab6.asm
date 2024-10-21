    .data
prime_msg:  .asciiz "Prime number: "
newline:    .asciiz "\n"

    .text
    .globl main

main:
    # Assign lower and upper bounds
    li $s0, 1      # Lower bound
    li $s1, 100    # Upper bound

    # Initialize registers
    move $t0, $s0      # Counter (current number)
    move $t1, $s1      # Upper bound

    # Initialize registers
    move $t0, $s0      # Counter (current number)
    move $t1, $s1      # Upper bound

loop:
    # Check if the current number is prime
    move $a0, $t0      # Load current number into argument register
    jal is_prime

    # If the current number is prime, print it
    beqz $v0, next     # Branch if not prime
    li $v0, 4         # Print string
    la $a0, prime_msg
    syscall

    li $v0, 1         # Print integer
    move $a0, $t0
    syscall

    li $v0, 4         # Print newline
    la $a0, newline
    syscall

next:
    # Increment the counter
    addi $t0, $t0, 1

    # Check if we reached the upper bound
    ble $t0, $t1, loop

    # Exit the program
    li $v0, 10        # Exit program
    syscall

is_prime:
    # Check for edge cases
    blez $a0, not_prime   # Negative numbers are not prime
    beq $a0, 1, not_prime  # 1 is not prime
    beq $a0, 2, prime     # 2 is prime

    # Check divisibility from 2 to sqrt(n)
    li $t2, 2         # Divisor
    li $t3, 0         # Remainder
    sqrt_loop:
        div $a0, $t2          # Divide the number by the divisor
        mfhi $t3              # Get the remainder
        beqz $t3, not_prime   # If remainder is 0, number is not prime
        addi $t2, $t2, 1      # Increment the divisor
        blt $t2, $a0, sqrt_loop

prime:
    li $v0, 1         # Set return value to 1 (number is prime)
    jr $ra

not_prime:
    li $v0, 0         # Set return value to 0 (number is not prime)
    jr $ra
