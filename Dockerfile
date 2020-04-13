FROM python:3.7.4

WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt
COPY instagramScraper.py /app/
COPY . /app/

CMD [ "python", "instangramScraper.py" ]