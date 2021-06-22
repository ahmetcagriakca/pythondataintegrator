# Python runtime with pyodbc to connect to SQL Server# Python runtime with pyodbc to connect to SQL Server
FROM  centos:7

RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y python3 python3-pip 

ARG         PIP_URL_PRIVATE
RUN         echo "Python repository url: $PIP_URL_PRIVATE"
RUN         pip3 install --upgrade pip
COPY       	./requirements.txt /app/requirements.txt
WORKDIR    	/app

RUN 		pip3 install -r requirements.txt 
RUN         pip3 list
COPY       	. /app
WORKDIR    	/app
RUN python3 --version
RUN date

ADD entrypoint.sh .
# # openshift set permission to non-root users for /app directory
RUN chgrp -R 0 /app && \
    chmod -R g=u /app && \
    chgrp -R 0 /etc/passwd && \
    chmod -R g=u /etc/passwd

# # openshift set running user 
USER 1001
ENTRYPOINT 	["/bin/sh"]
CMD 	["entrypoint.sh"]