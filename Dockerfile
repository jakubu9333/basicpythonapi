
FROM python

WORKDIR /app

COPY requirements.txt requirements.txt

RUN  pip install -r requirements.txt


COPY . .

ENV FLASK_APP=./app/aplication.py

EXPOSE 5000

RUN python init.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]