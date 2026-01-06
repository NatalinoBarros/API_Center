import re
import requests

def normalizar_cep(data: dict) -> dict:
    """
    Normaliza respostas de diferentes APIs de CEP para um formato único.
    Funciona com ViaCEP, BrasilAPI e CepAberto.
    """
    # Extrai CEP (remove hífen se tiver)
    cep = data.get("cep", "").replace("-", "")
    
    # Logradouro (mesmo nome em todas)
    logradouro = data.get("logradouro", "")
    
    # Bairro (mesmo nome em todas)
    bairro = data.get("bairro", "")
    
    # Cidade/Localidade (nomes diferentes)
    if "cidade" in data and isinstance(data["cidade"], dict):
        # CepAberto: {"cidade": {"nome": "Santo André"}}
        cidade = data["cidade"].get("nome", "")
    else:
        # ViaCEP/BrasilAPI: {"localidade": "Santo André"}
        cidade = data.get("localidade", "") or data.get("city", "")
    
    # Estado/UF (nomes diferentes)
    if "estado" in data and isinstance(data["estado"], dict):
        # CepAberto: {"estado": {"sigla": "SP"}}
        uf = data["estado"].get("sigla", "")
    else:
        # ViaCEP/BrasilAPI: {"uf": "SP"} ou {"state": "SP"}
        uf = data.get("uf", "") or data.get("state", "")
    
    # Complemento
    complemento = data.get("complemento", "")
    
    # DDD
    ddd = None
    if "cidade" in data and isinstance(data["cidade"], dict):
        ddd = data["cidade"].get("ddd")  # CepAberto
    else:
        ddd = data.get("ddd")  # ViaCEP
    
    # IBGE
    ibge = None
    if "cidade" in data and isinstance(data["cidade"], dict):
        ibge = data["cidade"].get("ibge")  # CepAberto
    else:
        ibge = data.get("ibge")  # ViaCEP
    
    return {
        "cep": cep,
        "logradouro": logradouro,
        "complemento": complemento,
        "bairro": bairro,
        "cidade": cidade,
        "uf": uf,
        "ddd": ddd,
        "ibge": ibge
    }


def get_registrobr_avail(domain: str, timeout: int = 10): # Api que busca dados do dominio no registroBR
    _ALLOWED_RE = re.compile(r"^[A-Za-z0-9àáâãéêíóôõúüç.-]+$")
    if not isinstance(domain, str) or not domain.strip():
        return "O domínio não foi informado corretamente!"

    domain = domain.strip().lower()

    if not _ALLOWED_RE.match(domain):
        return "O domínio não foi informado corretamente!"

    domain_idna = domain.encode("idna").decode("ascii")

    url = f"https://registro.br/v2/ajax/avail/raw/{domain_idna}"
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def get_cep_logradouro(cep: str, timeout: int = 10): # API que busca endereço com base em no CEP
    '''
    Buscando informações de CEP, utilizando 3 fontes de dados e normalizando as respostas
    param cep: Description
    type cep: str
    param timeout: Description
    type timeout: int
    '''
    if not isinstance(cep, str) or not cep.strip():
        return "CEP incorreto"
    
    if((not re.fullmatch(r"\d{8}|\d{5}-\d{3}", cep))):
         return "CEP incorreto"
        
    cep = cep.strip().lower()
    fontes = [
        [f"https://www.cepaberto.com/api/v3/cep?cep={cep}","5d1f037f20991606bdc691371b4ae2f4"],
        f"https://viacep.com.br/ws/{cep}/json/",
        f"https://brasilapi.com.br/api/cep/v1/{cep}"
        
    ]
    for url in fontes:
        try:
            if(isinstance(url,list)):
                headers = {"Authorization": f"Token token={url[1]}"}
                resp = requests.get(url[0], headers=headers ,timeout=timeout)
            else:
                resp = requests.get(url, timeout=timeout)

            resp.raise_for_status()
            response = resp.json()
            return(normalizar_cep(response))
        except requests.exceptions.RequestException as e:
            last_error = str(e)   # timeout, conexão, HTTPError etc. [web:319]
            continue

    if(response is None):
        return {"code": 502, "message": "Nenhuma fonte respondeu", "detail": last_error}
    
    return {"code": 502, "message": "Nenhuma fonte respondeu", "detail": last_error}

