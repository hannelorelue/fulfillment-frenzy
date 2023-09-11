using Godot;
using System;
using System.Data.Common;
using System.IO;
using System.Linq;
using DuckDB.NET.Data;
using static DuckDB.NET.NativeMethods;
using static Address;
using Dapper;

public partial class MainWindow : Node2D
{
	public override void _Ready() {
		// TODO use relative path
		using var duckDBConnection = new DuckDBConnection("Data Source=/Users/konze/Programming/fulfillment-frenzy/model/database.db");
		duckDBConnection.Open();

		var addresses = duckDBConnection.Query<Address>("SELECT AddressId, Street FROM Addresses");

		foreach(var address in addresses) {
			GD.Print($"{address.AddressId}, {address.Street}");
		}
	}
}
