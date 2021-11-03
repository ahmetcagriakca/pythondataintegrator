FROM  pythondataintegrator/process:base

RUN     mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN     pip install  --upgrade pip
COPY    ./requirements.txt /usr/src/app/requirements.txt
RUN     pip install  -r requirements.txt 

RUN     pip list
RUN     python --version
RUN     date

COPY    . /usr/src/app

# # openshift set permission to non-root users for /app directory
RUN chgrp -R 0 /usr/src/app && \
    chmod -R g=u /usr/src/app && \
    chgrp -R 0 /etc/passwd && \
    chmod -R g=u /etc/passwd

# # set running user 
USER 1001
ENTRYPOINT 	["/bin/sh"]
CMD 	["entrypoint.sh"]