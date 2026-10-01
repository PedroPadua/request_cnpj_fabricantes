class CNPJNaoEncontrado(Exception):
    """CNPJ não existe na base da API (404)."""

class RateLimitError(Exception):
    """Limite de requisições por minuto da API atingido (429)."""