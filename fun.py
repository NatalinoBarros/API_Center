import numbers
import re
from flask import jsonify
import logging

def response_default(code: int, msn) -> dict:
   # if code is None:
    data = {
                "code":code,
                "mensage": msn
            }
    
    return jsonify(data), code

def normalizar_cep(data: dict) -> dict:
    """
    Normaliza respostas de diferentes APIs de CEP para um formato único.
    Funciona com ViaCEP, BrasilAPI e CepAberto.
    """
    
    cep = data.get("cep", "").replace("-", "") # Extrai CEP (remove hífen se tiver)
    logradouro = data.get("logradouro", "") # Logradouro (mesmo nome em todas)
    bairro = data.get("bairro", "") # Bairro (mesmo nome em todas)
    
    if "cidade" in data and isinstance(data["cidade"], dict): # Cidade/Localidade (nomes diferentes)
        cidade = data["cidade"].get("nome", "") # CepAberto: {"cidade": {"nome": "Santo André"}}
    else:
        cidade = data.get("localidade", "") or data.get("city", "")  # ViaCEP/BrasilAPI: {"localidade": "Santo André"}
    
    if "estado" in data and isinstance(data["estado"], dict): # Estado/UF (nomes diferentes)
        uf = data["estado"].get("sigla", "")  # CepAberto: {"estado": {"sigla": "SP"}}
    else:
        uf = data.get("uf", "") or data.get("state", "") # ViaCEP/BrasilAPI: {"uf": "SP"} ou {"state": "SP"}
    
    complemento = data.get("complemento", "") # Complemento
    
    ddd = None # DDD
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

def formata_cnpj(cnpj: str) -> str | None:
    cnpj_limpo = re.sub(r"[^0-9]", "", str(cnpj)) 
    return cnpj_limpo if len(cnpj_limpo) == 14 else None
