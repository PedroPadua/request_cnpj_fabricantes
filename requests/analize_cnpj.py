import requests
from utils.exceptions import *

class Fabricantes:
    def __init__(self):
        self.search = ['Fabricação','Confecção','Produção','Preparação','Beneficiamento','Processamento','Torrefação','Moagem','Refino','Fundição','Forjamento','Usinagem','Montagem','Impressão','Reciclagem','Transformação','Elaboração','Manipulação']

        
    def request_cnpj(self,cnpj : str)->dict: 
        body_request = f'https://publica.cnpj.ws/cnpj/{cnpj}'
        resp = requests.request("GET", body_request)

        if resp.status_code == 404:
            raise CNPJNaoEncontrado(f'CNPJ não encontrado {cnpj}')

        if resp.status_code == 429:
            raise RateLimitError(f'Limite da cnpj.ws atingido')

        resp.raise_for_status()
        return resp.json().get("estabelecimento")


    def analize_ati_prin(self,data)-> list:
        ati_prin = data['atividade_principal']['descricao']

        for term in self.search:
            if term in ati_prin:
                return {
                    'status_prin': True,
                    'term_prin' : ati_prin
                }
            
        return {
            'status_prin' : False,
            'term_prin': None
        }


    def analize_ati_sec(self, data) ->dict:
        list_sec = data.get('atividades_secundarias',[])
        results = []
        if list_sec is None or len(list_sec) == 0:
            return [{
                    'status_sec_1' : False,
                    'term_sec_1': None
            }]
        for ati_sec in list_sec:

            descri_sec = ati_sec['descricao']

            for term in self.search:
                i = len(results) +1
                if term in descri_sec:
                    
                    dic_aux = {
                    f'status_sec_{i}' : True,
                    f'term_sec_{i}': descri_sec
                    }
                    results.append(dic_aux)
                    break

        return results