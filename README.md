# kraken2_2otu
This script allows creating OTU and NCBI taxa lineage tables from Kraken2 reports stored in 1 folder. Simple but effective.

## Prerequisites
Use setup.py to install all dependencies automatically (you may also need ```pip``` and ```click```).  
In case something goes wrong, you need to install:
1) pandas;
2) numpy;
3) ete3.

## Usage
```kraken2_2otu --folder_path {path_to_folder_w_kraken2_reports} --outdir {path_to_results_folder} ```

## How it works
Using Kraken2 report file which stores info about read count and taxid (columns 3 and 5 respectively) of each taxon it could found, we can transform it to OTU table suitable for later usage with ```phyloseq``` R package for downstream analysis.  

Output structure for OTU table has sample IDs stored in row names, taxons stores in column names and read counts are in cells and look like this (part of one of example tables is shown):  
| root    	| cellular organisms 	| Eukaryota 	| Sar      	| Apicomplexa 	| Aconoidasida 	| Plasmodium 	| Plasmodium relictum 	|
|---------	|--------------------	|-----------	|----------	|-------------	|--------------	|------------	|---------------------	|
| sample1 	| 15118.0            	| 2665209.0 	| 34758.0  	| 41584.0     	| 3447.0       	| 2085.0     	| 10036.0             	|
| sample2 	| 5035.0             	| 8991124.0 	| 129212.0 	| 5891.0      	| 6963.0       	| 2101.0     	| 4077.0              	|
| sample3 	| 2469.0             	| 637427.0  	| 113551.0 	| 14671.0     	| 21400.0      	| 2637.0     	| 21980.0             	|

Taxa table represents each taxid found in all samples with its desired taxonomic lineage. Each taxid is stored in row names, desired taxonomic ranks placed in column names, and taxonomic linegae is in cells. Note that if any rank is missing it the desired lineage, it will be shown as None:  

|       	| root 	| domain             	| kingdom  	| phylum         	| class               	| order            	| family             	| genus       	| species          	| strain                   	|
|-------	|------	|--------------------	|----------	|----------------	|---------------------	|------------------	|--------------------	|-------------	|------------------	|--------------------------	|
| 1224  	| root 	| cellular organisms 	| Bacteria 	| Pseudomonadota 	| None                	| None             	| None               	| None        	| None             	| None                     	|
| 91347 	| root 	| cellular organisms 	| Bacteria 	| Pseudomonadota 	| Gammaproteobacteria 	| Enterobacterales 	| None               	| None        	| None             	| None                     	|
| 83334 	| root 	| cellular organisms 	| Bacteria 	| Pseudomonadota 	| Gammaproteobacteria 	| Enterobacterales 	| Enterobacteriaceae 	| Escherichia 	| Escherichia coli 	| Escherichia coli O157:H7 	|

## Authors
I.Sonets, D.Fedorov
