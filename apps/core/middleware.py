"""Middlewares do projeto King Street."""


class NoCachePainelMiddleware:
    """Impede o navegador de servir páginas do painel a partir do cache.

    Sem isso o Chrome/Safari reaproveita a página anterior (inclusive no
    botão voltar e no app instalado como PWA) e o administrador vê dados
    velhos — estoque, pedidos e status já alterados. Cada clique numa
    funcionalidade do painel passa a fazer uma requisição nova ao servidor.
    """

    HEADERS = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/painel/"):
            for header, value in self.HEADERS.items():
                response[header] = value
        return response
