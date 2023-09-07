# Fulfillment Frenzy

## Development Setup

### macOS

 * install .NET 6.0 [https://dotnet.microsoft.com/en-us/download](https://dotnet.microsoft.com/en-us/download)
 * install Godot Engine 4.1.1 - .NET [https://godotengine.org/download/macos/](https://godotengine.org/download/macos/)
 * install DuckDB: `brew install duckdb`


### Windows

 * install .NET 6.0 [https://dotnet.microsoft.com/en-us/download](https://dotnet.microsoft.com/en-us/download)
 * install Godot Engine 4.1.1 - .NET [https://godotengine.org/download/macos/](https://godotengine.org/download/macos/)
 * install DuckDB:
    * download: [https://duckdb.org/docs/installation/](https://duckdb.org/docs/installation/)
    * unzip and move `duckdb` to the desired location e.g.: `C:\Program Files\duckdb\`
    * add `duckdb` to Path variable:
        * press [Win]+[R]
        * enter `sysdm.cpl`
        * select the tab "Advanced"
        * press button "Environment Variables"
        * choose "Environment Variables"
        * select "Path" and press "Edit"
        * select "New"
        * enter the path to the directory in which the `duckdb` binary resides
        * close all dialogs and windows and restart the terminal and enter `duckdb` to confirm that the installation was successful
