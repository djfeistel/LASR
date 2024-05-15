## TRACE: Tracking and Reporting Aggregated COVID-19 Emergences

Creating a meaninful visualization of SARS-CoV-2 relative abundance lineage estiamtes detected in and across wastewater samples can be challanging to accurately represent variations or interactions within a single visual format due the high number of distinct lineages. To overcome this, TRACE aggregates all known SARS-CoV-2 lineages into a single proxy lineage based on a least common ancestor. These proxy SARS-CoV-2 lineages are labeled "callout-groups" (COGs). The COG is user-defined and is represented by a known SARS-CoV-2 variant of interest (VOI) or concern (VOC) serving as the representative for all those descendant lineages. Aggregating SARS-CoV-2 lineages into COGs based on a least common ancestor facilitates a more streamlined visualization of the SARS-CoV-2 relative abundance estimates found in wastewater samples.

TRACE aggregates lineages into COGs by their least common ancestor using the **lineage.yml** file from the [outbreak.info github](https://github.com/outbreak-info/outbreak.info/tree/master) and a user-defined COG file. and creates a new three column dataframe file where each row represents a lineage, COG, and a color code.
 
 The new file is use for visualizing the relative abundance of aggregated SARS-CoV-2 lineages found in wastewater samples. 

The process involves checking each lineage in lineage.yml to determine if it is included as a callout-group (COG) in a user defined file. If a lineage is not immediately identified in the COG file, TRACE then recursively identifies the closest related parent that matches one listed in the COG file. The final output is structured into three main columns, designed to facilitate further downstream analysis. You can read [how we use recursion](CallOutRecursion.md) more generally in the link.

This methodology has been adopted by the National Wastewater Surveillance System [NWSS](https://www.cdc.gov/nwss/index.html) as part of its NWSS and Improved dashboard.

## Dependencies
Install the following libraries by running:  
```
pip install PyYAML pandas requests
```

## Usage
### Callout-groups (COG) file curation

The COG file is a user-defined, manually cureated two column file with each row functioning as the proxy lineage for the aggregated group (typically a VOI or VOC). The first column represents the COG and the second column is a unique HEX color:

| COG  | HEX     |
|------|---------|
| BA.2 | #090909 |
| JN.1 | #839472 |
| KP.2 | #639940 |

*example above of COG file*

1. The COG file should be in *TSV* or *CSV* format with or without a header
2. COG file can take on any prefix name
3. No limit to the number of COGs

### Downloading lineage.yml file

A user can download the latest **lineage.yml** file directly from the outbreak.info guthub under the [curated_reports_prep](https://github.com/outbreak-info/outbreak.info/tree/master/curated_reports_prep) directory using the command:  
```
python3 TRACE.py --download
```
This will download and save the **lineage.yml** in the current working directory, and will overwrite any preexisting lineage.yml files.

### Runnign TRACE

To run TRACE with the minimal usage:
```
python3 TRACE.py --lineage lineage.yml --cog cog_file.csv
```
This will produce the output file called **COG.tsv**. Users can rename the output file prefix using `--output`, modify the delimiter to TSV (default) or CSV with `--extension`, and add additional features related to the **lineage.yml** file using `--full` if desired.

When setting `--recombinants`, lineages that are only assotatied with a *recombinant_parents* as defined in the **lineage.yml** file will be aggregated to the "Recombinant" COG classification (default is to aggregate to "Other"). The default "Recombinant" HEX color can be changed with the `--reco_color` flag.

### Output

When using the minimal usage of TRACE, he final output returns a three column file:
1. **lineage**: name of the lineage as defined in the lineage.yml file under the *name* key
2. **cog**: callout-group assotiated with the lineage
3. **hex**: HEX color

When the `--full` flag is set, four additioinal columns are added to the final output:
4. **parent**: The lineage's parent as defined in the lineage.yml file under the *parent* key (NA if *parent* is not listed as a key)
5. **recombinant_parents**: The lineage's recombinant parents as defined in the lineage.yml file under the *recombinant_parents* key (NA if *recombinant_parents* is not listed as a key)
6. **alias**: The lineage's alias name as defined in the lineage.yml file under the *alias* key
7. **children**: The children of a lineage as defined in the lineage.yml file under the *children* key

### Help Menu for TRACE
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