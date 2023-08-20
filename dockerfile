FROM ubuntu

RUN apt-get update
RUN apt-get install -y python3 python3-pip

# RUN git clone git@github.com:Dvorfin/HH-parser-on-flask.git

WORKDIR /home/user

COPY . .

RUN cd HH-parser-on-flask/

#RUN pip3 install -r requirements

COPY HH-parser-on-flask/requirements.txt .

RUN pip install -r requirements.txt && rm requirements.txt

#ENTRYPOINT FLASK_APP=/HH-parser-on-flask/app.py flask run --host=0.0.0.0 --port=5000

ENTRYPOINT [ "python3", "HH-parser-on-flask/app.py" ]

#EXPOSE 5000