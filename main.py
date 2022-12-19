import pandas as pd
import os

folder = os.path.dirname(__file__)

def get_archives():
    global folder
    files = [f"{folder}\\data\\{archive}" for archive in os.listdir(f"{folder}\\data") if archive.endswith(".csv")]
    return files
    
def concat_dataframes():
    files = get_archives()
    df = pd.DataFrame()
    for file in files:
        file_name = file[-8:-4]
        df_ = pd.read_csv(file)
        df_["Ano"] = file_name
        
        #Convert data type of series
        df_["Mínimo"] = df_["Mínimo"].apply(lambda x: str(x))
        df_["Mínimo"] = df_["Mínimo"].apply(lambda x: x.replace(",", "."))
        df_["Mínimo"] = df_["Mínimo"].astype(float)
        
        #Convert data type of series
        df_["Máximo"] = df_["Máximo"].apply(lambda x: str(x))
        df_["Máximo"] = df_["Máximo"].apply(lambda x: x.replace(",", "."))
        df_["Máximo"] = df_["Máximo"].astype(float)
        
        df = pd.concat([df, df_])
    df = df[["Nome", "Turno", "Modalidade", "Mínimo", "Máximo", "Ano"]]
    return df
    
def main():
    df = concat_dataframes()
    df = df[df["Modalidade"] == "4.2"]
    df = df[df["Ano"] == "2022"]
    df = df[df["Mínimo"] <= 700]
    df = df.sort_values("Mínimo", ascending=False)
    print(df)
    
if __name__ == "__main__":
    main()