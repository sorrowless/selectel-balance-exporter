FROM python:3.10 as build
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt
COPY . .
EXPOSE 8000

WORKDIR /app/selectel_balance_exporter
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
