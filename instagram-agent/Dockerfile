FROM python:3.11-slim

WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# La base SQLite vive acá: móntalo como volumen o pierdes el historial
# y los borradores en cada despliegue.
VOLUME ["/srv/datos"]
ENV IG_DB_PATH=/srv/datos/instagram.db

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
