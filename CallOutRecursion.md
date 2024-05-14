# TRACE: Tracking and Reporting Aggregated COVID-19 Emergences

TRACE is a tool designed for aggregating and analyzing SARS-CoV-2 lineages. It maps each lineage to its most recent common ancestor within user-defined callout groups, supporting detailed and exploratory analysis.

## Features
- **Download Lineage Data:** Automatically fetch the latest lineage data from outbreak.info.
- **Customizable Callout Groups:** Define callout groups with custom HEX color codes.
- **Recombinant Handling:** Optionally include recombinant lineages with specified HEX colors.
- **Flexible Output:** Generate detailed or summarized output files in CSV or TSV formats.

## How It Works

1. **Check Direct Membership:**
   - If the lineage isn't a direct member of the callout groups:

2. **Look Up Parent Lineage:**
   - The function retrieves the lineage’s parent from the **lineage.yml** file, identifying this parent as the immediate ancestor in the lineage tree.

3. **Check for Recombinant Parents:**
   - It also examines "recombinant parents," which are additional possible lineage connections that occur when lineages recombine, diverging from a simple parent-child relationship.

## Handling Special Cases

4. **Parent is a Callout Group:**
   - If the lineage's parent is listed in the callout groups, the function returns this parent as the most relevant ancestor.

5. **Recombinant Lineages:**
   - If the lineage is associated with recombinant parents, indicating a complex ancestry, the function classifies it as "Other", or as "Recombinant" if the `-r` flag is set.

6. **Root Lineage Case:**
   - In cases where the lineage represents the base of the lineage tree (technically the last universal common ancestor, or LUCA, with no parent), the function also returns "Other.

## Recursive Analysis

7. **Recursive Call:**
   - If none of the above conditions apply (i.e., the lineage isn’t directly a callout group member, nor do its parent or recombinant connections provide a clear link), the function performs a recursive analysis. It calls itself with the parent lineage, repeating the checks and moving up the lineage tree until it either finds a connection to a callout group or exhausts the lineage links.
