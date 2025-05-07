@echo off
setlocal enabledelayedexpansion

REM === CONFIGURAÇÕES ===
set PROJECT_ID=dermasync-3d14a
set REGION=us-central1
set SERVICE_NAME=llm-api
set IMAGE_NAME=gcr.io/%PROJECT_ID%/%SERVICE_NAME%
set GEMINI_API_KEY=AIzaSyCd8KvANF4xdZMrCynUAGlTY1cfnKeeItc

echo 🔧 Buildando imagem Docker...
gcloud builds submit --tag %IMAGE_NAME%
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao construir a imagem. Abortando.
    goto fimcomerro
)

pause

echo 🚀 Fazendo deploy para Cloud Run...
gcloud run deploy %SERVICE_NAME% ^
  --image %IMAGE_NAME% ^
  --platform managed ^
  --region %REGION% ^
  --allow-unauthenticated ^
  --set-env-vars GEMINI_API_KEY=%GEMINI_API_KEY%
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Deploy falhou. Verifique erros no console.
    exit /b
)

pause
echo 🔍 Recuperando URL pública do serviço...
for /f "delims=" %%i in ('gcloud run services describe %SERVICE_NAME% --platform managed --region %REGION% --format="value(status.url)"') do set SERVICE_URL=%%i
pause
echo 🌐 Serviço publicado com sucesso:
echo.
echo     %SERVICE_URL%
echo.

echo 🔍 Verificando se /docs está acessível...
powershell -Command "try { $res = Invoke-WebRequest -Uri '%SERVICE_URL%/docs' -UseBasicParsing -TimeoutSec 5; if ($res.StatusCode -eq 200) { echo ✅ Endpoint /docs ativo! } else { echo ⚠️ Endpoint retornou código: $res.StatusCode } } catch { echo ❌ Falha ao acessar /docs }"

goto fimsucesso
endlocal
:fimcomerro
echo Fim com erro...
goto fimsucesso
pause

:fimsucesso
echo Fim com sucesso...
