.data

	# Dane wejściowe
	coefs:	.float 	2.3 3.45 7.67 5.32	# wektory przed kolejnymi potegami x
	degree:	.word	3		# stopień wielomianu
	
	# Zbiór komunikatów do interakcji z użytkownikiem
	prompt1: .asciiz "Wprowadz wartosc x: "
	prompt2: .asciiz "Wartosc wielomianu to: "
	prompt3: .asciiz " | Kontynuowac? No (0) / Yes (1) "
	
.text

	main:   
	
	    # pytanie o wartość x 
	    li $v0, 4		# pytanie o wartość x
	    la $a0, prompt1
	    syscall

	    li $v0, 7		# odczytanie wartości double x; zapis odczytu do $f0
	    syscall
	    
	    # skok do podprogramu i przekazanie argumentów
	    mov.d $f2, $f0 	# wartość x; kopia wartości $f0 do $f2; move.d = move double
	    lw $a0, degree	# wczytujemy degree do $a0
	    la $a1, coefs	# wczytujemy adres początku tablicy coefs do $a1
	    
	    jal eval_poly	# skok do eval_poly; $ra = $pc

	    # POWRÓT PO METHODZIE HORNERA

	    # drukujemy wyniki obliczeń programu
	    li $v0, 4
	    la $a0, prompt2	# syscall print string; printujemy prompt2
	    syscall

	    li $v0, 3
	    mov.d $f12, $f0	# syscall print double; printujemy wynik
	    syscall

	    # pytanie o dalszy ciąg programu
	    li $v0, 4
	    la $a0, prompt3	# syscall print string; pytanie o kontynuację
	    syscall

	    li $v0, 5
	    syscall		# syscall read int; 0 - koniec; 1 - kontynuacja
	    move $t0, $v0

	    bnez	 $t0, main 	# branch if not equal 0
	      
	    li $v0, 10
	    syscall
	    
	###########################################################
	#    
	# ====== Argumenty funkcji ======
	# $a0 - stopień wielomianu
    	# $a1 - adres tablicy coefs
	# $t0 - temporary: do obliczeń pętli; degree = degree - 1, 
	# gdzie degree przekazane jest do tego rejestru
    	# $t1 - temporary: adres pozycji w tablicy; w java coefs[degree] 
    	# $f2 - wartość x
    	# $f4 - wartość pozycji w tablicy (patrz równierz $t1)
    	# $f6 - temporary: obecna wartość x; currX = x
    	# $f8 - aktualna wartość wektora (coefs[i])
    	#
    	# ===== Założenia =====
    	# 1. Wszystkie obliczenia wykonywane są na double
    	# 2. Dane do obliczenia (wektory) są we float
    	# 3. Algorytm jest oparty na Horner's Method
    	# 4. Brak interakcji z użytkownikiem w metodzie eval_poly
    	#
    	###########################################################
    	
	eval_poly:

	    # obliczenia na tablicy
	    sll $t1, $a0, 2   # obliczamy offset dla tablicy; używamy sll zamiast mul dla wydajności (2^2 = 4)
			     # skalujemy stopień wielomianu * 4, każdt element coefs jest 4-byteowym floating-point value
			     
	    add $t1, $t1, $a1 # dodajemy offset do podstawowego adresu żeby obliczyć adres elementu coefs. 
	    		     # Index offset reprezentuje ilość elementów do pominięcia od podstawowego adresu. 
	    		     # TL;DR: Do początku tablicy dodajemy offset, żeby zacząć od porządanego miejsca
	    
	    # obliczenia na result
	    lwc1 $f4, ($t1)   # wczytujemy wartość z tablicy na pozycji $t1
	    cvt.d.s $f4, $f4  # zamieniamy odczytaną wartość na double 
	    		     # z single precision (jak w insturkcjach)
   
 	    # obliczenia na x
	    mov.d $f6, $f2	# obecna wartość x, zaczynamy od tej od użytkownika z $t2
    
	    # obliczenia na degree
	    move $t0, $a0    # temporary = degree; inicjalizacja
	    subi $t0, $t0, 1 # odejmujemy 1 od temporary (liczymy indeks od 0)
    
		horner_method:
	
	    		bltz $t0, exit_eval_poly     # skok do exit gdy temporary < 0
	    	
			subi $t1, $t1, 4     # odejmujemy od obliczonego adresu 4 (4 byte), żeby dostać sie do kolejnego wektora
		
			# wczytujemy wartość z obliczonego adresu tablicy
			lwc1 $f8, ($t1)		# zapisujemy wartość z tablicy do $f8
			cvt.d.s $f8, $f8		# zamieniamy wartość na double precission 
		
			# oblcizenia metody hornera,
			# obliczenia result
		
			# result = result + coefs[i] * currX
			mul.d $f8, $f8, $f6  
			add.d $f4, $f4, $f8  
			mul.d $f6, $f6, $f2
		 
			subi $t0, $t0, 1     # obliczenie indexu

			# skok do początku pętli
			j horner_method
		
	exit_eval_poly:
	
        		mov.d $f0, $f4     
	        jr $ra            
