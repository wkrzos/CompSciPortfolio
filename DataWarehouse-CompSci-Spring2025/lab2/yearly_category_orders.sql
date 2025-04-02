SELECT
    YEAR(f.OrderDate) AS 'Year',
    p.CategoryName AS 'Category',
    SUM(f.LineTotal) AS 'Kwota',
    COUNT(*) AS 'Liczba zamówień'
FROM [Fact_Orders] AS f
JOIN [Dim_Product] AS p ON f.ProductID = p.ProductID
GROUP BY YEAR(f.OrderDate), p.CategoryName
ORDER BY p.CategoryName, YEAR(f.OrderDate);
