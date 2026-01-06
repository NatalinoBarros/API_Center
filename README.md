# API Center #
Este repositório implementa uma central de APIs em Flask, expondo um endpoint POST (/pessoa) que recebe JSON, valida os campos e roteia a requisição por meio de um id para diferentes serviços (ex.: consulta de domínio, CEP e CNPJ).<br><br>
A arquitetura foi organizada em três módulos: main.py (camada HTTP/rotas, validações e respostas), api_connect.py (conectores para APIs externas) e fun.py (funções utilitárias como resposta padrão response_default, normalização de CEP e formatação/validação de CNPJ).<br><br>
​O projeto separa a camada HTTP (roteamento, validações e respostas) da camada de integrações externas, facilitando manutenção, testes e reaproveitamento das funções de consulta.<br><br>


## Atualmente, a central oferece: 
  1° Consulta de disponibilidade de domínio no Registro.br.<br><br>
  2° Consulta de endereço por CEP com fallback entre múltiplas fontes (ViaCEP, BrasilAPI e CepAberto), retornando um JSON normalizado com campos como cep, logradouro, bairro, cidade, uf, ddd e ibge.<br><br>
  3° Consulta de dados de CNPJ via OpenCNPJ, com formatação/validação do CNPJ antes da chamada externa. <br><br>


## Disponibilizado
Criador: Natalino<br>
Data: 06/01/2026<br>
Atualizado em: 06/01/2026<br>
