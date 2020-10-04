FROM python:3

WORKDIR /usr/src/app

#Wait for postgres to be ready
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

CMD /wait && python "./run.py"