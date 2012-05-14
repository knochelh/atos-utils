#!/usr/bin/env bash
#
#

source `dirname $0`/common.sh

TEST_CASE="ATOS audit nested driver"

# Generate a local surdriver that recursively invoke gcc
real_gcc=`which gcc`
cat >gcc.c <<EOF
#include <unistd.h>

int main(int argc, char *argv[])
{
  argv[0] = "gcc";
  execvp("$real_gcc", argv);
  return 1;
}
EOF
gcc -o gcc gcc.c

# Audit a build with this surdriver
$ROOT/atos-audit ./gcc -o sha1-c  $ROOT/examples/sha1-c/sha.c $ROOT/examples/sha1-c/sha1.c
[ -f atos-configurations/build.audit ]

# Check that we recorded a single gcc invocation
lines=`grep CC_DEPS atos-configurations/build.audit | wc -l | cut -f1 -d' '`
[ "$lines" = 1 ]