# Python runtime with pyodbc to connect to SQL Server# Python runtime with pyodbc to connect to SQL Server
FROM  centos:7

## Mssql client installation

#RedHat Enterprise Server 7
RUN curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo

RUN yum remove unixODBC-utf16 unixODBC-utf16-devel #to avoid conflicts
RUN ACCEPT_EULA=Y yum install -y msodbcsql17
# optional: for bcp and sqlcmd
RUN ACCEPT_EULA=Y yum install -y  mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN source ~/.bashrc
# optional: for unixODBC development headers

# Oracle installation
RUN yum install -y wget unzip libaio

RUN wget https://download.oracle.com/otn_software/linux/instantclient/19800/oracle-instantclient19.8-basiclite-19.8.0.0.0-1.x86_64.rpm?xd_co_f=ad019b31-76ea-48dd-a744-e6b838b7a809
RUN rpm -ivh oracle-instantclient19.8-basiclite-19.8.0.0.0-1.x86_64.rpm?xd_co_f=ad019b31-76ea-48dd-a744-e6b838b7a809

RUN echo export LD_LIBRARY_PATH=/usr/lib/oracle/19.8/client64/lib/ >> /etc/bashrc
RUN echo export ORACLE_HOME=/usr/lib/oracle/19.8/client64 >> /etc/bashrc
RUN echo export PATH=$ORACLE_HOME/bin:$PATH >> /etc/bashrc


# python and unixODBC installation
RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y python3 python3-pip gcc-c++ python3-devel unixODBC-devel
ARG         PIP_URL_PRIVATE
RUN         echo "Python repository url: $PIP_URL_PRIVATE"
#Python packages added to image
RUN pip3 install  cx_Oracle
RUN pip3 install  pyodbc



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