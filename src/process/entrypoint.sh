echo 'migration will start'
alembic upgrade head
echo 'migration is done'
python3 app.py