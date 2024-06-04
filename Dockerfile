FROM python:3.11.8
#Update system and add reqs
RUN apt update
RUN apt install -y make automake gcc g++ subversion python3-dev
RUN pip install --upgrade pip
#Add source files
WORKDIR /opt/code/source
COPY / ./
COPY requirements.txt .
#Install requirements
RUN pip install -r requirements.txt
CMD [ "python", "-u", "main.py"]
