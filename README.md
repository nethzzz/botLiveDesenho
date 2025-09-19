# Fiz apenas para gravar o vídeo no meu canal!
# Usei IA para criar todos os comentarios de apoio e esse README, então se tiver algum erro acontece kkkkk

Este é um projeto em Python que cria um sistema interativo para lives no YouTube. O bot identifica novos inscritos em tempo real, exibe o nome e a foto de perfil em uma interface para ser usada no OBS (ou qualquer software de streaming) e permite ao streamer navegar por uma fila de novos inscritos para que ninguém seja esquecido.
Em seguida, tem outro bot que irá executar o desenho no espaço escolhido ou caso o usuario queira desenhar ele mesmo é só não rodar o bot.


## ✨ Funcionalidades

* **Fila de Novos Inscritos**: Garante que todos os novos inscritos sejam exibidos, mesmo que vários se inscrevam ao mesmo tempo.
* **Controle de Navegação**: Botões de "Próximo" e "Anterior" para navegar pelo histórico de inscritos.
* **Interface para OBS**: Uma página web local (`display.html`) para ser adicionada como "Fonte de Navegador" no OBS, exibindo os dados em tempo real.
* **Download da Foto de Perfil**: Salva a foto do inscrito atual localmente (`ultimoinscrito.png`), permitindo fácil acesso.
* **Atualização em Tempo Real**: O número total de inscritos e o inscrito atual são atualizados dinamicamente.

## 🛠️ Tecnologias Utilizadas

* **Backend**: Python
    * **Flask**: Para criar o servidor web local.
    * **Google API Client Library**: Para interagir com a API de Dados do YouTube v3.
* **Frontend**: HTML, CSS, JavaScript (puro)
* **Integração**: OBS Studio (ou similar)

## 🚀 Instalação e Configuração

Siga estes passos para configurar e rodar o projeto em sua máquina.

### Pré-requisitos

* [Python 3.8+](https://www.python.org/downloads/) instalado.
* `pip` (gerenciador de pacotes do Python).

### 1. Clone o Repositório

```bash
git clone [https://github.com/SEU-USUARIO/NOME-DO-SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/NOME-DO-SEU-REPOSITORIO.git)
cd NOME-DO-SEU-REPOSITORIO
```

### 2. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 3. Configure a API do YouTube (Passo Mais Importante)

Este projeto requer credenciais da API do Google para funcionar.

1.  **Crie um Projeto no Google Cloud Console**: Acesse o [Google Cloud Console](https://console.cloud.google.com/) e crie um novo projeto.
2.  **Ative a API do YouTube**: No seu projeto, vá para "APIs e Serviços" > "Biblioteca" e procure por **"YouTube Data API v3"**. Clique em **"Ativar"**.
3.  **Configure a Tela de Permissão OAuth**:
    * Vá para "APIs e Serviços" > "Tela de permissão OAuth".
    * Selecione **"Externo"** e clique em "Criar".
    * Preencha as informações necessárias (nome do app, e-mail de suporte). Não precisa preencher tudo.
    * Na tela de "Escopos", não adicione nada.
    * Em **"Usuários de teste"**, adicione o endereço de e-mail da Conta Google que gerencia o canal do YouTube que você vai monitorar. **Este passo é obrigatório**.
4.  **Crie as Credenciais**:
    * Vá para "APIs e Serviços" > "Credenciais".
    * Clique em **"+ CRIAR CREDENCIAIS"** e selecione **"ID do cliente OAuth 2.0"**.
    * Em "Tipo de aplicativo", selecione **"Aplicativo para computador"**.
    * Dê um nome e clique em "Criar".
5.  **Baixe o Arquivo de Credenciais**:
    * Após criar a credencial, uma janela aparecerá. Clique em **"FAZER O DOWNLOAD DO JSON"**.
    * Renomeie o arquivo baixado para **`client_secrets.json`** e coloque-o na pasta raiz do projeto. **NÃO COMPARTILHE ESTE ARQUIVO COM NINGUEM!**


## ▶️ Como Usar

1.  **Execute o Servidor**: Abra um terminal na pasta do projeto e execute o comando:
    ```bash
    python app.py
    ```
2.  **Autorização Inicial**: Na primeira vez que você rodar, uma janela do navegador será aberta pedindo para você fazer login e autorizar o acesso à sua conta do YouTube. Faça o login com a conta que você adicionou como "usuário de teste". Após a autorização, um arquivo `token.pickle` será criado.
3.  **Adicione a Tela no OBS**:
    * No OBS, adicione uma nova fonte do tipo **"Navegador"**.
    * Marque a opção "Arquivo local".
    * Aponte para o arquivo `display.html` na pasta do projeto, OU (melhor) use a URL local.
    * Na URL, coloque: `http://127.0.0.1:5000/display`
    * Defina a largura e altura desejadas.
4.  **Use o Painel de Controle**:
    * Abra seu navegador e acesse `http://127.0.0.1:5000`.
    * Use os botões "Próximo Inscrito" e "Inscrito Anterior" para controlar as informações que aparecem na tela do OBS.
5.  * Quando quiser rodar o bot use, ele irá usar automaticamente a foto baixada
    ```bash
    python botDesenho.py
    ```

## 📁 Estrutura dos Arquivos

* `app.py`: O servidor Flask que gerencia toda a lógica, chamadas à API e a fila de inscritos.
* `display.html`: A página que é exibida no OBS com as informações do inscrito.
* `controller.html`: A página do painel de controle com os botões.
* `requirements.txt`: Lista de dependências Python para fácil instalação.
* `client_secrets.json` (Local): Suas credenciais secretas da API. **NÃO COMPARTILHE**.
* `token.pickle` (Local): Seu token de autorização salvo. **NÃO COMPARTILHE**.
* `/fotos_inscritos/ultimoinscrito.png` (Local): A foto de perfil do inscrito atual.
*  `botDesenho.py`: o bot responsável por desenhar a imagem baixada


---
Feito por NETHZ apenas para um vídeo no youtube.
