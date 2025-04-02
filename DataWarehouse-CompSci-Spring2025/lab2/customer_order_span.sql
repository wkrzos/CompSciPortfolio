-- Liczba dni pomiędzy pierwszym i ostatnim złożonym przez klientów zamówieniem

WITH CustomerOrderDates AS (
    SELECT 
        c.CustomerID,
        c.LastName + ', ' + c.FirstName AS CustomerName,
        MIN(f.OrderDate) AS FirstOrderDate,
        MAX(f.OrderDate) AS LastOrderDate
    FROM [Fact_Orders] AS f
    JOIN [Dim_Customer] AS c ON f.CustomerID = c.CustomerID
    GROUP BY c.CustomerID, c.LastName, c.FirstName
)
SELECT 
    CustomerName AS 'Nazwisko, imię',
    FORMAT(FirstOrderDate, 'yyyy-MM-dd') AS 'Pierwsze',
    FORMAT(LastOrderDate, 'yyyy-MM-dd') AS 'Ostatnie',
    DATEDIFF(day, FirstOrderDate, LastOrderDate) AS 'Liczba dni'
FROM CustomerOrderDates
WHERE DATEDIFF(day, FirstOrderDate, LastOrderDate) > 0 -- Wykluczamy klientów z tylko jednym zamówieniem
ORDER BY 'Liczba dni' DESC, CustomerName;
