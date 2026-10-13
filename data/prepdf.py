import pandas as pd
import os, re
from dotenv import load_dotenv
from config import path_folder
load_dotenv()

class PrepDF:

    @staticmethod
    def _sanatize_cnpj(cnpj):
        if pd.isna(cnpj):
            return None
        if isinstance(cnpj, float) and cnpj.is_integer():
            cnpj = int(cnpj)
        return re.sub(r'\D', '', str(cnpj)).zfill(14)

    def load_df(self):
        df = pd.read_excel(path_folder)
        df = df.rename(columns={'Cód.':'cod', 'Razão Social':'raz_soc', 'CNPJ':'cnpj', 'Município':'municipio'})
        df['cnpj'] = df['cnpj'].apply(self._sanatize_cnpj)

        return df