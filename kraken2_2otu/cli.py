#  activating libraries and ete3 NCBITaxa
import click
import pandas as pd
import numpy as np
import os
from pandas import read_csv, DataFrame
from ete3 import NCBITaxa
click.secho('All libraries imported. NCBI taxdump downloaded successfully.', fg = 'green')


@click.command()
@click.option('--data_dir', default='./', help='Path to Kraken2 reports folder.')
@click.option('--outdir',default ='./', help='Folder to store resulting OTU table and Tax table.')

def do_it_all(data_dir, outdir):
    """Main funtcion to execute other functions"""
    click.secho(f'Received input argument: {data_dir}', fg = "green")
    click.secho(f'Received input argument: {outdir}', fg = "green")
    read_and_process_files(data_dir, outdir)

# some important variables
file_extension = '.report'
COUNT_COL_IDX = 2
SCIENTIFIC_NAME_COL_IDX = 5
TAXID_COL_IDX = 4
desired_ranks = ['root', 'domain', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
#  one-time download, later just updates silently
ncbi = NCBITaxa()
# ncbi.update_taxonomy_database()


def check_and_create_directory(directory):
    click.secho("Creating folder to store results", fg = "green")
    if not os.path.exists(directory):
        os.makedirs(directory)
        click.secho(f'Created directory to store results: {directory}', fg = "green")
    else:
        click.secho(f'Directory already exists: {directory}. Probably you already have results in it. Remove the folder before restarting the script!', fg = "red")

def create_OTU_table(df, path):
    '''Function to create OTU table from merged_df dataframe from previous function'''
    click.secho("Creating OTU table!", fg = "green")
    OTU_table = df[['Count', 'TaxID', 'Sample']].pivot_table(index='Sample', columns='TaxID', values='Count')
    click.secho("OTU table created!", fg = "green")
    OTU_table =  OTU_table.fillna(0)
    click.secho("Filling NaNs with 0s in OTU table", fg = "green")
    OTU_file_path = os.path.join(path,'OTU_table' + '.csv')
    OTU_table.to_csv(OTU_file_path, sep='\t', header = True, index = False)
    click.secho("OTU table saved!", fg = "green")

def fill_taxa_with_Nones_to_desired_length(my_list, target_length):
    '''Small supplementary function for creating NCBI taxonomy table'''
    while len(my_list) < target_length:
        my_list.append(None)
    return my_list
click.secho("Taxa lineage gaps filled with None!", fg = "green")
    
def create_Tax_table(df, path):
    '''Function to create NCBI taxonomy table with ete3 NCBITaxa using merged_df_taxid dataframe from previous function'''
    # creaing empty table to fill it
    click.secho("Creating Taxa table!", fg = "green")
    taxa_table = []
    for row in df.to_dict(orient='records')[0:10]:
        #  smth wrong with taxid = 2637697, skip for now, but in TODO list
        #  using ete3 here, first get lineage, then translate obtained taxids into looong row of taxa,
        #  then get only needed taxa and fill the tax_table
        taxid_lineage = ncbi.get_lineage(row['TaxID'])
        taxid_names = ncbi.get_taxid_translator(taxid_lineage)
        taxid_names = [taxid_names[taxid] for taxid in taxid_lineage]
        taxid_names_filled = fill_taxa_with_Nones_to_desired_length(taxid_names, len(desired_ranks))
        taxid_names_filled = [row['TaxID']] + taxid_names_filled
        taxa_table.append(taxid_names_filled)
    #  transform tax table into df and naking the columns right
    click.secho("Taxa table created!", fg = "green")
    taxa_table = pd.DataFrame(taxa_table)
    taxa_table.set_index(0, inplace=True)
    taxa_table.columns = desired_ranks
    Taxa_file_path = os.path.join(path, 'Taxa_table' + '.csv')
    taxa_table.to_csv(Taxa_file_path, sep='\t', header = True, index = False)
    click.secho("Taxa table saved!", fg = "green")

def read_and_process_files(data_dir, outdir):
    '''Read Kraken2 .report files from the folder where they stored, combining them into 2 dataframes.
    1st (merged_df) will be used for OTU table creation,
    2nd (merged_df_taxid) will be used for NCBI taxonomy table creation'''
    #  creating empty df to fill it during loop
    merged_df = pd.DataFrame()
    merged_df_taxid = pd.DataFrame()
    click.secho("Reading files!", fg = "green")
    #  iterate over the files in the folder
    for file_name in os.listdir(data_dir):
        if file_name.endswith(file_extension):
            file_path = os.path.join(data_dir, file_name)
            if os.path.getsize(file_path) > 0:
                try:
                    #  extract the desired columns from each file. 
                    #  for NCBI taxonomy table it is 5th col, for OTU table it is 3rd and 6th columns
                    click.secho(f"{file_name} read successfully!", fg = "green")
                    temp_df = pd.read_csv(file_path, delimiter='\t', skiprows=1, 
                                          usecols=[COUNT_COL_IDX, TAXID_COL_IDX, SCIENTIFIC_NAME_COL_IDX], header=None)
                    temp_df_taxid = pd.read_csv(file_path, delimiter='\t', skiprows=1, 
                                                usecols=[TAXID_COL_IDX], header=None)
                    #  extract the sample number from the file name
                    sample_number = os.path.splitext(file_name)[0]
                    #  add the sample number as a new column in the DataFrame
                    temp_df['Sample'] = sample_number
                    temp_df_taxid['Sample'] = sample_number
                    # concatenate the data into one DataFrame
                    merged_df = pd.concat([merged_df, temp_df])
                    merged_df_taxid = pd.concat([merged_df_taxid, temp_df_taxid])
                    #  renaming columns for the pre-OTU table (here in long format)
                    merged_df.columns = ["Count", "TaxID", "Taxon", "Sample"]
                    merged_df = merged_df.reset_index(drop=True)
                    #  removing leading spaces of taxonomic labels with regex
                    merged_df = merged_df.replace(r"^ +| +$", r"", regex=True)
                    #  the same renaming for Tax table
                    merged_df_taxid.columns =['TaxID', 'Sample']
                    merged_df_taxid = merged_df_taxid.reset_index(drop=True)
                except:
                    pass
    click.secho("Files read successfully!", fg = "green")
    check_and_create_directory(outdir)
    create_OTU_table(merged_df, outdir)
    create_Tax_table(merged_df_taxid, outdir)

if __name__ == '__main__':
    do_it_all()
