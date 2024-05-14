# LASR
## Lineage Aggregation of SARS-CoV-2 genomes using Recursion
LASR aggregates all known SARS-CoV-2 lineages based on their closest parent, as specified in the lineage.yml file from outbreak.info. The process involves checking each lineage in lineage.yml to determine if it is included as a Callout Group (COG) in the COG file. If it is not identified in teh COG file, LASR then recursively identifies the closest related parent lineage that matches one listed in the COG file. The final output is structured into three main columns, designed to facilitate further downstream analysis.

This methodology has been adopted by the National Wastewater Surveillance System (NWSS) as part of its NWSS and Improved dashboard.

### Dependencies
The following libraries are required:
`pip install PyYAML pandas`  

### Usage

```
LASR: Lineage Aggregation of SARS-CoV-2 genomes using Recursion

optional arguments:
  -h, --help            show this help message and exit
  -c file, --cog file   Callout-group (COG) file. Two column file with lineage and hex color (TSV or CSV format, no header)
  -l file, --lineage file
                        lineage.yml file
  -o file, --output file
                        Name of output file (without extention)
  -e {t,c}, --extension {t,c}
                        File extension for output: "t" for TSV, "c" for CSV [default=t]
  -f, --full            Write detailed output file (includes additional information for each named lineage)
  -d, --download        Download lineage.yml from from outbreak.info github
  ```

