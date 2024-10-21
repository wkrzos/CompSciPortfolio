.data
    N:      .word   100                 # Zakres początkowych liczb naturalnych
    numbers: .space 404                # Tablica liczb (101 * 4 bytes)
    primes:  .space 404                # Tablica liczb pierwszych (101 * 4 bytes)
    newline: .asciiz "\n"              # Newline character for printing

.text
.globl main
    main:
        # Inicjalizacja tablicy
        li $t0, 1                       # Initialize i = 1
        la $t1, numbers                 # Load address of numbers array
        la $t2, N                       # Load address of N
        lw $t2, 0($t2)                  # Load value of N
    init_loop:
        ble $t0, $t2, init_loop_body    # Branch if i <= N
        j sieve                         # Jump to sieve implementation
    init_loop_body:
        sw $t0, ($t1)                   # Store i in numbers[i]
        addiu $t0, $t0, 1               # Increment i
        addiu $t1, $t1, 4               # Increment array index by 4
        j init_loop                     # Jump to next iteration

    sieve:
        # Implementacja sita Eratostenesa
        li $t3, 2                       # Initialize i = 2
        sqrt_loop:
            mul $t4, $t3, $t3           # Calculate i * i
            bgt $t4, $t2, count_primes   # Branch if i * i > N
            lw $t5, 0($t1)               # Load numbers[i]
            beqz $t5, sqrt_next         # Branch if numbers[i] == 0
            j sqrt_loop_end              # Jump to next iteration
        sqrt_next:
            addu $t4, $t3, $t3          # Calculate 2 * i
            sieve_inner_loop:
                sw $0, 0($t1)            # Store 0 in numbers[j]
                addu $t1, $t1, $t4      # Increment array index by 2 * i
                ble $t1, $t2, sieve_inner_loop  # Branch if j <= N
        sqrt_loop_end:
            addiu $t3, $t3, 1           # Increment i
            j sqrt_loop                 # Jump to next iteration

    count_primes:
        # Liczenie liczby liczb pierwszych
        li $t6, 0                       # Initialize nPrimes = 0
        li $t3, 2                       # Initialize i = 2
        count_loop:
            lw $t5, 0($t1)               # Load numbers[i]
            bnez $t5, count_next        # Branch if numbers[i] != 0
            j count_end                 # Jump to count_end
        count_next:
            addiu $t6, $t6, 1           # Increment nPrimes
        count_end:
            addiu $t3, $t3, 1           # Increment i
            j primes_array               # Jump to primes_array

    primes_array:
        # Zapisywanie liczb pierwszych do tablicy primes
        la $t7, primes                   # Load address of primes array
        addiu $t8, $t6, 1                # Calculate nPrimes + 1
        sll $t9, $t8, 2                  # Multiply by 4 to get byte offset
        li $v0, 9                        # Allocate memory for primes array
        move $a0, $t9                    # Size of memory block to allocate
        syscall                          # System call to allocate memory
        move $t7, $v0                    # Store the address of the allocated memory in $t7
        la $t1, numbers                 # Reset array index

        li $t3, 2                        # Initialize i = 2
        li $t8, 0                        # Initialize index = 0
        primes_loop:
            lw $t5, 0($t1)                # Load numbers[i]
            bnez $t5, primes_next        # Branch if numbers[i] != 0
            j print_primes               # Jump to print_primes
        primes_next:
            sw $t5, 0($t7)                # Store numbers[i] in primes[index]
            addiu $t7, $t7, 4            # Increment array index by 4
            addiu $t8, $t8, 1            # Increment index
        primes_end:
            addiu $t3, $t3, 1            # Increment i
            addiu $t1, $t1, 4            # Increment array index by 4
            j primes_loop                # Jump to next iteration

    print_primes:
        # Wypisywanie liczb pierwszych na konsoli
        move $t7, $v0                    # Restore the address of primes array
        li $v0, 1                        # System call to print integer
        lw $a0, 0($t7)                    # Load a prime number from primes array
        syscall                          # Print the prime number
        la $a0, newline                  # Load address of newline character
        li $v0, 4                        # System call to print string
        syscall                          # Print the newline character
        addiu $t7, $t7, 4                # Increment array index by 4
        j print_end                      # Jump to print_end

    print_end:
        bgt $t8, $t6, main_end          # Branch if index > nPrimes
        j print_primes                  # Jump to next iteration

    main_end:
        li $v0, 10                      # System call to exit the program
        syscall
