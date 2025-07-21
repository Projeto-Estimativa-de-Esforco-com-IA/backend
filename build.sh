#!/usr/bin/env bash
echo "Instalando dependências..."
pip install -r requirements.txt

echo "Executando migrate..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput
