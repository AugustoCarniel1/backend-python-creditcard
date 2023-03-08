**Explicação das insiprações**

Framework utilizado: Django REST API
Justificativa: Tenho uma maior familiaridade então conseguiria fazer algo mais fluído

Criptografia utilizada: RSA cryptography
Justificativa: Por ser assimétrica, apenas os usuários que possuirem a chave privada conseguem descriptograr as informações. Neste caso deixei no arquivo como .pem para qualquer um poder testar, mas o ideal seriam essas chaves serem variaveis de ambiente em algum servidor.

Autenticação utilizada: Token Auth
Justificativa: Um método de autenticação onde apenas os usuários que possuem um cadastro no django ou na API podem ter acesso as funções, assim criariasse um cadastro para cada cliente e poderia separar o cartões e informações baseado no token de acesso do usuário.

Banco de Dados: SQLite
Justificativa: Por ser apenas um projeto de porte pequeno, e dificilmente passará de 100 cartões em testes, utilizei o próprio SQLite para suportar as informações necessárias.




Guide through the code
**1 STEP**

On root run to create and virtual enviroment
```
python -m venv venv
```
Then inside the virtual enviroment, 
```
pip install -r requirements.txt 
```
to download all libraries of the project.


**2 STEP**
```
cd /creditcard
```
then run this command if you want to create your own superuser
```
python manage.py createsuperuser
```
or use my login to generate your access token.
username: augusto.carniel
password: 123456


**3 STEP**
```
python manage.py runserver
```
Run this command to start your server and start to test the application

You can use postman to call the url's.

Documentation
```
api/v1/generate-key' -> POST Method / Create the .pem files to cryptography the cards
api/v1/token/auth -> POST Method / Login in Django to generate your token
```
With this django token, you can implent in our header to access the other functions
```
Authorization: 'Token {token}'
```

```
api/v1/credit-card -> PUT Method / Insert a new card on database / Require: expiration_date (MM/YYYY), holder (str), number (str), cvv (int)
api/v1/credit-card/list -> GET Method / List all credit cards
api/v1/credit-card/{key} -> GET Method / List an specific credit card
```


To run the unit test simply type
```
python manage.py test
```


