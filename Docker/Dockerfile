FROM python:3.8.18
#Update system and add reqs
RUN apt update
RUN apt install -y make automake gcc g++ subversion python3-dev
RUN pip install --upgrade pip
#Add source files
WORKDIR /opt/code/source
COPY *.py ./
COPY requirements.txt .
#Install requirements
RUN pip install -r requirements.txt
CMD [ "python", "main.py"]
