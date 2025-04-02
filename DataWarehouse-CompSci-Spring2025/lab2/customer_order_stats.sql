-- Liczba dni pomiędzy pierwszym i ostatnim złożonym przez klientów zamówieniem
-- wraz z liczbą złożonych przez nich zamówień

WITH CustomerOrderStats AS (
    SELECT 
        c.CustomerID,
        c.LastName + ', ' + c.FirstName AS CustomerName,
        MIN(f.OrderDate) AS FirstOrderDate,
        MAX(f.OrderDate) AS LastOrderDate,
        COUNT(DISTINCT f.LineTotal) AS OrderCount
    FROM [Fact_Orders] AS f
    JOIN [Dim_Customer] AS c ON f.CustomerID = c.CustomerID
    GROUP BY c.CustomerID, c.LastName, c.FirstName
)
SELECT 
    CustomerID AS 'Klient',
    FORMAT(FirstOrderDate, 'yyyy-MM-dd') AS 'Od',
    FORMAT(LastOrderDate, 'yyyy-MM-dd') AS 'Do',
    DATEDIFF(day, FirstOrderDate, LastOrderDate) AS 'Liczba dni',
    OrderCount AS 'Liczba zam.'
FROM CustomerOrderStats
WHERE DATEDIFF(day, FirstOrderDate, LastOrderDate) > 0 -- Wykluczamy klientów z tylko jednym zamówieniem
ORDER BY 'Liczba dni' DESC;
