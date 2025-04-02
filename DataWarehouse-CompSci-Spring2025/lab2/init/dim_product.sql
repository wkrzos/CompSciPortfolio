-- Dim_Product
-- Using INTO this way is fast and simple but requires us to later set up the constraints later
SELECT   -- * here means a virtual schema so we can simply write schema
    p.ProductID, p.Name, p.ListPrice, p.Color,
    sc.Name AS SubCategoryName,
    c.Name  AS CategoryName
INTO [Dim_Product]
FROM [AdventureWorks2019].[Production].[Product] AS p
JOIN [AdventureWorks2019].[Production].[ProductSubcategory] AS sc
    ON p.ProductSubcategoryID = sc.ProductSubcategoryID
JOIN [AdventureWorks2019].[Production].[ProductCategory] AS c
    ON sc.ProductCategoryID = c.ProductCategoryID;