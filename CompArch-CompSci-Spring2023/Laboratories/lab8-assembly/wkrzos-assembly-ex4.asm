#=============================================
.eqv STACK_SIZE 2048

#=============================================
.data

# obszar na zapamiętanie adresu stosu systemowego
sys_stack_addr:	.word 0

# deklaracja własnego obszaru stosu
stack:	.space STACK_SIZE

# array z instrukcji do ćwiczenia; int global_array[10] = { 1,2,3,4,5,6,7,8,9,10}
global_array: .word 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
global_array_size: .word 10

# ============================================
.text

# czynności inicjalizacyjne
sw $sp, sys_stack_addr 		# zachowanie adresu stosu systemowego
la $sp, stack+STACK_SIZE 	# zainicjowanie obszaru stosu

# początek programu programisty - zakładamy, że main 
# wywoływany jest tylko raz
main:

	# przed skokiem do sum
	# double check this one, could be 12
	subiu $sp, $sp, 12			# int suma (4) + rezerwujemy meijsce na zmienne funkcji (8); 4 + 8 = 12
	
	la $t0, global_array		# peirwsza zmienna 
	sw $t0, 4($sp)		 
	
	lw $t0, global_array_size	# druga zmienna
	sw $t0, 0($sp) 	
		
	jal sum			# skok do labela sum
	
	# powrót po skoku do sum
	lw $t0, ($sp)		# wczytujemy wartość zwróconą w obliczeniach po skoku; $sp aktualnei na 12
	sw $t0, 12($sp)		# w 12 na stacku zapisujemy wynik obliczeń; s = sum(global_array, 10)
	
	addiu $sp, $sp, 12		# $sp w tym miejscu wskazuje na 24, gdzie 20 było array address
	
	lw $a0, ($sp)		# drukujemy wynik w konsoli
	li $v0, 1		
	syscall

	# koniec podprogramu main:
	addiu $sp, $sp, 4	# opróżniamy stack z suma (int s)

	lw $sp, sys_stack_addr	 	# odtworzenie wskaźnika stosu
							# systemowego
	li $v0, 10
	syscall
	
sum:

	subiu $sp, $sp, 8 		# adres do powrotu i wynik obliczeń; rezerwacja miejsca na stosie
	sw $ra, ($sp) 		# odkładamy adres powrotu na stos (użyliśmy jal, więc w $ra
				# znajduje się adres powrotu; zapisujemy w $sp)
	subiu $sp, $sp, 8		# rezerwacja miejsca na stosie dla int s, i
	
	# w tym miejscu odnieś się do ilustracji wizualizującej kolejność danych na stacku
	
	sw $zero, ($sp)		# jak w podanym kodzie; s = 0
	
	# operacje na array
	lw $t0, 16($sp)		# wczytujemy array_size do $t0
	subi $t0, $t0, 1		# zmniejszamy array_size o 1 (wykrozystujemy już tę liczbę); array_size - 1
	sw $t0, 4($sp)		# ustawiamy wartość i na nową wielkość array; i = array_size - 1
	
# while loop odpowiadający temu w wymaganiach;
whileloop:

	lw $t0, 4($sp)	# ta linia kodu nie jest potrzebna w założeniach assembly,
				#  jednak jeżeli traktujemy ten obszar jako pamięć, należy ponownie to wczytać

	bltz $t0, endwhileloop 	# while (i >= 0)
	
	# obliczenia na array adress
	lw $t0, 4($sp)		# wczytujemy int i (odpowiadający wielkości array)
	lw $t1, 20($sp)		# wczytujemy array adress
	
	sll $t0, $t0, 2		# mnożymy i x 4; sll bardziej optymalne od mul 
	
	add $t0, $t1, $t0	# array adress offset o $t0 bajtów (i x 4) 
	lw $t0, ($t0)		# wczytujemy wartość pod obliczonym adresem
	
	# obliczenia na s
	lw $t1, ($sp)		# wczytujemy s
	add $t1, $t1, $t0	# dosłowny kod z polecenia; s + array[i]
	sw $t1, ($sp)		# dosłowny kod z polecenia; s = s + array[i]
	
	# obliczenia na i
	lw $t0, 4($sp)		# wczytujemy i
	subi $t0, $t0, 1		# dosłowny kod z polecenia; i - 1
	sw $t0, 4($sp)		# dosłowny kod z polecenia; i = i - 1
	
	j whileloop	
	
endwhileloop:

	lw $t0, ($sp)		# wczytujemy wynik obliczeń s
	sw $t0, 12($sp)		# zapisujemy zwracaną wartość w 12 (wynik) 
	
	addiu $sp, $sp, 8		# usuwamy niepotrzebne zmienne lokalne 
	
	lw $ra, ($sp)		# wczytuje adres powrotny zapisany wcześniej 
				# do $ra w celu wykonania skoku
	
	addiu $sp, $sp, 4		# przesuwamy stack pointer na wynik do zwrócenia
	
	jr $ra			# używająć wcześńiej zapisanego $ra, wracamy do main
