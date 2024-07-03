FROM python:3.10

WORKDIR /

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /requirements.txt

### cache pip dependancies

COPY . .

EXPOSE 8000

CMD python run.py --mode front_dev
