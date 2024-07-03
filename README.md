# TeXtables
 Create LaTeX tables from CSV tables with appropriate decimal figures taking into account
 accounting the significant figures from the uncertainties. 


### Basic parameters

| Input     | Explanation                                                                                 |
| :-------- | :-------------                                                                              |
| File      | Path to the CSV file that you want to convert. The file must be comma-separated with column headers indicating the name of the parameter. Columns corresponding to with column headers indicating the name of the parameter. Columns corresponding to uncertainties of each parameter (e.g., named "Param") should be named as follows: i) Symetric uncertainties: "eParam", ii) Assymetric uncertainties: "elParam", "euParam". If no uncertainty colum is found matching this nomenclature, then the number of significant decimal figures used for the Param values will correspond to that specified in the --nsig option (default=6 for "BJD" columns and 4 for any other).    |               
|--nsig    |  [Integer] Number of significant figures by default for columns with no corresponding uncertainties  |
|--JOIN    |  [Boolean] Join the values and uncertainties in a single column like  $XX \pm YY$ (symetric uncertainties) or $XX^{+YY}_{-ZZ}$ (asymetric uncertainties).|

### Output
The output is a LaTeX table obtained from the original CSV but this time including the latex format and 
appropriate number of significant decimal figures. The table will be written int he same directory as 
the original file and with the same filename but ending with ".tex" 


### Installation and Usage
To use this code just clone or download this repository. The use it as follows:

1. Prepare your CSV table including the columns you want and specifying the column names as indicated above 
in the input "File".
2. Run the code using the required options (see below)

In the exaxmple_table.csv file you will find the follwing table including the Julkian date (column 1), 
the radial velocity (column 2), and its symetric uncertainty (column 3), with a large number of decimal digits: 

|BJD|RV|eRV|
|---|---|---|
|59397.64267499978|-23.290480994083612|0.0021458383964393|
|59403.647097200155|-23.292125557479164|0.002215711153444|
|59408.61682320014|-23.293933623992555|0.0021519362764250|
|59412.629282100126|-23.29134659370688|0.0020812284867629|
|59420.60012269998|-23.293718054199708|0.0021417367672328|
|59425.66288019996|-23.30405301036821|0.00223620588643153|
|59430.654212600086|-23.28968928174525|0.0017688107443666|
|59446.684781299904|-23.28855896541092|0.0019754197127090|
|59455.644156400114|-23.295624341977987|0.001898223531465|
|59460.694884200115|-23.297414805950652|0.002026704163577|

We want to move this to a publishable LaTeX table. Let's do it with two options:

#### Joint column of value and uncertainties:
- If you want a single column including the value and uncertainty then run with "--JOIN" option, then run as follows:

```
 python textables.py example_table.csv --JOIN
```
 
This will produce the following table:

\begin{table} \n
\begin{tabular}{cc} \n
BJD & RV \\ \n
59397.642675 & $-23.2905 \pm 0.0021$ \\ \n
59403.647097 & $-23.2921 \pm 0.0022$ \\ \n
59408.616823 & $-23.2939 \pm 0.0022$ \\ \n
59412.629282 & $-23.2913 \pm 0.0021$ \\ \n
59420.600123 & $-23.2937 \pm 0.0021$ \\ \n
59425.662880 & $-23.3041 \pm 0.0022$ \\ \n
59430.654213 & $-23.2897 \pm 0.0018$ \\ \n
59446.684781 & $-23.2886 \pm 0.0020$ \\ \n
59455.644156 & $-23.2956 \pm 0.0019$ \\ \n
59460.694884 & $-23.2974 \pm 0.0020$ \\ \n
\end{tabular} \n
\end{table}  \n

#### Separated columns for value and uncertainties:
- If you want the uncertainties in a separate column, then run as follows:

```
 python textables.py example_table.csv
```
 
This will produce the following table:

\begin{table}
\begin{tabular}{ccc}
BJD & RV & $\sigma_{\rm RV}$ \\
59397.642675 & -23.2905 & 0.0021 \\
59403.647097 & -23.2921 & 0.0022 \\
59408.616823 & -23.2939 & 0.0022 \\
59412.629282 & -23.2913 & 0.0021 \\
59420.600123 & -23.2937 & 0.0021 \\
59425.662880 & -23.3041 & 0.0022 \\
59430.654213 & -23.2897 & 0.0018 \\
59446.684781 & -23.2886 & 0.0020 \\
59455.644156 & -23.2956 & 0.0019 \\
59460.694884 & -23.2974 & 0.0020 \\
\end{tabular}
\end{table}
