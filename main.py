import pandas as pd
from requests.exceptions import RequestException
from pipes.PipeFabricantes import PipeFabricantes
from data.prepdf import PrepDF
from utils.exceptions import RateLimitError


def main():
    prep = PrepDF()
    df = prep.load_df()
    pipe = PipeFabricantes()
    resultados = []

    for cnpj in df["cnpj"].dropna():
        parar_lote = False
        try:
            resultado = pipe.run(cnpj)
        except RateLimitError as erro:
            resultado = {
                "cnpj": str(cnpj),
                "status": "erro",
                "erro": str(erro),
            }
            print(f"Lote interrompido: {erro}")
            parar_lote = True
        except RequestException as erro:
            resposta = erro.response
            resultado = {
                "cnpj": str(cnpj),
                "status": "erro_request",
                "http_status": resposta.status_code if resposta is not None else None,
                "erro": f"{type(erro).__name__}: {erro}",
            }
            print(resultado)

        resultados.append(resultado)
        pd.DataFrame(resultados).to_excel("resultado.xlsx", index=False)

        if parar_lote:
            break

if __name__ == "__main__":
    main()