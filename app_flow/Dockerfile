FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask flask_sqlalchemy flask_migrate psycopg2-binary werkzeug
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0"]
