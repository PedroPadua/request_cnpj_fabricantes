import pandas as pd
from pipes.PipeFabricantes import PipeFabricantes
from data.prepdf import PrepDF
from utils.exceptions import RateLimitError


def main():
    prep = PrepDF()
    df = prep.load_df()
    pipe = PipeFabricantes()
    resultados = []

    for cnpj in df["cnpj"].dropna():
        try:
            resultado = pipe.run(cnpj)
        except RateLimitError as erro:
            resultados.append({
                "cnpj": str(cnpj),
                "status": "erro",
                "erro": str(erro),
            })
            print(f"Lote interrompido: {erro}")
            break

        resultados.append(resultado)

        pd.DataFrame(resultados).to_excel("resultado.xlsx", index=False)

if __name__ == "__main__":
    main()