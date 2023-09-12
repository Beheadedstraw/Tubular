FROM python:3.9.18-bullseye
VOLUME [ "/data" ]
WORKDIR /data
COPY . .
RUN pip install --no-cache-dir -r requirements.txt 
CMD ["python3", "./app/tubular.py"]
EXPOSE 8000
