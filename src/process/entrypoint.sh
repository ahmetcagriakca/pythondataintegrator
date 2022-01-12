#!/bin/sh -eu
export $(id)
echo "$uid" 
echo "$(id)" 
echo "default:x:$uid:0:user for openshift:/tmp:/bin/bash" >> /etc/passwd

if [ -z "${KRB_REALM:-}" ]; then
    echo 'Realm undifened'
else
    /usr/src/app/generate_config_krb.sh > /etc/krb5.conf
fi
if [ -z "${KRB_USER:-}" ]; then
    echo 'User undifened'
else
    /usr/src/app/login_krb.sh
fi
python app.py