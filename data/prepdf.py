import pandas as pd
import os, re
from dotenv import load_dotenv
load_dotenv()

class PrepDF:

    def _sanatize_cnpj(cnpj):
        return re.sub(r'/D','', str(cnpj)).zfill(14)

    def load_df(self):
        df = pd.read_excel(os.getenv('relat_path'))
        df = df.rename(columns={'Cód.':'cod', 'Razão Social':'raz_soc', 'CNPJ':'cnpj', 'Município':'municipio'})
        df['cnpj'] = df['cnpj'].apply(self._sanatize_cnpj)

        return df