from flask import Flask, jsonify, request
from flask_cors import CORS
import numbers
import api_connect as cr # Apis de conexão
import fun as fnc # Funções para a utlização interna
from logging_config import setup_logging
import time
import logging

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

setup_logging(app)
logger = logging.getLogger(__name__)

@app.before_request
def _start_timer():
    request._start_time = time.time()

@app.after_request
def _log_response(response):
    elapsed_ms = int((time.time() - getattr(request, "_start_time", time.time())) * 1000)
    logger.info("response status=%s duration_ms=%s", response.status_code, elapsed_ms)
    return response

@app.route('/pessoa', methods=['POST'])
def pessoa():
    data = request.get_json(silent=True)  # retorna dict/list, ou None se não der pra ler [web:51]
    headers = dict(request.headers)  # útil para log/debug [web:131]
    auth = request.headers.get("Authorization")  # None se não vier [web:130]
    content_type = request.headers.get("Content-Type") # content type   
    logger.info("Inicio do processo")

    if(data is None): # Validação do json 
        return fnc.response_default(400,'json invalido')

    idSolicitacao = data.get("id")
    if(idSolicitacao is None or not isinstance(idSolicitacao, numbers.Number)): # Validação do ID (opção da API)
        return fnc.response_default(422,"Campo 'ID' Ausente ou não numerico")

    match idSolicitacao: # Lista de serviços e apis Listadas
        case 1: # Busca disponibilidade de sites no RegistroBR
            domain = data.get("domain")
            if(domain is None or not isinstance(domain, str)): # Valida se é campo texto
                return fnc.response_default(422,"Campo 'Domain' Ausente ou não é do tipo texto")
            logger.info(f"Iniciado a busca pelo Dominio no RegistroBR: {domain}")
            return fnc.response_default(200,cr.get_registrobr_avail(domain))
        
        case 2: # Busca de endereço baseado no cep
            cep = data.get("cep")
            if(cep is None or not isinstance(cep, str)): # Valida se é campo texto
                return fnc.response_default(422,"Campo 'CEP' Ausente ou não é do tipo texto")
            logger.info(f"Iniciado a busca por CEP: {cep}")
            return fnc.response_default(200,cr.get_cep_logradouro(cep))
        
        case 3:
            cnpj = data.get("cnpj")
            if(cnpj is None or not isinstance(cnpj, str)): # Valida se é campo texto
                return fnc.response_default(422,"Campo 'Cnpj' Ausente ou não é do tipo texto")
            logger.info(f"Iniciado a busca pelo cartão CNPJ: {cnpj}")
            return fnc.response_default(200,cr.get_cnpj(cnpj))
        case _:
            return fnc.response_default(200,"Nenhuma opção encontrada")
  
if __name__ == '__main__': # Iniciando o Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
