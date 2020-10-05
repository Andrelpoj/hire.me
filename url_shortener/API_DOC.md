# URL Shortener API

Documentação do projeto URL Shortener para o processo seletivo da Bemobi.


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
![Retrieve URL](https://tinyurl.com/y4rfn44r)

1. Realize uma chamada a API passando o **alias** que deseja acessar
    1. Caso não exista um link com esse **alias** é retornado um erro ```{err_code: 002, description: Shortened URL not found}```.
2. A url original é recuperada através de uma consulta ao banco de dados Postgres.
3. É retornado um redirecionamento para a url original.


### Top Viewed URLs

