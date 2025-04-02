-- Fact_Orders

SELECT
	sod.[ProductID], sod.[OrderQty], sod.[UnitPrice], sod.[UnitPriceDiscount], sod.[LineTotal],
	soh.[CustomerID], soh.[OrderDate], soh.[ShipDate]
INTO [Fact_Orders]
FROM [AdventureWorks2019].[Sales].[SalesOrderDetail] AS sod
JOIN [AdventureWorks2019].[Sales].[SalesOrderheader] AS soh
	ON sod.SalesOrderID = soh.SalesOrderID

-- PK
ALTER TABLE [Dim_Product] 
ADD CONSTRAINT PK_Dim_Product PRIMARY KEY ([ProductID]);

ALTER TABLE [Dim_Customer] 
ADD CONSTRAINT PK_Dim_Customer PRIMARY KEY ([CustomerID]);

-- FK
ALTER TABLE [Fact_Orders] 
ADD CONSTRAINT FK_FactOrders_DimProduct FOREIGN KEY ([ProductID]) 
REFERENCES [Dim_Product]([ProductID]);

ALTER TABLE [Fact_Orders] 
ADD CONSTRAINT FK_FactOrders_DimCustomer FOREIGN KEY ([CustomerID]) 
REFERENCES [Dim_Customer]([CustomerID]);
