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


    def analize_ati_prin(self,data)-> dict:
        ati_prin = data['atividade_principal']['descricao']

        for term in self.search:
            if term in ati_prin:
                return {
                    'status': True,
                    'term' : term
                }
            
        return {
            'status' : False,
            'term': None
        }


    def analize_ati_sec(self, data) ->dict:
        list_sec = data.get('atividades_secundarias',[])
        if len(list_sec) == 0:
            return {
                    'status' : False,
                    'term': None
            }
        for ati_sec in list_sec:

            descri_sec = ati_sec['descricao']

            for term in self.search:
                if term in descri_sec:
                    return {
                    'status' : True,
                    'term': term
                    }
                
        return {
            'status' : False,
            'term': None
        }