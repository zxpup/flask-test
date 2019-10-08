FROM python:3.7
EXPOSE 8081
COPY . /project/cinderella/
WORKDIR /project/cinderella/
CMD python3 cinderella.py
