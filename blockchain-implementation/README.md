

## Projeto

As implementações tem como objetivo explorar as funcionalidades do blockchain por meio de implementações em python.

- As chamadas para as funcionalidades do blockchain estão no arquivo testes.py

- A estrutura dos arquivos estão divididas em módulos

### Recomendação
- Estudar a documentação https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa.html
- Utilizar Anaconda e Spyder

### Requisitos
- PIP
 > python -m pip --version

### signatures.py
 - Primeiramente são gerados as chaves públicas e privadas
 - Depois uma mensagem é assinada pela chave privada e verificada com a chave pública
  
### hashing.py
 - Utilizado para gerar hash de uma mensagem

  
### encryption_decryption.py
 - Realiza a criptografia da mensagem com a chave publica 
 - Descriptografa com a chave privada