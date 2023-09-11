FROM python:3.9.18-bullseye
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt 
CMD ["python3", "./tubular.py"]
EXPOSE 8000
