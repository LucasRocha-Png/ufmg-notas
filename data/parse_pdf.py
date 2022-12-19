"""
This file parses the PDF files
"""

import tabula
import pandas as pd
import os

folder = os.path.dirname(__file__)

def get_archives():
    global folder
    files = [f"{folder}\\pdf\\{archive}" for archive in os.listdir(f"{folder}\\pdf") if archive.endswith(".pdf")]
    return files

def parse_pdf(file):
    
    try:
        #Read file
        df = tabula.read_pdf(file, pages="all")
        
        #Remove last page
        df = df[:len(df)-1]
        
        #Concat all pages and delete Null Values
        df = pd.concat(df).dropna(axis=1, how="all")
        # df = df.dropna(axis=0)
        
        columns = df.columns.to_list()
        columns = columns[:5]
        df = df[columns]
        
        #rename columns
        df.columns = ['Nome','Turno', 'Modalidade', 'Mínimo', 'Máximo']
            
        #Reset index    
        df = df.reset_index(drop=True)
        
        return df
        
    except:
        print(df)
        input(f"{file}")
    
    
    
def main():
    files = get_archives()
    for file in files:
        file_name = file[-8:-4]
        df = parse_pdf(file)
        df.to_csv(f"{file_name}.csv")
    
    
if __name__ == "__main__":
    main()

