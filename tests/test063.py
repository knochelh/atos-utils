#!/usr/bin/env python
#
#

import common
import os
import random
import itertools
import re

from atoslib import utils
from atoslib import generators

TEST_CASE = "ATOS generators - simple"

args = common.atos_setup_args(ATOS_DEBUG_FILE="debug.log")

sha1dir = os.path.join(common.SRCDIR, 'examples', 'sha1-c')

status = utils.invoque(
    "atos-init", args, run_script=os.path.join(sha1dir, "run.sh"),
    build_script="gcc -o sha1-c %s %s" % (
        os.path.join(sha1dir, "sha.c"), os.path.join(sha1dir, "sha1.c")))
assert status == 0

def generated_configs(gen, max_iter=None):
    random.seed(0)
    configs = []
    for ic in itertools.count():
        if max_iter != None and ic >= max_iter: break
        try: configs.append(gen.next())
        except StopIteration: break
    return configs

def query_configs(cfg, **kwargs):
    def match(x):
        return all(
            map(lambda (k, v):
                    re.match('^%s$' % v, getattr(x, k, None) or ''),
                    kwargs.items()))
    return filter(match, cfg)


#
#   gen_base
#     gen_base(optim_levels='')
#

gen = generators.gen_base()
cfg = generated_configs(gen)
assert len(cfg) == 1

gen = generators.gen_base(optim_levels='-Os')
cfg = generated_configs(gen)
assert len(cfg) == 1
assert len(query_configs(cfg, flags='-Os')) == 1

gen = generators.gen_base(optim_levels='-Os,-O2')
cfg = generated_configs(gen)
assert len(cfg) == 2
assert len(query_configs(cfg, flags='-Os')) == 1
assert len(query_configs(cfg, flags='-O2')) == 1
assert all(map(lambda x: x.variant == None, cfg))


#
#   gen_flags_file
#     gen_flags_file(flags_file='')
#

try:
    gen = generators.gen_flags_file()
    cfg = generated_configs(gen)
except AssertionError: pass
else: assert 0

try:
    gen = generators.gen_flags_file(flags_file='XXXX')
    cfg = generated_configs(gen)
except AssertionError: pass
else: assert 0

with open('flags1.txt', 'w') as flagsf:
    print >>flagsf, '0 1'
    print >>flagsf, ' 2 3 '
    print >>flagsf, '4 '
    print >>flagsf, ''

gen = generators.gen_flags_file(flags_file='flags1.txt')
cfg = generated_configs(gen)
assert len(cfg) == 3
assert len(query_configs(cfg, flags='0 1')) == 1
assert len(query_configs(cfg, flags='2 3')) == 1
assert len(query_configs(cfg, flags='4')) == 1
assert all(map(lambda x: x.variant == None, cfg))

gen = generators.gen_flags_file(generators.gen_config(flags='9 9'),
                                flags_file='flags1.txt')
cfg = generated_configs(gen)
assert len(cfg) == 3
assert len(query_configs(cfg, flags='9 9 0 1')) == 1
assert len(query_configs(cfg, flags='9 9 2 3')) == 1
assert len(query_configs(cfg, flags='9 9 4')) == 1
assert all(map(lambda x: x.variant == None, cfg))


#
#   gen_rnd_uniform_deps
#     gen_rnd_uniform_deps(flags_files='', optim_levels='')
#

try:
    gen = generators.gen_rnd_uniform_deps()
    cfg = generated_configs(gen)
except AssertionError: pass
else: assert 0

try:
    gen = generators.gen_rnd_uniform_deps(flags_files='XXXX')
    cfg = generated_configs(gen)
except AssertionError: pass
else: assert 0

with open('flags2.txt', 'w') as flagsf:
    print >>flagsf, '-fearly-inlining|-fno-early-inlining'
    print >>flagsf, '--param early-inlining-insns=[5..64]'
    print >>flagsf, '--param max-early-inliner-iterations=[5..20]'
    print >>flagsf, '-finline :: -fearly-inlining'
    print >>flagsf, '-fearly-inlining :: --param early-inlining-insns='
    print >>flagsf, '-fearly-inlining :: --param max-early-inliner-iterations='
    print >>flagsf, '=> -O0'
    print >>flagsf, '-O0 => -fno-inline'
    print >>flagsf, '-O1 => -finline'
    print >>flagsf, '-O2, -Os, -O3 => -fearly-inlining'


gen = generators.gen_rnd_uniform_deps(flags_files='flags2.txt')
cfg = generated_configs(gen, max_iter=5)
assert len(cfg) == 5
assert all(map(lambda x: not x.flags, cfg))
assert all(map(lambda x: x.variant == None, cfg))

gen = generators.gen_rnd_uniform_deps(
    generators.gen_config(flags='-O0'),
    flags_files='flags2.txt')
cfg = generated_configs(gen, max_iter=5)
assert len(cfg) == 5
assert len(query_configs(cfg, flags='-O0')) == 5

gen = generators.gen_rnd_uniform_deps(
    generators.gen_config(flags='-O1'),
    flags_files='flags2.txt')
cfg = generated_configs(gen, max_iter=1000)
assert len(cfg) == 1000
l1 = len(query_configs(cfg, flags='.*max-early-inliner-iterations.*'))
l2 = len(query_configs(cfg, flags='.*early-inlining-insns.*'))
nbmatchesO1 = max(l1, l2)
assert l1 and l2

gen = generators.gen_rnd_uniform_deps(
    generators.gen_config(flags='-O2'),
    flags_files='flags2.txt')
cfg = generated_configs(gen, max_iter=1000)
assert len(cfg) == 1000
assert len(query_configs(cfg, flags='.*max-early-inliner-iterations.*')) > nbmatchesO1
assert len(query_configs(cfg, flags='.*early-inlining-insns.*')) > nbmatchesO1

gen = generators.gen_rnd_uniform_deps(
    flags_files='flags2.txt', optim_levels='-O0', nbiters=1000)
cfg = generated_configs(gen, max_iter=1000)
assert len(cfg) == 1000
assert not len(query_configs(cfg, flags='.*max-early-inliner-iterations.*'))
assert not len(query_configs(cfg, flags='.*early-inlining-insns.*'))

gen = generators.gen_rnd_uniform_deps(
    flags_files='flags2.txt', optim_levels='-O1,-O2,-O3', nbiters=1000)
cfg = generated_configs(gen, max_iter=1000)
assert len(cfg) == 1000
assert len(query_configs(cfg, flags='.*max-early-inliner-iterations.*'))
assert len(query_configs(cfg, flags='.*early-inlining-insns.*'))
assert len(query_configs(cfg, flags='.*fno-early-inlining.*'))
assert len(query_configs(cfg, flags='.*fearly-inlining.*'))

gen = generators.gen_rnd_uniform_deps(
    flags_files='flags2.txt', optim_levels='-O2', nbiters=1000)
cfg = generated_configs(gen, max_iter=1000)
assert len(cfg) == 1000
assert len(query_configs(cfg, flags='-O2.*')) == 1000

