# URL Shortener API

Documentação do projeto URL Shortener para o processo seletivo da Bemobi. 
Para rodar o projeto basta seguir os seguintes passos:
1. Clonar o repositório
2. Executar o comando docker-compose build
3. Executar o comando docker-compose up

Obs.: A primeira inicialização demora um pouco mais devido a criação do banco.

### Shorten URL
![Shorten URL](https://tinyurl.com/yydlnqg4)

1. Realize uma chamada a API passando a **url** a ser encurtada e um parâmetro opcional **custom_alias**.
    1. Caso o **custom_alias** já exista, é retornado um erro ```{err_code: 001, description: Custom Alias already exists }```
    2. Caso o parâmetro **custom_alias** não tenha sido utilizado, então a função **shorten_url** gera um alias utilizando o algoritmo de hashing MD5 e a codificação em base64 com limite de 8 caracteres.
2. O novo link gerado é salvo no banco de dados Postgres.
3. É retornado um resultado contendo a url original, a url encurtada e o tempo de execução da operação. 

Exemplos:

* Chamada sem custom_alias
```
PUT http://localhost:5000/addlink?url=https://www.bemobi.com

{
    "alias": "BVWa8mUw",
    "message": "Short URL created",
    "time_taken": "38.53ms",
    "url": "https://www.bemobi.com"
}
```

* Chamada com custom_alias
```
PUT http://localhost:5000/addlink?url=http://www.bemobi.com.br&custom_alias=bemobi

{
    "alias": "bemobi",
    "message": "Short URL created",
    "time_taken": "42.064ms",
    "url": "https://www.bemobi.com"
}
```

* Chamada com custom_alias que já existe
```
PUT http://localhost:5000/addlink?url=http://www.github.com&custom_alias=bemobi

{
    "alias": "bemobi",
    "description": "Custom Alias already exists",
    "err_code": "001"
}
```


### Retrieve URL
![Retrieve URL](https://tinyurl.com/yytqr2vk)

1. Realize uma chamada a API passando o **alias** que deseja acessar
    1. Caso não exista um link com esse **alias** é retornado um erro ```{err_code: 002, description: Shortened URL not found}```.
2. A url original é recuperada através de uma consulta ao banco de dados Postgres.
3. É retornado um redirecionamento para a url original.

### Top Viewed URLs
![Top URLs](https://tinyurl.com/y4nemar4)
1. Realize uma chamada ao endpoint ``` /top ```.
2. É retornado um JSON com as 10 urls mais accessadas e sua quantidade de visitas.

Exemplo:

``` 
GET http://localhost:5000/top

{
    "1V0H_0~X": 4,
    "7g62Ji5_": 2,
    "K88Lbt3I": 3,
    "QeuJ6sPy": 10,
    "TAkcAEf8": 13,
    "a9MWHVva": 5,
    "l9lDxS8I": 6,
    "ossy0Vtd": 8,
    "phO8CXWY": 11,
    "tes": 20
}
```

## Testes

Comando para executar os testes:
``` docker-compose run url-shortener py.test ```
