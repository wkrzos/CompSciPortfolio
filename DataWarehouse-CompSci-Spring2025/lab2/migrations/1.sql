-- FK
ALTER TABLE [Fact_Orders] 
ADD CONSTRAINT FK_FactOrders_DimProduct FOREIGN KEY ([ProductID]) 
REFERENCES [Dim_Product]([ProductID]);

ALTER TABLE [Fact_Orders] 
ADD CONSTRAINT FK_FactOrders_DimCustomer FOREIGN KEY ([CustomerID]) 
REFERENCES [Dim_Customer]([CustomerID]);


-- Add dim_salesperson table
SELECT
    sp.BusinessEntityID AS SalesPersonID,
    sp.SalesYTD,
    sp.SalesQuota
INTO [Dim_SalesPerson]
FROM [AdventureWorks2019].[Sales].[SalesPerson] AS sp;


ALTER TABLE [Dim_SalesPerson] 
ADD CONSTRAINT PK_Dim_SalesPerson PRIMARY KEY ([SalesPersonID]);

ALTER TABLE [Fact_Orders]
ADD [SalesPersonID] INT NULL;

UPDATE f
SET f.SalesPersonID = soh.SalesPersonID
FROM [Fact_Orders] AS f
JOIN [AdventureWorks2019].[Sales].[SalesOrderHeader] AS soh
     ON f.LineTotal = soh.SubTotal;

-- New FK
ALTER TABLE [Fact_Orders] 
ADD CONSTRAINT FK_FactOrders_DimSalesPerson FOREIGN KEY ([SalesPersonID]) 
REFERENCES [Dim_SalesPerson]([SalesPersonID]);
