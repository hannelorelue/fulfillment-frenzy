CREATE SEQUENCE SeqAddressId START 1; 

CREATE TABLE Addresses(
    AddressId INTEGER PRIMARY KEY DEFAULT NEXTVAL('SeqAddressId'),
    Street TEXT NOT NULL,
    HouseNumber TEXT,
    City TEXT NOT NULL,
    ZipCode TEXT NOT NULL,
    Country TEXT NOT NULL,
    CoordinateX REAL NOT NULL,
    CoordinateY REAL NOT NULL
);

CREATE TABLE Suppliers(
    SupplierId INTEGER PRIMARY KEY,
    SuppliersName TEXT NOT NULL,
    AddressId INTEGER NOT NULL REFERENCES Addresses (AddressId)
);

CREATE TABLE Customers(
    CustomerId INTEGER PRIMARY KEY,
    CustomerName TEXT NOT NULL,
    AddressId INTEGER NOT NULL REFERENCES Addresses (AddressId)
);

CREATE TABLE Warehouses(
    WarehouseId INTEGER PRIMARY KEY,
    WarehouseName TEXT NOT NULL,
    AddressId INTEGER NOT NULL REFERENCES Addresses (AddressId)
);

CREATE TABLE Products(
    ProductId INTEGER PRIMARY KEY, 
    ProductName TEXT NOT NULL,
    Manufacturer TEXT NOT NULL,
    Cost DECIMAL(32,2), -- what does it cost to buy this product from the supplier
    Price DECIMAL(32,2), -- for how much is this product sold
    SupplierId INTEGER REFERENCES Suppliers (SupplierId)
);

CREATE TABLE Inventory(
    WarehouseId INTEGER NOT NULL REFERENCES Warehouses (WarehouseId),
    ProductId INTEGER NOT NULL REFERENCES Products (ProductId),
    Stock INTEGER NOT NULL, -- contraint to greater equal 0 
    Capacity INTEGER NOT NULL, -- contraint to greater equal 0 
    PRIMARY KEY (WarehouseId, ProductId)
);

CREATE TABLE CustomerOrders(
    OrderId INTEGER PRIMARY KEY,
    CustomerId INTEGER NOT NULL REFERENCES Customers (CustomerId),
    OrderDate TEXT NOT NULL, 
    InvoiceId TEXT NOT NULL,
    FulfillmentDate DATETIME,
    Total DECIMAL(32,2) NOT NULL -- since prices can change the total is not calculated from the Products table
);

CREATE TABLE CustomerOrderDetails(
    OrderId INTEGER NOT NULL REFERENCES CustomerOrders (OrderId),
    ProductId INTEGER NOT NULL REFERENCES Products (ProductId),
    Quantity INTEGER NOT NULL,
    TotalPrice NUMERIC NOT NULL, -- since prices can change the total is not calculated from the Products table
    PRIMARY KEY (OrderId, ProductId)
);

CREATE TABLE SupplierOrders(
    OrderId INTEGER PRIMARY KEY,
    SupplierId INTEGER NOT NULL REFERENCES Suppliers (SupplierId),
    OrderDate TEXT NOT NULL, 
    InvoiceId TEXT NOT NULL,
    FulfillmentDate DATETIME,
    Total DECIMAL(32,2) NOT NULL -- since prices can change the total is not calculated from the Products table
);

CREATE TABLE SupplierOrderDetails(
    OrderId INTEGER NOT NULL REFERENCES SupplierOrders (OrderId),
    ProductId INTEGER NOT NULL REFERENCES Products (ProductId),
    Quantity NUMERIC NOT NULL,
    Total DECIMAL(32,2) NOT NULL, -- since prices can change the total is not calculated from the Products table
    PRIMARY KEY (OrderId, ProductId)
);

