FROM python:3.8
WORKDIR /src

COPY . /src

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:5000"]