# API_Center
Esta central de APIs é um serviço em Flask que expõe um endpoint único (/webhook) para receber requisições POST em JSON, validar os dados de entrada e encaminhar a execução para diferentes “serviços” internos com base no campo id.
O projeto separa a camada HTTP (roteamento, validações e respostas) em main.py e a camada de integrações externas em api_connect.py, facilitando manutenção e reaproveitamento.

## Atualmente, a central oferece: 
  -> (1) consulta de disponibilidade de domínio no Registro.br;
  -> (2) consulta de endereço por CEP com fallback entre múltiplas fontes (ViaCEP, BrasilAPI e CepAberto), retornando um JSON normalizado com campos como cep, logradouro, bairro, cidade, uf, ddd e ibge

# Disponibilizado
Criador: Natalino
Data: 06/01/2026
Atualizado em: 06/01/2026
