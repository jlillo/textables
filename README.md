# TeXtables
 Create LaTeX tables from CSV tables with appropriate decimal figures taking into account
 accounting the significant figures from the uncertainties. 


### Basic parameters

| Input     | Explanation                                                                                 |
| :-------- | :-------------                                                                              |
| File      | Path to the CSV file that you want to convert. The file must be comma-separated with column headers indicating the name of the parameter. Columns corresponding to with column headers indicating the name of the parameter. Columns corresponding to uncertainties of each parameter (e.g., named "Param") should be named as follows: i) Symetric uncertainties: "eParam", ii) Assymetric uncertainties: "elParam", "euParam". If no uncertainty colum is found matching this nomenclature, then the number of significant decimal figures used for the Param values will correspond to that specified in the --nsig option (default=6 for "BJD" columns and 4 for any other).    |               
|--nsig    |  [Integer] Number of significant figures by default for columns with no corresponding uncertainties  |
|--join    |  [Boolean] Join the values and uncertainties in a single column like  $XX \pm YY$ (symetric uncertainties) or $XX^{+YY}_{-ZZ}$ (asymetric uncertainties).|

Output      
-------
texTable    # LaTeX table obtained from the original CSV but this time including the latex format and 
                appropriate number of significant decimal figures. The table will be written int he same 
                directory as the original file and with the same filename but ending with ".tex" 


### Usage

To 

```
 python textables.py example_table.csv --JOIN
```

