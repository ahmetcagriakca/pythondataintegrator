# Introduction 
The application that we aim to perform the integration processes easily and quickly through APIs

# Getting Started

1.	Installation process
    -  Application running with python 3.6.8 version preferred installation url:
    https://www.python.org/downloads/release/python-368/    
2.	Software dependencies
    - Postgresql is preferred database application. You can still use any relational database with sqlalchemy, just configure it.
    - And you must install related database client
3.	API references
    After python installation run package install command :
    -   pip install -r requirements.txt 
4. Database Initialize
    -   database migration run scripts
        alembic upgrade head
alembic revision --autogenerate -m "baseline"

# Build and Test
After all installation, you can run application with "python startup.py" also you can run test scenarios  
