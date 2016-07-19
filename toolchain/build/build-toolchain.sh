#!/bin/bash
HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


function usage {
cat << EOF
usage: $0 \$DIR
EOF
}
#############################################

DIR=$1

if [ ! "${DIR:0:1}" = "/" ]; then
    DIR="$(pwd)/$DIR"
fi

CT_VERSION="crosstool-ng-1.20.0"
CT_DIR="$DIR/$CT_VERSION"
CT_TC_BUILD_DIR="$DIR/build"
CT_TC_DIR="$DIR/x-tools"


LOG="$DIR/build.log"

if [ ! -e "$DIR" ]; then
	mkdir $DIR
fi

if [ -n "$1" ]; then
	cd $DIR
  if [ ! -e "$DIR/$CT_VERSION.tar.bz2"]; then
    echo "Downloading $CT_VERSION"
	   wget -q http://crosstool-ng.org/download/crosstool-ng/$CT_VERSION.tar.bz2
  else
    echo "$CT_VERSION already downloaded"
  fi

  if [ ! -e "$CT_DIR" ]; then
	  tar xjf $CT_VERSION.tar.bz2
  fi

	cd $CT_DIR
	echo "Building $CT_VERSION"
	./bootstrap >> $LOG
	./configure --enable-local --with-libtool=/usr/share/libtool >> $LOG
	make >> $LOG

	echo "Building toolchain"
  if [ ! -e "$CT_TC_BUILD_DIR" ]; then
	   mkdir $CT_TC_BUILD_DIR
  fi

	cd $CT_TC_BUILD_DIR
  if [ ! -e "$CT_TC_BUILD_DIR/.config"]; then
	   cp -v $HOME_DIR/ct_mpw.conf $CT_TC_BUILD_DIR/.config
  fi

	$CT_DIR/ct-ng build
else
	usage
fi
