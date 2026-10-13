from services.request_clients import RequestClient
from services.conference import ConferenceCNPJ
from utils.exceptions import CNPJNaoEncontrado
class PipeFabricantes:

    def __init__(self):
        self.request = RequestClient()
        self.conf = ConferenceCNPJ() 

    def run(self, cnpj:str):    
        try:
            resp = self.request.request_cnpj(cnpj)
            list_ati = self.request.list_ati(resp)
            result = self.conf.compare(list_ati)

            dic_retur =  {
                'cnpj' : str(cnpj),
                **result,
                'erro' : None
            }
            print(dic_retur)
            return dic_retur
        except CNPJNaoEncontrado as erro:

            dic_retur = {                 
                'cnpj' : str(cnpj),
                'status':'erro',
                'erro' : str(erro)
            }

            print(dic_retur)
            return dic_retur



if __name__ == '__main__':
    pf = PipeFabricantes()
    result = pf.run('43960247000162')
    print(result)
