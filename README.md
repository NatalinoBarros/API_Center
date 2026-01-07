# API Center #
Este repositório implementa uma central de APIs em Flask, expondo um endpoint POST (/pessoa) que recebe JSON, valida os campos e roteia a requisição por meio de um idSolicitacao para diferentes serviços (ex.: consulta de domínio, CEP e CNPJ).<br><br>

A arquitetura foi organizada em três módulos: main.py (camada HTTP/rotas, validações, respostas e logs por requisição), api_connect.py (conectores para APIs externas, com logs de chamadas) e fun.py (funções utilitárias como resposta padrão response_default, normalização de CEP e formatação/validação de CNPJ).<br><br>
​
O projeto também inclui configuração centralizada de logging em logging_config.py, com saída em console e arquivo, incluindo data no nome do arquivo e enriquecimento automático do log com informações do request (método, path e IP) quando disponível.<br><br>

## Atualmente, a central oferece: 
  1° Consulta de disponibilidade de domínio no Registro.br.<br><br>
  2° Consulta de endereço por CEP com fallback entre múltiplas fontes (ViaCEP, BrasilAPI e CepAberto), retornando um JSON normalizado com campos como cep, logradouro, bairro, cidade, uf, ddd e ibge.<br><br>
  3° Consulta de dados de CNPJ via OpenCNPJ, com formatação/validação do CNPJ antes da chamada externa. <br><br>

## Observabilidade (logging)
Logs com contexto de requisição (método, path, IP) e registro de tempo de processamento e status code por request (via before_request/after_request).<br><br>​
Logs de integração nas consultas externas (ex.: sucesso da consulta e origem/URL).<br><br>
​

## Disponibilizado
Criador: Natalino Barros<br>
Data: 06/01/2026<br>
Atualizado em: 06/01/2026<br>
