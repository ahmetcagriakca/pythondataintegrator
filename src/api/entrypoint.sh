if [ -z "$UPGRADE_DATABASE" ]
then
    echo "UPGRADE_DATABASE not defined"
else 
    alembic upgrade head
fi
python app.py
