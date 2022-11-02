#!/bin/bash

DIR="$(dirname "$(realpath "$0")")"
DIR="$(realpath $DIR/../..)"
WORKSPACE=/tmp/ci_workspace

set -eE

DEBIAN_FRONTEND=noninteractive
# [ "$EUID" -eq 0 ] || sudo="sudo -E"
# $sudo apt-get install -y libhdf5-dev libatlas-base-dev libboost-system-dev
# $sudo apt-get install -y g++-aarch64-linux-gnu gcc-aarch64-linux-gnu

# pip3 install setuptools wheel

[ -d $WORKSPACE ] && [ "$(ls -A ${WORKSPACE})"="" ] && rm -rf ${WORKSPACE}
mkdir -p $WORKSPACE

dep_dir=$DIR/dependencies

# download libsophon
if [ $LIBSOPHON_URL ]; then
    libsophon_tar=$WORKSPACE/libsophon.tar.gz
    wget -O $libsophon_tar $LIBSOPHON_URL
else
    for fn in $dep_dir/libsophon*.tar.gz; do libsophon_tar=$fn; done
fi
libsophon_dir=$WORKSPACE/libsophon
mkdir -p $libsophon_dir
tar --wildcards --strip-components=4 -xvf $libsophon_tar \
    -C $libsophon_dir libsophon_*_x86_64/opt/sophon/libsophon*

# download protoc
protoc_zip=protoc-3.19.4-linux-x86_64.zip
wget -O $WORKSPACE/$protoc_zip \
    https://github.com/protocolbuffers/protobuf/releases/download/v3.19.4/$protoc_zip
unzip -o -d $WORKSPACE/protoc $WORKSPACE/$protoc_zip
PATH=$PATH:$WORKSPACE/protoc/bin

# download tpu-nntc
if [ $TPU_NNTC_URL ]; then
    tpu_nntc_tar=$WORKSPACE/tpu_nntc.tar.gz
    wget -O $tpu_nntc_tar $TPU_NNTC_URL
else
    for fn in $dep_dir/tpu-nntc*.tar.gz; do tpu_nntc_tar=$fn; done
fi
tpu_nntc_dir=$WORKSPACE/tpu_nntc
mkdir -p $tpu_nntc_dir
tar -xvf $tpu_nntc_tar -C $tpu_nntc_dir

# download tpu-mlir
if [ $TPU_MLIR_URL ]; then
    tpu_mlir_tar=$WORKSPACE/tpu_mlir.tar.gz
    wget -O $tpu_mlir_tar $TPU_MLIR_URL
else
    for fn in $dep_dir/tpu-mlir*.tar.gz; do tpu_mlir_tar=$fn; done
fi
tpu_mlir_dir=$WORKSPACE/tpu_mlir
mkdir -p $tpu_mlir_dir
tar -xvf $tpu_mlir_tar -C $tpu_mlir_dir