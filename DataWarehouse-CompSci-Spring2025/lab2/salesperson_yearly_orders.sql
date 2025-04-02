WITH SalesPersonYearlyOrders AS (
    SELECT 
        f.SalesPersonID AS 'Pracownik',
        YEAR(f.OrderDate) AS 'Rok',
        COUNT(DISTINCT f.LineTotal) AS 'Liczba'
    FROM [Fact_Orders] AS f
    WHERE f.SalesPersonID IS NOT NULL
    GROUP BY f.SalesPersonID, YEAR(f.OrderDate)
)
SELECT 
    Pracownik,
    Rok,
    Liczba,
    SUM(Liczba) OVER (PARTITION BY Pracownik ORDER BY Rok) AS 'Razem'
FROM SalesPersonYearlyOrders
ORDER BY Pracownik, Rok;
