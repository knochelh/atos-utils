#!/usr/bin/env bash
#
#

source `dirname $0`/common.sh

TEST_CASE="ATOS lib frontier query"

$ROOT/bin/atos-init \
    -r "$ROOT/examples/sha1-c/run.sh" \
    -b "gcc -o sha1-c $ROOT/examples/sha1-c/sha.c $ROOT/examples/sha1-c/sha1.c"

$ROOT/bin/atos-opt -r -a "-O2"

$ROOT/lib/atos/atos_lib.py speedups -f \
    | $ROOT/lib/atos/atos_lib.py query -C- -t -q'$[*].variant' \
    > frontier.variant.txt

[ `cat frontier.variant.txt` = "OPT-O2" ]
