## TRACE: Tracking and Reporting Aggregated COVID-19 Emergences
TRACE aggregates all known SARS-CoV-2 lineages based on their closest parent, as specified in the lineage.yml file from [outbreak.info](https://github.com/outbreak-info/outbreak.info/tree/master). The process involves checking each lineage in lineage.yml to determine if it is included as a callout-group (COG) in a user defined file. If a lineage is not immediately identified in the COG file, TRACE then recursively identifies the closest related parent that matches one listed in the COG file. The final output is structured into three main columns, designed to facilitate further downstream analysis. You can read [how we use recursion](CallOutRecursion.md) more generally in the link.

This methodology has been adopted by the National Wastewater Surveillance System [NWSS](https://www.cdc.gov/nwss/index.html) as part of its NWSS and Improved dashboard.

## Dependencies
Install the following libraries by running:  
```
pip install PyYAML pandas
```

## Usage
### Callout-groups (COG) file curation

A user must manually create a COG file, where each row functions as the representative lineage for the aggregated group of lineages. The first column should list the COG, and the second column should specify the HEX color.

| COG  | HEX     |
|------|---------|
| BA.2 | #090909 |
| JN.1 | #839472 |
| KP.2 | #639940 |

*example above of COG file*

1. The COG file should be in TSV or CSV format and without a header (though a header should not interfere with the final output)
2. COG file can take on any prefix name
3. No limit to the number of COG lineages
5. Hex color codes are not necessary and a user can redefine these values as needed for other downstream applications/analyses

### Downloading lineage.yml file

A user can download the latest **lineage.yml** file directly from the [outbreak.info](https://github.com/outbreak-info/outbreak.info/tree/master) using the command:  
```
python3 TRACE.py --download
```
This will download and save the **lineage.yml** in the current working directory. This file is used as input for the `--lineage` flag. 

### Runnign TRACE

To run TRACE with the minimal usage:
```
python3 TRACE.py --lineage lineage.yml --cog cog_file.csv
```
This will produce the output file called **COG.tsv**

Users can rename the output file prefix using the `--output option`, modify the delimiter with the `--extension {t,c}` option, and add additional features related to the **lineage.yml** file using the `--full option`, as desired.

The `--recombinants` flag is intended for **exploratory purposes only** and is not utilized in the NWSS implementation of this algorithm. When used, all lineages that are not assotiated with a *parant* but do have *recombinant_parents* as defined in the **lineage.yml** file will be aggregated to the "Recombinant" COG classification in the final output. The default "Recombinant" HEX color can be changed with the `--reco_color` flag. Note that when used with a lower number of COGs, the number of "Recombinants" increases.

### Output

The final output when using the minimal usage of TRACE returns a file called **COG.tsv** with three columns:
1. lineage: name of the lineage as defined in the lineage.yml file
2. cog: callout-group assotiated with the lineage
3. hex: HEX color

When the `--full` flag is set, four additioinal columns are added to the **COG.tsv** file:
4. parent: lineage parent as defined in the lineage.yml file (NA if "parent" is not listed under a lineage name)
5. recombinant_parents: lineage recombinant parents as defined in the lineage.yml file (NA if "recombinant_parents" is not listed under a lineage name)
6. alias: lineage alias name as defined in the lineage.yml file
7. children: all children found under a the lineage

### Help Menu
```
usage: TRACE.py [-h] [-c file] [-l file] [-r] [-x hex color] [-o file] [-e {t,c}] [-f] [-d]

TRACE: Tracking and Reporting Aggregated COVID-19 Emergences

optional arguments:
  -h, --help            show this help message and exit
  -c file, --cog file   Callout-group (COG) file. Two column file with lineage and hex color (TSV or CSV format, no header)
  -l file, --lineage file
                        lineage.yml file
  -r, --recombinants    Add "Recombinants" to the output file
  -x hex color, --reco_color hex color
                        HEX color for Recombinants [default=#FF00F0 i.e. hot pink]
  -o file, --output file
                        Name of output file (without extention)
  -e {t,c}, --extension {t,c}
                        File extension for output: "t" for TSV, "c" for CSV [default=t]
  -f, --full            Write detailed output file (includes additional information for each named lineage)
  -d, --download        Download lineage.yml from from outbreak.info github
  ```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://www.gnu.org/licenses/) file for details.

Copyright (c) 2024 Dorian J. Feistel