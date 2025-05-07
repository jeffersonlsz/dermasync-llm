@echo off
echo 🔧 Buildando imagem Docker...
gcloud builds submit --tag gcr.io/dermasync-3d14a/llm-api

echo 🚀 Fazendo deploy para Cloud Run...
gcloud run deploy llm-api --image gcr.io/dermasync-3d14a/llm-api --platform managed --region us-central1 --allow-unauthenticated --set-env-vars GEMINI_API_KEY=AIzaSyCd8KvANF4xdZMrCynUAGlTY1cfnKeeItc

echo 🌐 URL do serviço:
gcloud run services describe llm-api --platform managed --region us-central1 --format="value(status.url)"

echo 🛠️  Deploy concluído com sucesso!