import requests
from requests.exceptions import Timeout
from collections import deque
from utils.exceptions import *
from config import *
import time

class RequestClient:
    def __init__(self):
        self.search = ['Fabricação','Confecção','Produção','Preparação','Beneficiamento','Processamento','Torrefação','Moagem','Refino','Fundição','Forjamento','Usinagem','Montagem','Impressão','Reciclagem','Transformação','Elaboração','Manipulação']
        self.url = api_url
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.slots = deque()



    def  _wait_for_slot(self):
        now = time.monotonic()

        while self.slots and now - self.slots[0] >= self.window_seconds:
            self.slots.popleft()

        if len(self.slots) >= self.max_requests:
            sleep_time = self.window_seconds - (now - self.slots[0]) + 2
            print(f'Aguardando {round(sleep_time, 2)} segundos antes de realizar o request.')
            time.sleep(max(sleep_time,0))
        
        self.slots.append(time.monotonic())



    def request_cnpj(self,cnpj : str)->dict: 
        body_request = f'{self.url}{cnpj}'
        while True:
            self._wait_for_slot()
            print(f'Iniciando o request do cnpj -> {cnpj}')
            try:
                resp = requests.get(body_request, timeout=60)
            except Timeout:
                print(f'Timeout ao consultar {cnpj}; tentando novamente.')
                continue

            if resp.status_code == 429:
                wait_seconds = self.window_seconds + 2
                print(f'Limite da cnpj.ws atingido; aguardando {wait_seconds} segundos para repetir {cnpj}.')
                time.sleep(wait_seconds)
                continue

            break

        if resp.status_code == 404:
            raise CNPJNaoEncontrado(f'CNPJ não encontrado {cnpj}')

        resp.raise_for_status()
        estabelecimento = resp.json().get("estabelecimento")
        if estabelecimento is None:
            raise CNPJNaoEncontrado(f'Resposta sem estabelecimento: {cnpj}')
        return estabelecimento



    def list_ati(self, resp):
        list_ati = []
        list_ati.append({'ati_prin': resp['atividade_principal']['descricao']})
        list_sec = resp.get('atividades_secundarias',[])
        if list_sec is None or len(list_sec) == 0:
            list_ati.append({'ati_sec_1' : None})
        else:   
            for i, ati_sec in enumerate(list_sec, start=1):
            
                descri_sec = ati_sec['descricao']
                list_ati.append({f'ati_sec_{i}': descri_sec})

        return list_ati

