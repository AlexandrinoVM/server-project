🖥️ Server Control
Projeto em Python + FastAPI para facilitar conexões com servidores locais via SSH.Permite autenticação usando senha ou chave RSA (id_rsa), e salva todos os dados de servidores e comandos em um arquivo YAML persistente.

⚡ Funcionalidades

📡 Conexão SSH com múltiplos servidores locais  
🔐 Autenticação por senha ou chave RSA  
💾 Armazena servidores e comandos em dados.yaml  
🌐 Interface web simples feita com FastAPI + Jinja2  
🐳 Fácil de rodar em container Docker com persistência de dados


📁 Estrutura de diretórios
.
├── app/
│   ├── main.py                 # Código principal (FastAPI)
│   ├── connection_manager.py   # Gerenciador de conexões SSH (Paramiko)
│   ├── dados.yaml              # Arquivo YAML com servidores e comandos
│   └── templates/              # Templates HTML (Jinja2)
├── Dockerfile
├── requirements.txt
└── README.md


🧩 Tecnologias utilizadas

FastAPI — Framework web para a API  
Paramiko — Para conexões SSH  
Jinja2 — Templates HTML  
Docker — Para empacotamento da aplicação


📥 Como clonar o projeto
git clone https://github.com/AlexandrinoVM/server-control.git
cd server-control


⚙️ Como criar a imagem Docker
Antes de executar, crie a imagem com o nome server-project:
sudo docker build -t server-project .


🚀 Como executar o container com persistência de dados
Esse comando expõe a aplicação na porta 8000 e garante que o arquivo dados.yaml seja persistente mesmo após parar o container:
sudo docker run -d -p 8000:8000 \
  -v $(pwd)/app/dados.yaml:/app/dados.yaml \
  --name server-project \
  server-project

Depois, acesse no navegador:
🔗 http://localhost:8000

📌 Observações importantes

Caso exista a chave SSH ~/.ssh/id_rsa no sistema, a conexão tentará usá-la automaticamente.  
Se não houver chave, a conexão será feita por senha.  
O arquivo dados.yaml contém todos os servidores cadastrados e comandos salvos.  
Sempre que alterar o código, execute novamente o build para atualizar a imagem:

sudo docker build -t server-project .

