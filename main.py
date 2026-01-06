from flask import Flask, jsonify, request
from flask_cors import CORS
import numbers
import api_connect as cr


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)  # retorna dict/list, ou None se não der pra ler [web:51]
    headers = dict(request.headers)  # útil para log/debug [web:131]
    auth = request.headers.get("Authorization")  # None se não vier [web:130]
    content_type = request.headers.get("Content-Type") # content type   

    if(data is None): # Validação do json 
        data = {
            "code":400,
            "mensage":"Json invalido"
        }
        return jsonify(data), 400

    idSolicitacao = data.get("id")
    if(idSolicitacao is None or not isinstance(idSolicitacao, numbers.Number)): # Validação do ID (opção da API)
        data = {
            "code":422,
            "mensage":"Campo 'ID' Ausente ou não numerico"
        }
        return jsonify(data), 422

    match idSolicitacao: # Lista de serviços e apis Listadas
        case 1: # Busca disponibilidade de sites no RegistroBR
            domain = data.get("domain")
            if(domain is None or not isinstance(domain, str)): # Valida se é campo texto
                data = {
                    "code":422,
                    "mensage":"Campo 'Domain' Ausente ou não é do tipo texto"
                }
                return jsonify(data), 422
            
            ret = cr.get_registrobr_avail(domain)
            data = {
                "code":200,
                "mensage": ret
            }
            return jsonify(data), 200
        case 2:
            cep = data.get("cep")
            if(cep is None or not isinstance(cep, str)): # Valida se é campo texto
                data = {
                    "code":422,
                    "mensage":"Campo 'CEP' Ausente ou não é do tipo texto"
                }
                return jsonify(data), 422

            ret = cr.get_cep_logradouro(cep)
            data = {
                "code":200,
                "mensage":ret
            }
            return jsonify(data), 200
        case _:
            data = {
                "code":200,
                "mensage":"Nenhuma opção encontrada"
            }
            return jsonify(data), 200
  
if __name__ == '__main__': # Iniciando o Flask
    app.run(host='0.0.0.0', port=5000, debug=True)