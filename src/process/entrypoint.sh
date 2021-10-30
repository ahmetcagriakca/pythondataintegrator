export $(id)
echo "$uid" 
echo "$(id)" 
echo "default:x:$uid:0:user for openshift:/tmp:/bin/bash" >> /etc/passwd
python app.py