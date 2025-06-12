
FROM python:3.12-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /


RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 7744

RUN chmod +x wait-for-it.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]