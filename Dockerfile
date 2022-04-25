FROM python:3.9.1

WORKDIR /app

# COPY . /app

# same as working dir is /app
COPY . .

RUN pip install -r ./requirements.txt


CMD ["python", "app.py"]
