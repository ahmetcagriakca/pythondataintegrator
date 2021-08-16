#!/bin/sh -eu

if [ -z "${AUTHORITY:-}" ]; then
    AUTHORITY=undefined
else
    AUTHORITY=$(jq -n --arg AUTHORITY "$AUTHORITY" '$AUTHORITY')
fi

if [ -z "${CLIENT_ID:-}" ]; then
    CLIENT_ID=undefined
else
    CLIENT_ID=$(jq -n --arg CLIENT_ID "$CLIENT_ID" '$CLIENT_ID')
fi

if [ -z "${REDIRECT_URI:-}" ]; then
    REDIRECT_URI=undefined
else
    REDIRECT_URI=$(jq -n --arg REDIRECT_URI "$REDIRECT_URI" '$REDIRECT_URI')
fi

if [ -z "${POST_REDIRECT_URI:-}" ]; then
    POST_REDIRECT_URI=undefined
else
    POST_REDIRECT_URI=$(jq -n --arg POST_REDIRECT_URI "$POST_REDIRECT_URI" '$POST_REDIRECT_URI')
fi

if [ -z "${SLIENT_REDIRECT_URI:-}" ]; then
    SLIENT_REDIRECT_URI=undefined
else
    SLIENT_REDIRECT_URI=$(jq -n --arg SLIENT_REDIRECT_URI "$SLIENT_REDIRECT_URI" '$SLIENT_REDIRECT_URI')
fi

if [ -z "${API_URI:-}" ]; then
    API_URI=undefined
else
    API_URI=$(jq -n --arg API_URI "$API_URI" '$API_URI')
fi

if [ -z "${NOTIFICATION_URI:-}" ]; then
    NOTIFICATION_URI=undefined
else
    NOTIFICATION_URI=$(jq -n --arg NOTIFICATION_URI "$NOTIFICATION_URI" '$NOTIFICATION_URI')
fi
 
cat <<EOF
window.AUTHORITY=$AUTHORITY;
window.CLIENT_ID=$CLIENT_ID;
window.REDIRECT_URI=$REDIRECT_URI;
window.POST_REDIRECT_URI=$POST_REDIRECT_URI;
window.SLIENT_REDIRECT_URI=$SLIENT_REDIRECT_URI;
window.API_URI=$API_URI;
window.NOTIFICATION_URI=$NOTIFICATION_URI;
EOF
