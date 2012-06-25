#!/usr/bin/env bash
#
#

source `dirname $0`/common.sh

TEST_CASE="ATOS exploration loop test"

# this test must only be run manually
[ "$MAKELEVEL" == "" ] || skip

echo "Running test in: $TMPTEST"


tradeoff_variants() {
    regexp="^.*[\"\']variant[\"\']: [\"\']\([^\"\']*\)[\"\'].*$"
    $ROOT/lib/atos/atos_lib.py speedups \
	--tradeoff=5 --tradeoff=1 --tradeoff=0.2 \
	| grep "$regexp" | sed "s/$regexp/\1/" | sort -u
}


$ROOT/bin/atos-init \
    -n 0 \
    -r "$ROOT/examples/sha1-c/run.sh" \
    -b "gcc -o sha1-c $ROOT/examples/sha1-c/sha.c $ROOT/examples/sha1-c/sha1.c"

$ROOT/lib/atos/atos_lib.py create_db --type=json


echo "# atos-explore..."
$ROOT/bin/atos-explore -q


$ROOT/bin/atos-graph -x1 -t sha1-c --tradeoff=5 --tradeoff=1 --tradeoff=0.2 --follow > /dev/null &


echo "# atos-explore-inline..."
tradeoff_variants
$ROOT/bin/atos-explore-inline -q -M20 `tradeoff_variants`


echo "# atos-explore-loop..."
tradeoff_variants
$ROOT/bin/atos-explore-loop -q -M20 `tradeoff_variants`


echo "# simplifying selected points..."
tradeoff_variants
for v in `tradeoff_variants`; do
    $ROOT/lib/atos/atos_toolkit.py -q -k --gen-one-off-rnd=$v,3
done


echo "# selected points:"
tradeoff_variants

echo -n "close graph and press <enter> to quit "
read