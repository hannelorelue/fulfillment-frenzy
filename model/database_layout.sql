CREATE TABLE Products(
    ProductId TEXT PRIMARY KEY Unique, 
    ProductName TEXT NOT NULL,
    Manufacturer TEXT,
    SupplierId INTEGER,
    Cost NUMERIC, -- what does it cost to buy this product from the supplier
    Price NUMERIC -- for how much is this product sold
);

CREATE TABLE Addresses(
    AddressId INTEGER PRIMARY KEY Unique,
    Street TEXT,
    HouseNumber TEXT,
    ZipCode TEXT,
    CoordinateX REAL,
    CoordinateY REAL
);

CREATE TABLE Suppliers(
    SupplierId INTEGER PRIMARY KEY Unique,
    SuppliersName TEXT,
    AddressId INTEGER
);

CREATE TABLE Customers(
    CustomerId INTEGER PRIMARY KEY Unique,
    CustomerName TEXT,
    AddressId INTEGER
);

CREATE TABLE Warehouses(
    WarehouseId INTEGER PRIMARY KEY Unique,
    WarehouseName TEXT,
    AddressId INTEGER
);

CREATE TABLE Inventory(
    WarehouseId INTEGER PRIMARY KEY Unique,
    ProductId INTEGER,
    Stock INTEGER, -- contraint to greater equal 0 
    Capacity INTEGER -- contraint to greater equal 0 
);

CREATE TABLE CustomerOrders(
    OrderId INTEGER PRIMARY KEY Unique,
    CustomerId INTEGER,
    OrderDate TEXT, 
    InvoiceId TEXT,
    FulfillmentDate TEXT,
    Total NUMERIC -- since prices can change the total is not calculated from the Products table
);

CREATE TABLE CustomerOrderDetails(
    OrderId INTEGER,
    ProductId INTEGER,
    Quantity INTEGER,
    TotalPrice NUMERIC
);

CREATE TABLE SupplierOrders(
    OrderId INTEGER,
    SupplierId INTEGER,
    OrderDate TEXT, 
    InvoiceId TEXT,
    FulfillmentDate TEXT,
    Total NUMERIC -- since prices can change the total is not calculated from the Products table
);

CREATE TABLE SupplierOrderDetails(
    OrderId INTEGER,
    ProductId INTEGER,
    Quantity NUMERIC,
    Total NUMERIC
);

-- TODO foreign keys
