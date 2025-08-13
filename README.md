# 📦 Compactador de PDFs

##  Descrição

O **Compactador de PDFs** é uma aplicação desenvolvida para comprimir arquivos PDF, tornando-os mais leves e fáceis de compartilhar. Ideal para quem precisa enviar documentos por e-mail ou armazená-los sem ocupar muito espaço.

---

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal para o desenvolvimento da aplicação.
- **Tkinter**: Interface gráfica para facilitar a interação do usuário.
- **Ghostscript**: Utilizado para compressão eficiente de PDFs.
- **Pyinstaller**: Utilizado para empacotar os arquivos necessários e transformar em um app.


---
## 🚀 Como Usar

1. Clone este repositório:

 digite no terminal do vs code,ou outro editor de preferência:
git clone https://github.com/paulohenrique-souza-dev/Compactador-de-PDFS.git


---


Após isso crie a venv com :python -m venv venv

Ative a venv com :venv/scripts/activate

--- 
Instale as dependências:

pip install -r requirements.txt  

---
Após instalar as bibliotecas confirme o caminho da imagem e demais arquivos....

Teste o programa rodando local,se estiver tudo ok,sem erros ,ai sim vamos para a última etapa que é transformar em um aplicativo.

---
## 📦  Transformando em App
No seu terminal digite:

pyinstaller --onefile --windowed --name=CompactadorPDF \
  --add-binary "gswin64c.exe;." \
  --add-data "sua imagem;." \
  script.py

Essa etapa de transformar em app, é a mais dificil do programa,qualquer dúvida mande para mim,ou busque na web que tem solução ...


