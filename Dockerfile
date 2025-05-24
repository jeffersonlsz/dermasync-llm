# Usa imagem leve do Python
FROM python:3.10-slim-bullseye

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta usada pelo Cloud Run
EXPOSE 8080

# Comando que inicia o servidor FastAPI via uvicorn (porta dinâmica)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
