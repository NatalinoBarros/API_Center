import re
import requests
import fun as fnc
import logging

logger = logging.getLogger(__name__)

def get_registrobr_avail(domain: str, timeout: int = 10): # Api que busca dados do dominio no registroBR
    _ALLOWED_RE = re.compile(r"^[A-Za-z0-9àáâãéêíóôõúüç.-]+$")
    if not isinstance(domain, str) or not domain.strip():
        return "O domínio não foi informado corretamente!"

    domain = domain.strip().lower()

    if not _ALLOWED_RE.match(domain):
        return "O domínio não foi informado corretamente!"

    domain_idna = domain.encode("idna").decode("ascii")

    url = f"https://registro.br/v2/ajax/avail/raw/{domain_idna}"

    logger.info("Domain lookup Ok source=%s", url)
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def get_cep_logradouro(cep: str, timeout: int = 10): # API que busca endereço com base em no CEP
    '''
    Buscando informações de CEP, utilizando 3 fontes de dados e normalizando as respostas
    parametro cep: Consulta de endereço por cep, onde o cep deve conter 8 caracteres e sem pontuação
    tipo cep: str
    parametro timeout: tempo de espera da API
    tipo timeout: int
    '''

    if not isinstance(cep, str) or not cep.strip():
        return "CEP incorreto"
    
    cep = cep.replace("-","")

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

            # log
            logger.info("Cep lookup ok source=%s", url[0] if isinstance(url, list) else url)

            return(fnc.normalizar_cep(response))
        except requests.exceptions.RequestException as e:
            last_error = str(e)   # Timeout, conexão, HTTPError etc. [web:319]
            continue

    if(response is None):
        return {"code": 502, "message": "Nenhuma fonte respondeu", "detail": last_error}
    
    return {"code": 502, "message": "Nenhuma fonte respondeu", "detail": last_error}

def get_cnpj(cnpj: str, timeout: int = 10): # Api que busca dados QSA da receita, busca é feita pelo cnpj
    '''
    Busca dados do cartão cnpj, trazendo dados como socios (QSA), endereço, razão social.
    parametro cnpj: Cnpj a ser consultado
    tipo cnpj: str
    parametro timeout: tempo de espera da API
    tipo timeout: int
    '''

    if not isinstance(cnpj, str) or len(fnc.formata_cnpj(cnpj)) != 14 :
        return "CNPJ invalido"
        
    url = f'https://api.opencnpj.org/{fnc.formata_cnpj(cnpj)}'
    logger.info("CNPJ lookup Ok source=%s", url)
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()
    
