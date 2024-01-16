if [ -z "${KRB_USER:-}" ]; then
    KRB_USER=undefined
else
    KRB_USER=$KRB_USER
fi
 

if [ -z "${KRB_PASSWORD:-}" ]; then
    KRB_PASSWORD=undefined
else
    KRB_PASSWORD=$KRB_PASSWORD
fi
printf "%b" "addent -password -p $KRB_USER -k 1 -e aes256-cts-hmac-sha1-96\n$KRB_PASSWORD\nwkt $KRB_USER.keytab\nexit" | ktutil

kinit -k -t $KRB_USER.keytab $KRB_USER$