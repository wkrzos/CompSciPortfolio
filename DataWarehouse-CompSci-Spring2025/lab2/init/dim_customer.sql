-- Dim_Customer

SELECT
	c.CustomerID,
	p.FirstName, p.LastName,
	s.Name AS TerritoryName, s.CountryRegionCode, s.[Group]
INTO [Dim_Customer]
FROM [AdventureWorks2019].[Person].[Person] AS p
JOIN [AdventureWorks2019].[Sales].[Customer] AS c
	ON p.BusinessEntityID = c.PersonID
JOIN [AdventureWorks2019].[Sales].[SalesTerritory] AS s
	ON c.TerritoryID = s.TerritoryID
