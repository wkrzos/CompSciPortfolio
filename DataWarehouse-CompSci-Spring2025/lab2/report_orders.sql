-- Report: Zamówienia(Nazwisko, imię, Kategoria produktu, Nazwa produktu, Cena)

SELECT 
    c.LastName + ', ' + c.FirstName AS 'Nazwisko, imię',
    p.CategoryName AS 'Kategoria produktu',
    p.Name AS 'Nazwa produktu',
    f.UnitPrice AS 'Cena'
FROM [Fact_Orders] AS f
JOIN [Dim_Customer] AS c 
    ON f.CustomerID = c.CustomerID
JOIN [Dim_Product] AS p 
    ON f.ProductID = p.ProductID
ORDER BY c.LastName, c.FirstName, p.CategoryName, p.Name
OFFSET 0 ROWS FETCH NEXT 1000 ROWS ONLY;
