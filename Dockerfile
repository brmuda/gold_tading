FROM python:3.11.7

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]