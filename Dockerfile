FROM python:3.11-slim-buster

#create app folder
RUN mkdir app

#set working directory to app folder
WORKDIR /app

ENV PYTHONPATH=/app

#copy and install requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

#copy application files into image
COPY . .

#run server
CMD ["python3", "run_server.py"]