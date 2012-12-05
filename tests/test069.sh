#!/usr/bin/env bash
#
#

source `dirname $0`/common.sh

TEST_CASE="ATOS atoslib modules unit tests"

# Unitary tests do not necessarily set python path themselves
export PYTHONPATH=$ROOT/lib/atos/python:$PYTHONPATH

python $ROOT/lib/atos/python/atoslib/deep_eq.py -v

python $ROOT/lib/atos/python/atoslib/cmd_interpreter.py

python $ROOT/lib/atos/python/atoslib/generators.py

python $ROOT/lib/atos/python/atoslib/atos_deps.py

python $ROOT/lib/atos/python/atoslib/atos_argparse.py

python $ROOT/lib/atos/python/atoslib/process.py

python $ROOT/lib/atos/python/atoslib/regexp.py

python $ROOT/lib/atos/python/atoslib/gen_argparse.py

python $ROOT/lib/atos/python/atoslib/cc_arguments.py

python $ROOT/lib/atos/python/atoslib/cc_argparse.py
