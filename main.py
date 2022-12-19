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
    df = df.dropna(subset=["Mínimo"])
    return df
    

def dif_notas():
    df_concat = concat_dataframes()
    df_concat = df_concat[df_concat["Modalidade"] == "4.2"]
    df_concat = df_concat[["Nome", "Turno", "Mínimo", "Ano"]]
    
    nomes = pd.unique(df_concat["Nome"])
    df_notas = pd.DataFrame()
    for nome in nomes:
        df = df_concat[df_concat["Nome"] == nome].copy()
        turnos = pd.unique(df["Turno"])
        if len(turnos) > 1:
            for turno in turnos:
                df_ = df[df["Turno"] == turno]
                
                linha = {"Nome":nome,
                         "Turno":turno,
                        }
                        
                for ano in df_["Ano"].to_list():
                    linha[ano] = float(df_[df_["Ano"] == ano]["Mínimo"])

                df_notas = pd.concat([df_notas, pd.DataFrame(linha, index=[0])])  
        else:
            linha = {"Nome":nome,
                     "Turno":df["Turno"].iloc[0],
                    }
                    
            for ano in df["Ano"].to_list():
                linha[ano] = float(df[df["Ano"] == ano]["Mínimo"])
            
            df_notas = pd.concat([df_notas, pd.DataFrame(linha, index=[0])])    
                    
    df_notas = df_notas.reset_index(drop=True)                    
    df_notas.to_csv("notas.csv")

    
    
def main():
    # df = concat_dataframes()
    # df = df[df["Modalidade"] == "4.2"]
    # df = df[df["Ano"] == "2018"]
    # df = df[df["Mínimo"] <= 700]
    # df = df.sort_values("Mínimo", ascending=False)
    # df = df.reset_index(drop=True)
    
    dif_notas()
    
    
if __name__ == "__main__":
    main()