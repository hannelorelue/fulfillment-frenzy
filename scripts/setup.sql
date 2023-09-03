CREATE TABLE Products(
  ProductId TEXT PRIMARY KEY Unique, 
  ProductName TEXT NOT NULL,
  Manufcturer TEXT,
  SupplierId TEXT,
  Cost NUMERIC,
  Price NUMERIC
);

CREATE TABLE Suppliers(
    SupplierId TEXT PRIMARY KEY Unique,
    SuppliersName TEXT,
);

CREATE TABLE SupplierAddresses(
    SupplierId TEXT PRIMARY KEY Unique,
    Street TEXT,
    HouseNumber TEXT,
    ZipCode TEXT,
    Street TEXT,
    CoordinateX TEXT,
    CoordinateY TEXT,
);

CREATE TABLE Customers(
    CustomerId TEXT PRIMARY KEY Unique,
    CustomerName TEXT,
);


CREATE TABLE CustomerAddresses(
    CustomerId TEXT PRIMARY KEY Unique,
    Street TEXT,
    HouseNumber TEXT,
    ZipCode TEXT,
    Street TEXT,
    CoordinateX TEXT,
    CoordinateY TEXT,
);

CREATE TABLE Warehouses(
    WarehouseId TEXT PRIMARY KEY Unique,
    ProductId TEXT,
    Stock NUMERIC,
    Max NUMERIC,
);

CREATE TABLE WarehouseAddresses(
    CustomerId TEXT PRIMARY KEY Unique,
    Street TEXT,
    HouseNumber TEXT,
    ZipCode TEXT,
    Street TEXT,
    CoordinateX TEXT,
    CoordinateY TEXT,
);


CREATE TABLE CustomerOrders(
    OrderId TEXT,
    CustomerId TEXT,
    OrderDate date, 
    InvoiceId TEXT,
    FulfillmentDate date,
    Total NUMERIC,
);

CREATE TABLE CustomerOrderDetails(
    OrderId TEXT,
    ProductId TEXT,
    Quantity NUMERIC,
    Price NUMERIC,
);

CREATE TABLE SupplierOrders(
    OrderId TEXT,
    SupplierId TEXT,
    OrderDate date, 
    InvoiceId TEXT,
    FulfillmentDate date,
    Total NUMERIC,
);

CREATE TABLE SupplierOrderDetails(
    OrderId TEXT,
    ProductId TEXT,
    Quantity NUMERIC,
    Price NUMERIC,
);

-- TODO foreign keys