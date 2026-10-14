import pandas as pd
import os, re
from datetime import datetime
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
        try:
            result = pd.read_excel('resultado.xlsx')
            timestamp = datetime.now().strftime('%d_%m_%H_%M')
            result.to_excel(f'resultado_anterior_{timestamp}.xlsx', index=False)
            df = pd.read_excel(path_folder)
            df = df.rename(columns={'Cód.':'cod', 'Razão Social':'raz_soc', 'CNPJ':'cnpj', 'Município':'municipio'})
            df_somente = df.merge(result, on='cnpj', how='left', indicator=True)
            df_somente = df_somente[df_somente['_merge'] == 'left_only'].drop(columns='_merge')
            df_somente['cnpj'] = df_somente['cnpj'].apply(self._sanatize_cnpj)
            return df_somente
        except:
            print('Não foi encontrada planilha de resultados')
            df = pd.read_excel(path_folder)
            df = df.rename(columns={'Cód.':'cod', 'Razão Social':'raz_soc', 'CNPJ':'cnpj', 'Município':'municipio'})
            df['cnpj'] = df['cnpj'].apply(self._sanatize_cnpj)

        return df