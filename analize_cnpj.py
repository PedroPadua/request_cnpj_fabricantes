import requests


class Fabricantes:

    def __init__(self):
        
        
    def request_cnpj(cnpj): 
        body_request = "https://publica.cnpj.ws/cnpj" / cnpj
        resp = requests.request("GET", body_request)
        data = resp.json()
        list_ati = []
        estabelecimento = data.get('estabelecimento')
        return  data.get('atividade_principal')
    