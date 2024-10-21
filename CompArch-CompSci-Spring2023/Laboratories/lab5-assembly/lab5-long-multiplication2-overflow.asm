.data
# Przypisujemy pamiec statyczna dla komunikatow
prompt1: .asciiz "Wprowadz 1 liczbe: "
prompt2: .asciiz "Wprowadz 2 liczbe: "
result: .asciiz "Wynik: "
overflow: .asciiz "Nastapilo przepelnienie. Status: "

# Przypisujemy pamiec statyczna naszym zmiennym
num1: .word 0
num2: .word 0
res: .word 0
status: .word 0
# Ostatecznie postanowilem uzywac zmiennych temporary ($t*), jest to drobna modyfikacja;
# Uzycie zmiennych to zmiana ladowania odczytu z konsoli i uzycie instrukcji sw oraz lw

.text
.globl main

main:
    # Poproszenie uzytkownika o podanie pierwszej liczby
    li $v0, 4   # ladujemy instrukcje do printowania string w konsoli
    la $a0, prompt1   # ladujemy string z wiadomoscia do $a0 (z $a0 korzysta syscall 4)
    syscall # wykonujemy instrukcje systemowa, wyswietlajac prompt1

    # Odczytanie pierwszej liczby
    li $v0, 5   # ladujemy instrukcje read integer
    syscall # czytamy input uzytkownika 
    sw $t0, num1
    move $t0, $v0   # kopiujemy zawartosc instrukcji do $t0 (poniewaz wartosc odczytana $v0 zaraz sie zmieni, tak jak i wykonywana instrukcja)
    
    # Poproszenie uzytkownika o podanie drugiej liczby, komentarze analogiczne do tych powyzej
    li $v0, 4
    la $a0, prompt2
    syscall

    # Odczytanie drugiej liczby
    li $v0, 5
    syscall
    sw $t1, num2
    move $t1, $v0

    # Obliczanie iloczynu
    li $t2, 0       # Ustawienie $t2 na zero, uzywane do przechowywania wyniku
    li $t3, 1       # Ustawienie $t3 na 1 dla kontrolowania przesuniecia bitowego
    li $t4, 0       # Ustawienie $t4 na zero do sledzenia przepełnienia

multiply:
    andi $t5, $t1, 1     # Pobranie najmniej znaczacego bitu (LSB) z $t1 i ustawienie $t5 na jego wartość
    beq $t5, $zero, skip # Jesli $t5 jest zerem, przejdz do instrukcji skip, nie wykonujemy dodawania, tylko shift

    addu $t6, $t2, $t0   # Dodanie $t0 do $t2 bez sprawdzania przepełnienia, przechowywane w $t6 (patrz nastepny komentarz)
    sltu $t7, $t6, $t2   # Sprawdzenie, czy dodawanie spowodowalo przepełnienie, jezeli wynik z aktualnej iteracji jest mniejszy od tego z poprzedniej, to nastapilo przepełnienie
    addiu $t4, $t4, 1    # Zwiekszenie licznika przepełnienia ($t4)

    beqz $t7, skip_overflow  # Jezeli nie wystapilo przepełnienie, pomin obsluge przepełnienia tj. dla 0 nie ma przepełnienia, dla 1 nastapilo przepełnienie

    # Obsluga przepełnienia
    li $v0, 4   # zaladowanie instrukcji syscall: print integer
    la $a0, overflow   # kopia string o overflow do $a0 (wymaganej przy tej instrukcji)
    syscall # print wiadomosci

    li $v0, 1   # zaladowanie instrukcji syscall: print integer
    move $a0, $t7   # kopia wartosci licznika overflow do $a0 (wymaganie instrukcji)
    syscall # wyswietlenie wartosci status

    # Zakonczenie programu
    li $v0, 10   # zaladowanie instrukcji zakonczenia programu
    syscall # zakonczenie programu

skip_overflow:
    move $t2, $t6   # zmienna nie przepełnila sie po dodaniu, wiec kopiujemy ja do wyniku

skip:
    sll $t0, $t0, 1         # Przesuniecie $t0 w lewo, jak w mnozeniu pisemnym
    srl $t1, $t1, 1         # Przesuniecie $t1 w prawo, wybranie nastepnego bitu w liczbie
    sll $t3, $t3, 1         # Przesuniecie $t3 w lewo, jak w mnozeniu pisemnym
    bne $t1, $zero, multiply    # Jezeli $t1 nie jest zerem, wroc do multiply; kod kontynuuje, dopoki nie jest zerem

    # Zapisanie wyniku w pamieci
    sw $t2, res	# Zachowujemy wynik w pamięci statycznej; przydatne, jeżeli program bylby dalej rozwijany, a interesowalby nas tylko wynik

    # Wyswietlenie wyniku
    li $v0, 4
    la $a0, result
    syscall

    li $v0, 1
    lw $a0, res
    syscall

    # Zakonczenie programu
    li $v0, 10
    syscall
