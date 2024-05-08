@click.command()
@click.option('--folder_path', default='./', help='Path to Kraken2 reports folder.')
@click.option('--outdir',default ='./', help='Folder to store resulting OTU table and Tax table.')

def do_it_all(folder_path, outdir):
    """Main funtcion to execute other functions"""
    click.echo(f'Received input argument: {folder_path}')
    click.echo(f'Received input argument: {outdir}')
    return read_files(), create_OTU_table(), create_Tax_table()
        
if __name__ == '__main__':
    do_it_all()

#  activating libraries and ete3 NCBITaxa
import pandas as pd
import numpy as np
import os
from pandas import read_csv, DataFrame
from ete3 import NCBITaxa
import click

# some important variables
file_extension = '.report'
COUNT_COL_IDX = 2
SCIENTIFIC_NAME_COL_IDX = 5
TAXID_COL_IDX = 4
desired_ranks = ['root', 'domain', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
#  one-time download, later just updates silently
ncbi = NCBITaxa()
ncbi.update_taxonomy_database()

def read_files(folder_path):
    '''Read Kraken2 .report files from the folder where they stored, combining them into 2 dataframes.
    1st (merged_df) will be used for OTU table creation,
    2nd (merged_df_taxid) will be used for NCBI taxonomy table creation'''
    #  creating empty df to fill it during loop
    merged_df = pd.DataFrame()
    merged_df_taxid = pd.DataFrame()
    #  iterate over the files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(file_extension):
            file_path = os.path.join(folder_path, file_name)
            if os.path.getsize(file_path) > 0:
                try:
                    #  extract the desired columns from each file. 
                    #  for NCBI taxonomy table it is 5th col, for OTU table it is 3rd and 6th columns
                    temp_df = pd.read_csv(file_path, delimiter='\t', skiprows=1, 
                                          usecols=[COUNT_COL_IDX, SCIENTIFIC_NAME_COL_IDX, TAXID_COL_IDX], header=None)
                    temp_df_taxid = pd.read_csv(file_path, delimiter='\t', skiprows=1, 
                                                usecols=[TAXID_COL_IDX], header=None)
                    #  extract the sample number from the file name
                    sample_number = os.path.splitext(file_name)[0]
                    #  add the sample number as a new column in the DataFrame
                    temp_df['sample_number'] = sample_number
                    temp_df_taxid['sample_number'] = sample_number
                    # concatenate the data into one DataFrame
                    merged_df = pd.concat([merged_df, temp_df])
                    merged_df_taxid = pd.concat([merged_df_taxid, temp_df_taxid])
                    #  renaming columns for the pre-OTU table (here in long format)
                    merged_df.columns = ["Count", "Taxid", "Taxon", "Sample"]
                    merged_df = merged_df.reset_index(drop=True)
                    #  removing leading spaces of taxonomic labels with regex
                    merged_df = merged_df.replace(r"^ +| +$", r"", regex=True)
                    #  the same renaming for Tax table
                    merged_df_taxid.columns =['TaxID', 'Sample']
                    merged_df_taxid = merged_df_taxid.reset_index(drop=True)
                except:
                    pass
    return merged_df, merged_df_taxid

def create_OTU_table(merged_df, outdir):
    '''Function to create OTU table from merged_df dataframe from previous function'''
    OTU_table = merged_df[['Count', 'Taxid', 'Sample']].pivot(index='Sample', columns='Taxid', values='Count')
    OTU_file_path = os.path.join(outdir + 'OTU_table' + 'csv')
    OTU_table.to_csv(OTU_file_path, sep='\t', header = True, index = False)

def fill_taxa_with_Nones_to_desired_length(my_list, target_length):
    '''Small supplementary function for creating NCBI taxonomy table'''
    while len(my_list) < target_length:
        my_list.append(None)
    return my_list
    
def create_Tax_table(merged_df_taxid, outdir):
    '''Function to create NCBI taxonomy table with ete3 NCBITaxa using merged_df_taxid dataframe from previous function'''
    # creaing empty table to fill it
    taxa_table = []
    for row in merged_df_taxid.to_dict(orient='records')[0:10]:
        #  smth wrong with taxid = 2637697, skip for now, but in TODO list
        #  using ete3 here, first get lineage, then translate obtained taxids into looong row of taxa,
        #  then get only needed taxa and fill the tax_table
        taxid_lineage = ncbi.get_lineage(row['Taxid'])
        taxid_names = ncbi.get_taxid_translator(taxid_lineage)
        taxid_names = [taxid_names[taxid] for taxid in taxid_lineage]
        taxid_names_filled = fill_taxa_with_Nones_to_desired_length(taxid_names, len(desired_ranks))
        taxid_names_filled = [row['Taxid']] + taxid_names_filled
        taxa_table.append(taxid_names_filled)
    #  transform tax table into df and naking the columns right
    taxa_table = pd.DataFrame(taxa_table)
    taxa_table.set_index(0, inplace=True)
    taxa_table.columns = desired_ranks
    Taxa_file_path = os.path.join(outdir + 'Taxa_table' + 'csv')
    taxa_table.to_csv(Taxa_file_path, sep='\t', header = True, index = False)