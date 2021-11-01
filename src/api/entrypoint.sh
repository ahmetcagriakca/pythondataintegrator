if [ "$UPGRADE_DATABASE"=="true" ]
then
    alembic upgrade head
fi
python app.py
