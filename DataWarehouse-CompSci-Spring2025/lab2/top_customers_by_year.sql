-- Klienci z największą liczbą zamówień w poszczególnych latach przekraczających 130 000 brutto

WITH CustomerYearlySummary AS (
    -- Grupa zamówień według klienta i roku, zlicza zamówienia i sumuje wartości
    SELECT 
        c.CustomerID,
        c.LastName + ', ' + c.FirstName AS CustomerName,
        YEAR(f.OrderDate) AS OrderYear,
        COUNT(DISTINCT f.LineTotal) AS OrderCount,
        SUM(f.LineTotal) AS YearlyTotal
    FROM [Fact_Orders] AS f
    JOIN [Dim_Customer] AS c ON f.CustomerID = c.CustomerID
    GROUP BY c.CustomerID, c.LastName, c.FirstName, YEAR(f.OrderDate)
    HAVING SUM(f.LineTotal) > 130000
),
RankedCustomers AS (
    SELECT 
        CustomerID,
        CustomerName,
        OrderYear,
        OrderCount,
        YearlyTotal,
        ROW_NUMBER() OVER (PARTITION BY OrderYear ORDER BY OrderCount DESC, YearlyTotal DESC) AS Rank
    FROM CustomerYearlySummary
)
SELECT 
    OrderYear AS 'Rok',
    CustomerName AS 'Nazwisko, imię',
    OrderCount AS 'Liczba zam.',
    FORMAT(YearlyTotal, 'C', 'us-US') AS 'Kwota'
FROM RankedCustomers
WHERE Rank = 1
ORDER BY OrderYear;
