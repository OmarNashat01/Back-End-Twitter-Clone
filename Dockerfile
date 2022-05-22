FROM python:3.9.1

WORKDIR /

# COPY . /app

# same as working dir is /app
COPY . .

RUN pip install -r ./requirements.txt

VOLUME /storage


CMD ["python", "app.py"]
