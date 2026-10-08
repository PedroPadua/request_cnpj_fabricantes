from config import target_words


class ConferenceCNPJ:

    def __init__(self):
        self.target_words = target_words


    def compare(self, atividades : list[dict]):
        ati_totais = [
            description
            for activity in atividades
            for description in activity.values()
            if isinstance(description, str)
        ]

        is_manufacturer = any(
            word.casefold() in atividade.casefold()
            for word in self.target_words
            for atividade in ati_totais
        )

        return {
            'status': 'fabricante' if is_manufacturer else 'não_fabricante'
        }