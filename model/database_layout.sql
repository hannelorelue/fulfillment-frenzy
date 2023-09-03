CREATE TABLE Suppliers(
    SupplierId INTEGER PRIMARY KEY,
    SuppliersName TEXT NOT NULL,
    AddressId INTEGER NOT NULL
);

CREATE TABLE Products(
    ProductId INTEGER PRIMARY KEY, 
    ProductName TEXT NOT NULL,
    Manufacturer TEXT NOT NULL,
    SupplierId INTEGER,
    Cost NUMERIC, -- what does it cost to buy this product from the supplier
    Price NUMERIC -- for how much is this product sold
);

CREATE TABLE Addresses(
    AddressId INTEGER PRIMARY KEY,
    Street TEXT NOT NULL,
    HouseNumber TEXT NOT NULL,
    ZipCode TEXT NOT NULL,
    CoordinateX REAL NOT NULL,
    CoordinateY REAL NOT NULL
);

CREATE TABLE Customers(
    CustomerId INTEGER PRIMARY KEY,
    CustomerName TEXT NOT NULL,
    AddressId INTEGER NOT NULL
);

CREATE TABLE Warehouses(
    WarehouseId INTEGER PRIMARY KEY,
    WarehouseName TEXT NOT NULL,
    AddressId INTEGER NOT NULL
);

CREATE TABLE Inventory(
    WarehouseId INTEGER PRIMARY KEY,
    ProductId INTEGER NOT NULL,
    Stock INTEGER NOT NULL, -- contraint to greater equal 0 
    Capacity INTEGER NOT NULL -- contraint to greater equal 0 
);

CREATE TABLE CustomerOrders(
    OrderId INTEGER PRIMARY KEY,
    CustomerId INTEGER NOT NULL,
    OrderDate TEXT NOT NULL, 
    InvoiceId TEXT NOT NULL,
    FulfillmentDate TEXT,
    Total NUMERIC NOT NULL -- since prices can change the total is not calculated from the Products table
);

CREATE TABLE CustomerOrderDetails(
    OrderId INTEGER NOT NULL,
    ProductId INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    TotalPrice NUMERIC NOT NULL
);

CREATE TABLE SupplierOrders(
    OrderId INTEGER NOT NULL,
    SupplierId INTEGER NOT NULL,
    OrderDate TEXT NOT NULL, 
    InvoiceId TEXT NOT NULL,
    FulfillmentDate TEXT,
    Total NUMERIC NOT NULL -- since prices can change the total is not calculated from the Products table
);

CREATE TABLE SupplierOrderDetails(
    OrderId INTEGER NOT NULL,
    ProductId INTEGER NOT NULL,
    Quantity NUMERIC NOT NULL,
    Total NUMERIC NOT NULL
);
