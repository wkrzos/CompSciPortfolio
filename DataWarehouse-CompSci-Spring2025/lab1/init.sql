CREATE TABLE Szpital (
    NIP           VARCHAR(10)  NOT NULL PRIMARY KEY,
	REGON		  VARCHAR(10) NOT NULL,
    Nazwa         VARCHAR(100) NOT NULL,
    Telefon       VARCHAR(30),
    TypSzpital    VARCHAR(50)  NOT NULL,   -- references TypSzpital(Nazwa)
    DataZalozenia DATE         NOT NULL,

    CONSTRAINT FK_Szpital_TypSzpital
        FOREIGN KEY (TypSzpital) REFERENCES TypSzpital(Nazwa)
);

CREATE TABLE Oddzial (
    SzpitalNIP VARCHAR(10)  NOT NULL,
    Nazwa      VARCHAR(100) NOT NULL,
    Lokalizacja       VARCHAR(500),

    CONSTRAINT PK_Oddzial
        PRIMARY KEY (SzpitalNIP, Nazwa),

    CONSTRAINT FK_Oddzial_Szpital
        FOREIGN KEY (SzpitalNIP) REFERENCES Szpital(NIP)
);

CREATE TABLE Gabinet (
    Numer         VARCHAR(50)  NOT NULL PRIMARY KEY,
    SzpitalNIP    VARCHAR(10)  NOT NULL,
    OddzialNazwa  VARCHAR(100) NOT NULL,
    Nazwa          VARCHAR(500),
	Lokalizacja          VARCHAR(500),

    CONSTRAINT FK_Gabinet_Oddzial
        FOREIGN KEY (SzpitalNIP, OddzialNazwa)
        REFERENCES Oddzial (SzpitalNIP, Nazwa)
);

CREATE TABLE Lekarz (
    PWZ             VARCHAR(20) NOT NULL PRIMARY KEY,
    Imie            VARCHAR(50) NOT NULL,
    Nazwisko        VARCHAR(50) NOT NULL,
    Email           VARCHAR(100),
    Specjalizacja   VARCHAR(50) NOT NULL,  -- references Specjalizacja(Nazwa)
    StopienZawodowy VARCHAR(50) NOT NULL,  -- references StopienZawodowy(Nazwa)

    CONSTRAINT FK_Lekarz_Specjalizacja
        FOREIGN KEY (Specjalizacja) REFERENCES Specjalizacja(Nazwa),
    CONSTRAINT FK_Lekarz_StopienZawodowy
        FOREIGN KEY (StopienZawodowy) REFERENCES StopienZawodowy(Nazwa)
);

CREATE TABLE Pacjent (
    KodPacjenta VARCHAR(20) NOT NULL PRIMARY KEY,
    Imie        VARCHAR(50) NOT NULL,
    Nazwisko    VARCHAR(50) NOT NULL,
    Email       VARCHAR(100)
);

CREATE TABLE Choroba (
    KodICD10         VARCHAR(10)  NOT NULL PRIMARY KEY,
    Nazwa            VARCHAR(100),
    Opis             VARCHAR(500),
    KategoriaChorob  VARCHAR(50),
    PrzebiegChoroba  VARCHAR(50),

    CONSTRAINT FK_Choroba_KategoriaChorob
        FOREIGN KEY (KategoriaChorob) REFERENCES KategoriaChorob(Nazwa),
    CONSTRAINT FK_Choroba_PrzebiegChoroba
        FOREIGN KEY (PrzebiegChoroba) REFERENCES PrzebiegChoroba(Nazwa)
);

CREATE TABLE Wizyta (
    LekarzPWZ      VARCHAR(20)  NOT NULL,
    PacjentKod     VARCHAR(20)  NOT NULL,
    DataWizyta     DATE         NOT NULL,
    GodzinaWizyta  TIME         NOT NULL,
    GabinetNumer   VARCHAR(50)  NULL,

    CONSTRAINT PK_Wizyta
        PRIMARY KEY (LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta),

    CONSTRAINT FK_Wizyta_Lekarz
        FOREIGN KEY (LekarzPWZ) REFERENCES Lekarz(PWZ),
    CONSTRAINT FK_Wizyta_Pacjent
        FOREIGN KEY (PacjentKod) REFERENCES Pacjent(KodPacjenta),
    CONSTRAINT FK_Wizyta_Gabinet
        FOREIGN KEY (GabinetNumer) REFERENCES Gabinet(Numer)
);

CREATE TABLE Diagnoza (
    LekarzPWZ       VARCHAR(20) NOT NULL,
    PacjentKod      VARCHAR(20) NOT NULL,
    DataWizyta      DATE        NOT NULL,
    GodzinaWizyta   TIME        NOT NULL,
    KodICD10        VARCHAR(10) NOT NULL,
    DataWystawienia DATE        NOT NULL,
	Opis        VARCHAR(500),

    CONSTRAINT PK_Diagnoza
        PRIMARY KEY (
            LekarzPWZ,
            PacjentKod,
            DataWizyta,
            GodzinaWizyta,
            KodICD10,
            DataWystawienia
        ),

    CONSTRAINT FK_Diagnoza_Wizyta
        FOREIGN KEY (LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta)
        REFERENCES Wizyta (LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta),

    CONSTRAINT FK_Diagnoza_Choroba
        FOREIGN KEY (KodICD10) REFERENCES Choroba(KodICD10)
);

CREATE TABLE Zabieg (
    Nazwa            VARCHAR(100) NOT NULL PRIMARY KEY,
    LekarzPWZ        VARCHAR(20)  NOT NULL,
    PacjentKod       VARCHAR(20)  NOT NULL,
    DataWizyta       DATE         NOT NULL,
    GodzinaWizyta    TIME         NOT NULL,
    DataWystawienia  DATE         NOT NULL,
    Opis             VARCHAR(500),
	Koszt             VARCHAR(100),

    CONSTRAINT FK_Zabieg_Wizyta
        FOREIGN KEY (LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta)
        REFERENCES Wizyta(LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta)
);

CREATE TABLE Recepta (
    Kod             VARCHAR(50)  NOT NULL PRIMARY KEY,
    LekarzPWZ       VARCHAR(20)  NOT NULL,
    PacjentKod      VARCHAR(20)  NOT NULL,
    DataWizyta      DATE         NOT NULL,
    GodzinaWizyta   TIME         NOT NULL,
    DataWystawienia DATE         NOT NULL,
    Opis            VARCHAR(500),
	Lek          VARCHAR(500),
	Dawkowanie            VARCHAR(500),
	Zalecenia          VARCHAR(500),

    CONSTRAINT FK_Recepta_Wizyta
        FOREIGN KEY (LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta)
        REFERENCES Wizyta(LekarzPWZ, PacjentKod, DataWizyta, GodzinaWizyta)
);
