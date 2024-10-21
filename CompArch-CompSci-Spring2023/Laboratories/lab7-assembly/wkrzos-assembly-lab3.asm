.data
    RAM:        .space 4096

    prompt1:    .asciiz "Number of rows: "
    prompt2:    .asciiz "Number of columns: "

    prompt3:    .asciiz "\nRead (0) / Write (1): "
    prompt4:    .asciiz "\nErr. Incorrect value. Try 0 or 1."

    prompt5:    .asciiz "Row: "
    prompt6:    .asciiz "Column: "
    prompt7:    .asciiz "New value: "

.text

    ## Pytamy o ilość rzędów nowej tablicy
    li $v0, 4       # Print string z pytaniem o ilość rzędów
    la $a0, prompt1
    syscall

    li $v0, 5
    syscall         # Zapis ilości kolumn do $s1
    move $s1, $v0

    ## Pytamy o ilość kolumn nowej tablicy
    li $v0, 4       # Print string z pytaniem o ilość kolumn
    la $a0, prompt2
    syscall

    li $v0, 5
    syscall         # Zapis ilości kolumn do $s0
    move $s0, $v0

    mul $s2, $s1, 4    # number of rows * 4; size of memory taken up by the row address array
    move $t0, $s2    # address of the first (empty) cell of the new matrix

    # loop 1
calculate_and_fill_array:
    sw $t0, RAM($t1)    # temporary; zapisujemy adres obecnej liczby w array; adres wiersza; 
    			# store $t0 into adress RAM with offset $t1
    			
    li $t2, 0       # resetujemy $t2, żeby zacząć od początku kolumny
    mul $t4, $t3, 100    # liczymy nową bazę liczby (jak podpowiedziano przy ostatnim sprawdzeniu); $t4 = i * 100

	# patrz na spis wartości

    # loop 2: do wypełnienia tablicy wartościami
	fill_array:
   	 # loop
   	 addi $t4, $t4, 1    # do base value dodajemy kolejno 1 otrzymując 0 + 1, 0 + 2, 0 + 3, ...
   	 sw $t4, RAM($t0)    # zapisujemy w tablicy

   	 addi $t0, $t0, 4    # zwiększamy kolumnę o 4, czyli o wielkość .word,
                  	     # żeby przejść do następnego miejsca w array
   	 addi $t2, $t2, 1    # dodajemy 1 do licznika obecnej kolumny

   	 bne $t2, $s0, fill_array    # tak długo jak nasz temporary liczba kolumn ($t2) nie będzie równa ogólnej liczbie kolumn ($s0),
                              	  # to kontynuujemy loop branchując do fill_array
  	  # end loop
   	 addi $t3, $t3, 1    # dodajemy 1 do temporary row
   	 addi $t1, $t1, 4    # dodajemy 4 (.word w byte) do adresu wierszy

   	 blt $t3, $s1, calculate_and_fill_array    # powtarzamy loop dopóki nie wypełnimy wszystkich wierszy

ask_for_action:
    # Ask for action
    li $v0, 4
    la $a0, prompt3
    syscall

    li $v0, 5
    syscall
    move $t0, $v0  # Move the input value to $t0 (or $a0)

    beq $t0, 0, read    # Branch if input is 0
    beq $t0, 1, write   # Branch if input is 1

    li $v0, 4
    la $a0, prompt4
    syscall

    j ask_for_action   # Jump back to the beginning to ask for action again

read:
    # pytamy i zapisujemy liczbę wiersza (indeksy od 0)
    li $v0, 4
    la $a0, prompt5    # print string
    syscall

    li $v0, 5
    syscall        # zapis input
    move $s1, $v0

    # pytamy i zapisujemy liczbę kolumny (indeksy od 0)
    li $v0, 4
    la $a0, prompt6    # pirnt string
    syscall

    li $v0, 5
    syscall        # zapis input
    move $s0, $v0

    # obliczenia na adresach
    mul $t0, $s1, 4    # adres wiersza w tablicy wierszy
    lw $t0, RAM($t0)    # ładujemy adres wiersza
    mul $t1, $s0, 4    # liczymy adres kolumny (*4 przez .word = 4 byte)

    # obliczamy ostateczny adres w drugiej tablicy (tablicy wartości)
    add $s2, $t0, $t1

    ## interakcja z użytkownikiem

    li $v0, 1
    lw $a0, RAM($s2)    # drukujemy int
    syscall


    j ask_for_action    # powrót do pytania o ask_for_action

write:
    # pytamy i zapisujemy liczbę wiersza (indeksy od 0)
    li $v0, 4
    la $a0, prompt5    # print string
    syscall

    li $v0, 5
    syscall        # zapis input
    move $s1, $v0

    # pytamy i zapisujemy liczbę kolumny (indeksy od 0)
    li $v0, 4
    la $a0, prompt6    # print string
    syscall

    li $v0, 5
    syscall        # zapis input
    move $s0, $v0

    # obliczenia na adresach
    mul $t0, $s1, 4    # adres wiersza w tablicy wierszy
    lw $t0, RAM($t0)    # ładujemy adres wiersza
    mul $t1, $s0, 4    # liczymy adres kolumny (*4 przez .word = 4 byte)

    # obliczamy ostateczny adres w drugiej tablicy (tablicy wartości)
    add $s2, $t0, $t1

    ## interakcja z użytkownikiem
    # pytanie o nową wartość
    li $v0, 4
    la $a0, prompt7
    syscall

    # zapisujemy nową wartość
    li $v0, 5
    syscall

    # zapisujemy wartość do obliczonego adresu
    sw $v0, RAM($s2)

    j ask_for_action # wracamy do pytania o dalszą akcję
