FROM  python:3.9.7

RUN     mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN     pip install  --upgrade pip
COPY    ./requirements.txt /usr/src/app/requirements.txt
RUN     pip install  -r requirements.txt 

RUN     pip list
RUN     python --version
RUN     date

COPY    . /usr/src/app
# # openshift set running user 

USER    1001
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
EXPOSE 7500
ENTRYPOINT 	["python"]
CMD 		["app.py"]