    .data
prime_msg:  .asciiz "Prime number: "
newline:    .asciiz "\n"
limit:      .word 100

    .text
    .globl main

main:
    # Load the limit from memory
    lw $t0, limit

    # Initialize the sieve array
    li $t1, 0               # Counter
    li $t2, 0               # Current number
    li $t3, 0              # Start from 2 (first prime number)
    li $t4, 20             # Size of the sieve array
    la $t5, sieve_array     # Address of the sieve array

    sieve_init_loop:
        sw $t2, ($t5)      # Store the current number in the sieve array
        addi $t2, $t2, 1   # Increment the current number
        addi $t1, $t1, 1   # Increment the counter
        addi $t5, $t5, 4   # Move to the next element in the sieve array
        bne $t1, $t4, sieve_init_loop

    # Perform the Sieve of Eratosthenes
    move $t1, $zero         # Reset the counter
    li $t2, 2               # Start from 2 (first prime number)
    la $t5, sieve_array     # Address of the sieve array

    sieve_loop:
        beqz $t2, sieve_next    # Skip if the number is already marked as composite

        sieve_inner_loop:
            lw $t3, ($t5)      # Load the current number from the sieve array
            add $t6, $t3, $t2  # Calculate the multiple

            beqz $t6, sieve_next        # Skip if the multiple is zero
            blt $t4, $t6, sieve_next    # Skip if the multiple exceeds the limit

            addi $t7, $t5, 4     # Address of the multiple in the sieve array
            sll $t8, $t6, 2     # Multiply the multiple by 4 to get the offset
            add $t7, $t7, $t8   # Calculate the address of the multiple

            sw $zero, ($t7)     # Mark the multiple as composite

            addi $t2, $t2, 1    # Increment the current number
            j sieve_inner_loop

    sieve_next:
        addi $t1, $t1, 1        # Increment the counter
        addi $t2, $t2, 1        # Increment the current number
        addi $t5, $t5, 4        # Move to the next element in the sieve array
        blt $t1, $t4, sieve_loop

    # Print the prime numbers
    li $v0, 4               # Print string
    la $a0, prime_msg
    syscall

    move $t1, $zero         # Reset the counter
    la $t5, sieve_array     # Address of the sieve array

    print_loop:
        lw $t2, ($t5)       # Load the current number from the sieve array

        bnez $t2, print_prime    # Branch if the number is not zero

        addi $t1, $t1, 1    # Increment the counter
        addi $t5, $t5, 4    # Move to the next element in the sieve array
        blt $t1, $t4, print_loop

    # Exit the program
    li $v0, 10              # Exit program
    syscall

print_prime:
    # Print the prime number
    li $v0, 1               # Print integer
    move $a0, $t2           # Load the prime number into argument register
    syscall

    li $v0, 4               # Print newline
    la $a0, newline
    syscall

    addi $t1, $t1, 1        # Increment the counter
    addi $t5, $t5, 4        # Move to the next element in the sieve array
    blt $t1, $t4, print_loop

    j sieve_next            # Jump to sieve_next label

    .data
sieve_array: .space 400   # Allocate space for the sieve array (100 integers)

    .text
    .globl __start
__start:
    j main
