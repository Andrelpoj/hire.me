# URL Shortener API Client

Para testar o client é necessário:
1. Instalar as dependências em ``` url_shortener_client/requirements.txt ```
2. Importar o módulo url_shortener_client
3. Utilizar as classes e métodos importados
4. Garantir que os serviços (url-shortener e db) estão ativos, para iniciar os containers basta executar ```docker-compose up``` na pasta raíz do projeto. 


## URLShortenerClient

### retrieve_url(alias)
Recebe um **alias** (e.g. bemobi) e retorna a **url original** (string) associada. 

- Caso o alias passado como parâmetro não esteja registrado no banco a exceção **AliasNotFound(alias)** é levantada.
- Caso a resposta da API seja de um status inesperado a exceção **UnexpectedServerResponse(response)** é levantada.

### shorten_url(url[, alias])
Recebe uma **url** e um **alias**(opcional), registra a associação entre url e alias e por fim retorna o alias (string).

Um alias é gerado automaticamente, caso nenhum tenha sido passado como parâmetro. 

- Caso o alias passado como parâmetro já tenha sido registrado no banco a exceção **AliasAlreadyExists(alias)** é levantada.
- Caso a resposta da API seja de um status inesperado a exceção **UnexpectedServerResponse(response)** é levantada.


### get_top_links()
Retorna as dez **urls encurtadas** mais acessadas.

A estrutura de dados retornada é um **array** de tuplas no formato: ``` (url_encurtada, quantidade_de_acessos) ```.
 
- Caso a resposta da API seja de um status inesperado a exceção **UnexpectedServerResponse(response)** é levantada.


## Exceptions

- **AliasNotFound(alias)**: alias não está registrado no banco de dados.

- **AliasAlreadyExists(alias)**: alias já possui um registro no banco.

- **UnexpectedServerResponse(response)**: o serviço retornou um status inesperado.