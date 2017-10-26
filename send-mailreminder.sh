#!/bin/sh

SIGNERS_GROUP=tunnelberlin-signer
MAIL_SUBJECT="Tunnel-Berlin - open requests notice"

#   nothing to configure down here  #

MYDIR=`dirname $0`

# get users of group
MAIL_RCPT=`getent group $SIGNERS_GROUP| cut -d : -f 4`
SIGNCOUNT=`$MYDIR/runscript.sh $MYDIR/manage.py requests show|wc -l`


mail -s "$MAIL_SUBJECT" "$MAIL_RCPT" <<EOF
Hi Certificate-signers,

this is a notice showing you the number of open certificate-requests.

Currently there are $SIGNCOUNT requests to process. Probably you find the time to check by for signing them.
EOF
