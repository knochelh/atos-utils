#!/usr/bin/env bash
#
#

source `dirname $0`/common.sh

TEST_CASE="ATOS exploration loop test"

# this test must only be run manually
[ "$MAKELEVEL" == "" ] || skip "interactive test"

echo "Running test in: $TMPTEST"


tradeoff_variants() {
    regexp="^.*[\"\']variant[\"\']: [\"\']\([^\"\']*\)[\"\'].*$"
    $ROOT/bin/atos lib speedups \
	--tradeoff=5 --tradeoff=1 --tradeoff=0.2 \
	| grep "$regexp" | sed "s/$regexp/\1/" | sort -u
}

$ROOT/bin/atos lib create_db --type=json

$ROOT/bin/atos-init \
    -r "$SRCDIR/examples/sha1-c/run.sh" \
    -b "gcc -o sha1-c $SRCDIR/examples/sha1-c/sha.c $SRCDIR/examples/sha1-c/sha1.c"

echo "# atos-explore..."
$ROOT/bin/atos-explore


$ROOT/bin/atos-graph -x1 -t sha1-c --tradeoff=5 --tradeoff=1 --tradeoff=0.2 --follow > /dev/null &


echo "# atos-explore-inline..."
tradeoff_variants
$ROOT/bin/atos-explore-inline -M20 `tradeoff_variants`


echo "# atos-explore-loop..."
tradeoff_variants
$ROOT/bin/atos-explore-loop -M20 `tradeoff_variants`

echo "# selected points:"
tradeoff_variants

echo -n "close graph and press <enter> to quit "
read
