## LASR: Lineage Aggregation for SARS-CoV-2 using Recursion
LASR aggregates all known SARS-CoV-2 lineages based on their closest parent, as specified in the lineage.yml file from [outbreak.info](https://github.com/outbreak-info/outbreak.info/tree/master). The process involves checking each lineage in lineage.yml to determine if it is included as a callout-group (COG) in a user defined file. If a lineage is not immediately identified in the COG file, LASR then recursively identifies the closest related parent that matches one listed in the COG file. The final output is structured into three main columns, designed to facilitate further downstream analysis. You can read [how we use recursion](CallOutRecursion.md) more generally in the link.

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
python3 LASR.py --download
```
This will download and save the **lineage.yml** in the current working directory. This file is used as input for the `--lineage` flag. 

### Runnign LASR

To run LASR with the minimal usage:
```
python3 LASR.py --lineage lineage.yml --cog cog_file.csv
```
This will produce the output file called **COG.tsv**

Users can rename the output file prefix using the `--output option`, modify the delimiter with the `--extension {t,c}` option, and add additional features related to the **lineage.yml** file using the `--full option`, as desired.

The `--recombinants` flag is intended for **exploratory purposes only** and is not utilized in the NWSS implementation of this algorithm. When used, all lineages that are not assotiated with a *parant* but do have *recombinant_parents* as defined in the **lineage.yml** file will be aggregated to the "Recombinant" COG classification in the final output. The default "Recombinant" HEX color can be changed with the `--reco_color` flag. Note that when used with a lower number of COGs, the number of "Recombinants" increases.

### Help Menu
```
usage: LASR.py [-h] [-c file] [-l file] [-r] [-x hex color] [-o file] [-e {t,c}] [-f] [-d]

LASR: Lineage Aggregation for SARS-CoV-2 using Recursion

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