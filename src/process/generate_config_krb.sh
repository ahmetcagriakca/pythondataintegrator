#!/bin/sh -eu

if [ -z "${KRB_REALM:-}" ]; then
    KRB_REALM=undefined
else
    KRB_REALM=$KRB_REALM

fi
 

cat <<EOF
[libdefaults]
default_realm = $KRB_REALM
kdc_timesync = 1
ccache_type = 4
forwardable = true
proxiable = true
[realms]
$KRB_REALM = {
kdc = $KRB_REALM
default_domain = $KRB_REALM
}
EOF
