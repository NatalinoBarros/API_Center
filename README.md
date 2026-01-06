# API Center #
Esta central de APIs é um serviço em Flask que expõe um endpoint único (/webhook) para receber requisições POST em JSON, validar os dados de entrada e encaminhar a execução para diferentes “serviços” internos com base no campo id.<br><br>
O projeto separa a camada HTTP (roteamento, validações e respostas) em main.py e a camada de integrações externas em api_connect.py, facilitando manutenção e reaproveitamento.<br>

## Atualmente, a central oferece: 
  1° Consulta de disponibilidade de domínio no Registro.br.<br>
  2° Consulta de endereço por CEP com fallback entre múltiplas fontes (ViaCEP, BrasilAPI e CepAberto), retornando um JSON normalizado com campos como cep, logradouro, bairro, cidade, uf, ddd e ibge.<br>

## Disponibilizado
Criador: Natalino<br>
Data: 06/01/2026<br>
Atualizado em: 06/01/2026<br>
