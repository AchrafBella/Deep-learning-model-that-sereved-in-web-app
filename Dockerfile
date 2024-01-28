FROM python:3.9

WORKDIR /DL_project

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./APP /DL_project/APP
COPY ./database /DL_project/database

RUN mkdir -p static

EXPOSE 8080

ENV FLASK_APP=APP/api.py

CMD [ "flask", "run", "--host=0.0.0.0", "--port=8080"]
