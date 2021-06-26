FROM  python:3.6.8

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
ENTRYPOINT 	["python"]
CMD 		["app.py"]