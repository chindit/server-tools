#!/bin/bash

home="/home/archlinux"
target="${home}/mirror"
tmp="${home}/tmp"
lock='/tmp/mirrorsync.lck'
bwlimit=4096

source='rsync://archlinux.mailtunnel.eu/archlinux/'
lastupdate_url="rsync://archlinux.mailtunnel.eu/archlinux/lastupdate"

[ ! -d "${target}" ] && mkdir -p "${target}"
[ ! -d "${tmp}" ] && mkdir -p "${tmp}"

exec 9>"${lock}"
flock -n 9 || exit

# if we are called without a tty (cronjob) only run when there are changes
if ! tty -s && diff -b <(curl -s "$lastupdate_url") "$target/lastupdate" >/dev/null; then
	exit 0
fi

#if ! stty &>/dev/null; then
#    QUIET="-q"
#fi

rsync -rtlvH --safe-links --delete-after --progress -h ${QUIET} --timeout=60 --contimeout=6 -p \
	--delay-updates --no-motd --bwlimit=$bwlimit \
	--temp-dir="${tmp}" \
	--exclude='*.links.tar.gz*' \
	--exclude='/other' \
	--exclude='/sources' \
	${source} \
	"${target}"

#Add «--exclude='/iso' \» after «--exclude='/sources' \» to… exclude ISO's :)
#echo "Last sync was $(date -d @$(cat ${target}/lastsync))"
