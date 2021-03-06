#
# Copyright (C) STMicroelectronics Ltd. 2012
#
# This file is part of ATOS.
#
# ATOS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# ATOS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# v2.0 along with ATOS. If not, see <http://www.gnu.org/licenses/>.
#

import re, os, sys
import globals
from atos_argparse import ATOSArgumentParser
import argparse

def parser(tool, parser=None):
    """
    Arguments parser factory for the given tool.
    Dispatch to the corresponding per tool factory.
    """
    factories = {
        "atos": parsers.atos,
        "atos-help": parsers.atos_help,
        "atos-audit": parsers.atos_audit,
        "atos-build": parsers.atos_build,
        "atos-deps": parsers.atos_deps,
        "atos-explore": parsers.atos_explore,
        "atos-init": parsers.atos_init,
        "atos-opt": parsers.atos_opt,
        "atos-play": parsers.atos_play,
        "atos-profile": parsers.atos_profile,
        "atos-raudit": parsers.atos_raudit,
        "atos-run": parsers.atos_run,
        "atos-replay": parsers.atos_replay,
        "atos-run-profile": parsers.atos_run_profile,
        "atos-explore-inline": parsers.atos_explore_inline,
        "atos-explore-loop": parsers.atos_explore_loop,
        "atos-explore-optim": parsers.atos_explore_optim,
        "atos-explore-random": parsers.atos_explore_random,
        "atos-explore-acf": parsers.atos_explore_acf,
        "atos-explore-staged": parsers.atos_explore_staged,
        "atos-explore-genetic": parsers.atos_explore_genetic,
        "atos-explore-flag-values": parsers.atos_explore_flag_values,
        "atos-explore-flags-pruning": parsers.atos_explore_flags_pruning,
        "atos-config": parsers.atos_config,
        "atos-cookie": parsers.atos_cookie,
        "atos-lib": parsers.atos_lib,
        "atos-generator": parsers.atos_generator,
        "atos-graph": parsers.atos_graph,
        "atos-web": parsers.atos_web,
        }
    return factories[tool](parser)

class parsers:
    """
    Container namespace for all top level command arguments parser factories.
    One static method per top level tool or atos subcommand.
    Some may take an optional parser argument when used both as top level tool
    or atos subcommand.
    Some may take a required parser argument when used only as atos subcommand.

    For instance, parser = parsers.atos() returns the atos argparser object.
    """

    @staticmethod
    def help_message(help_msg, hidden=False):
        # tuple will be interpreted by atoshelpformatter as a
        # hidden-by-default help message
        if hidden:
            return (help_msg,)
        return help_msg

    @staticmethod
    def update_parser(parser, description):
        parser.description = description
        parser.epilog = (
            "run '%s -h -v' to see all available options." % parser.prog)
        return parser

    @staticmethod
    def add_subparser(sub_parsers, tool, help, hidden=False):
        sub = sub_parsers.add_parser(
            tool, help=parsers.help_message(help, hidden))
        parser("atos-" + tool, parser=sub)

    @staticmethod
    def atos(parser=None):
        """ atos tool arguments parser factory. """
        parser = ATOSArgumentParser(
            prog="atos",
            description="ATOS auto tuning optimization system tool, "
            "see available commands below "
            "or run 'atos help' for the full manual.",
            epilog="Run 'atos -h -v' to see all available commands.")

        args.version(parser)
        subs = parser.add_subparsers(
            title="atos commands",
            dest="subcmd", help="",
            description="See short description of commands below and " +
            "run 'atos COMMAND -h' for each command options.")

        parsers.add_subparser(
            subs, "help",
            help="get full ATOS tools manual")

        parsers.add_subparser(
            subs, "init",
            help="initialize atos environment")

        parsers.add_subparser(
            subs, "opt",
            help="build and run a variant")

        parsers.add_subparser(
            subs, "explore",
            help="exploration of common variants")

        parsers.add_subparser(
            subs, "explore-inline",
            help="exploration of inlining optimizations")

        parsers.add_subparser(
            subs, "explore-loop",
            help="exploration of loop optimizations")

        parsers.add_subparser(
            subs, "explore-optim",
            help="exploration of backend optimizations")

        parsers.add_subparser(
            subs, "explore-random",
            help="exploration of all optimizations")

        parsers.add_subparser(
            subs, "explore-staged",
            help="full staged exploration")

        parsers.add_subparser(
            subs, "explore-genetic",
            help="full genetic exploration")

        parsers.add_subparser(
            subs, "explore-flag-values",
            help="flag values exploration")

        parsers.add_subparser(
            subs, "explore-flags-pruning",
            help="pruning of useless and inefficent flags")

        parsers.add_subparser(
            subs, "explore-acf",
            help="fine grain exploration")

        parsers.add_subparser(
            subs, "play",
            help="play an existing variant")

        parsers.add_subparser(
            subs, "graph",
            help="show exploration results in a graph", hidden=True)

        parsers.add_subparser(
            subs, "build",
            help="build a variant", hidden=True)

        parsers.add_subparser(
            subs, "run",
            help="run a variant", hidden=True)

        parsers.add_subparser(
            subs, "replay",
            help="replay a session", hidden=True)

        parsers.add_subparser(
            subs, "profile",
            help="generate a profile build", hidden=True)

        parsers.add_subparser(
            subs, "run-profile",
            help="run a variant in profile collection mode", hidden=True)

        parsers.add_subparser(
            subs, "audit",
            help=("audit and generate a build "
                  "template to be used by atos-build"), hidden=True)

        parsers.add_subparser(
            subs, "raudit",
            help=("audit and generate a run template "
                  "to be used by atos-build"), hidden=True)

        parsers.add_subparser(
            subs, "deps",
            help="generate the build system from a previous build audit",
            hidden=True)

        parsers.add_subparser(
            subs, "config",
            help="find compilers configuration", hidden=True)

        parsers.add_subparser(
            subs, "cookie",
            help="generate a cookie", hidden=True)

        parsers.add_subparser(
            subs, "generator",
            help="internal API access to ATOS generators", hidden=True)

        parsers.add_subparser(
            subs, "lib",
            help="internal API access to ATOS library", hidden=True)

        parsers.add_subparser(
            subs, "web",
            help="web user interface API", hidden=True)

        return parser

    @staticmethod
    def atos_help(parser=None):
        """ atos-help arguments parser factory. """
        description = (
            "ATOS help tool. get full ATOS tools manual.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-help")
        parsers.update_parser(parser, description=description)
        args.atos_help.topics(parser)
        args.atos_help.text(parser)
        args.atos_help.man(parser)
        args.version(parser, hidden=True)
        return parser

    @staticmethod
    def atos_init(parser=None):
        """ atos init arguments parser factory. """
        description = (
            "ATOS init tool. Environment initialization.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-init")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')
        args.build_script(group)
        args.run_script(group)
        args.results_script(group)
        args.prof_script(group)
        args.nbruns(group)
        args.remote_exec_script(group, hidden=True)
        args.remote_build_script(group, hidden=True)
        args.remote_run_script(group, hidden=True)
        args.remote_path(group, hidden=True)
        args.atos_init.no_run(group)
        args.cookie(group, hidden=True)
        args.jobs(group, hidden=True)
        args.build_jobs(group, hidden=True)
        args.run_jobs(group, hidden=True)
        args.size_cmd(group, hidden=True)
        args.time_cmd(group, hidden=True)
        args.force(group, hidden=True)
        args.legacy(group, hidden=True)
        args.blacklist(group, hidden=True)
        args.reuse(group, hidden=True)
        # audit options
        group = parser.add_argument_group(
            'Audit Options')
        args.exes(group, hidden=True)
        args.ccregexp(group, hidden=True)
        args.ccname(group, hidden=True)
        args.ldregexp(group, hidden=True)
        args.ldname(group, hidden=True)
        args.arregexp(group, hidden=True)
        args.arname(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        # positional arguments
        args.executables(parser)
        # other optional arguments
        args.clean(parser, hidden=True)
        return parser

    @staticmethod
    def atos_opt(parser=None):
        """ atos opt arguments parser factory. """
        description = (
            "ATOS opt tool. build and run a variant.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-opt")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # configuration variant options
        group = parser.add_argument_group(
            'Variant Configuration Options')
        args.options(group)
        args.useprofile(group)
        args.atos_opt.lto(group)
        args.atos_opt.fdo(group)
        args.atos_opt.profile(group)
        # build and run options
        group = parser.add_argument_group(
            'Run Options')
        args.record(group)
        args.remote_path(group, ("-b", "--remote_path"), hidden=True)
        args.nbruns(group, hidden=True)
        args.reuse(group, hidden=True)
        args.cookie(group, hidden=True)
        args.legacy(group, hidden=True)
        args.blacklist(group, hidden=True)
        args.force(group, ("--force",), hidden=True)
        args.jobs(group, hidden=True)
        args.build_jobs(group, hidden=True)
        args.run_jobs(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        return parser

    @staticmethod
    def atos_explore(parser=None):
        """ atos explore arguments parser factory. """
        description = (
            "ATOS explore tool. exploration of common variants.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-explore")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # exploration options
        group = parser.add_argument_group(
            'Exploration Options')
        args.optim_levels(group)
        args.optim_variants(group)
        args.extra_arguments(group, hidden=True)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')
        args.build_script(group)
        args.run_script(group)
        args.results_script(group)
        args.prof_script(group)
        args.nbruns(group)
        args.remote_exec_script(group, hidden=True)
        args.remote_build_script(group, hidden=True)
        args.remote_run_script(group, hidden=True)
        args.remote_path(group, hidden=True)
        args.size_cmd(group, hidden=True)
        args.time_cmd(group, hidden=True)
        args.force(group, hidden=True)
        args.legacy(group, hidden=True)
        args.exes(group, hidden=True)
        args.cookie(group, hidden=True)
        args.reuse(group, hidden=True)
        args.clean(group, hidden=True)
        args.jobs(group, hidden=True)
        args.build_jobs(group, hidden=True)
        args.run_jobs(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        # positional arguments
        args.executables(parser)
        return parser

    @staticmethod
    def atos_explore_inline(parser=None):
        """ atos explore inline arguments parser factory. """
        description = (
            "ATOS explore-inline tool. " +
            "exploration of inlining optimizations.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-explore-inline")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # exploration options
        group = parser.add_argument_group(
            'Exploration Options')
        args.nbiters(group)
        args.optim_levels(group)
        args.optim_variants(group)
        args.seed(group, hidden=True)
        args.flags(group, hidden=True)
        args.extra_arguments(group, hidden=True)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')
        args.cookie(group, hidden=True)
        args.reuse(group, hidden=True)
        args.jobs(group, hidden=True)
        args.build_jobs(group, hidden=True)
        args.run_jobs(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        # positional arguments
        args.base_variants(parser)
        return parser

    @staticmethod
    def atos_explore_loop(parser=None):
        """ atos explore loop arguments parser factory. """
        description = (
            "ATOS explore-loop tool. " +
            "exploration of loop optimizations.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-explore-loop")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # exploration options
        group = parser.add_argument_group(
            'Exploration Options')
        args.nbiters(group)
        args.optim_levels(group)
        args.optim_variants(group)
        args.seed(group, hidden=True)
        args.flags(group, hidden=True)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')
        args.cookie(group, hidden=True)
        args.reuse(group, hidden=True)
        args.jobs(group, hidden=True)
        args.build_jobs(group, hidden=True)
        args.run_jobs(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        # positional arguments
        args.base_variants(parser)
        return parser

    @staticmethod
    def atos_explore_optim(parser=None):
        """ atos explore optim arguments parser factory. """
        description = (
            "ATOS explore-optim tool. " +
            "exploration of backend optimizations.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-explore-optim")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # exploration options
        group = parser.add_argument_group(
            'Exploration Options')
        args.nbiters(group)
        args.optim_levels(group)
        args.optim_variants(group)
        args.seed(group, hidden=True)
        args.flags(group, hidden=True)
        args.extra_arguments(group, hidden=True)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')
        args.cookie(group, hidden=True)
        args.reuse(group, hidden=True)
        args.jobs(group, hidden=True)
        args.build_jobs(group, hidden=True)
        args.run_jobs(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        # positional arguments
        args.base_variants(parser)
        return parser

    @staticmethod
    def atos_explore_random(parser=None):
        """ atos explore random arguments parser factory. """
        description = (
            "ATOS explore-random tool. " +
            "exploration of all optimizations.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-explore-random")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # exploration options
        group = parser.add_argument_group(
            'Exploration Options')
        args.nbiters(group)
        args.optim_levels(group)
        args.optim_variants(group)
        args.seed(group, hidden=True)
        args.atos_explore.weight_class(group)
        args.flags(group, hidden=True)
        args.extra_arguments(group, hidden=True)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')
        args.cookie(group, hidden=True)
        args.reuse(group, hidden=True)
        args.jobs(group, hidden=True)
        args.build_jobs(group, hidden=True)
        args.run_jobs(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        # positional arguments
        args.base_variants(parser)
        return parser

    @staticmethod
    def atos_explore_staged(parser=None):
        """ atos explore staged arguments parser factory. """
        description = (
            "ATOS explore-staged tool. " +
            "full staged exploration.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-explore-staged")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # exploration options
        group = parser.add_argument_group(
            'Exploration Options')
        args.nbiters(group)
        args.tradeoffs(group)
        args.optim_levels(group)
        args.optim_variants(group)
        args.seed(group, hidden=True)
        args.atos_explore.weight_class(group)
        args.flags(group, hidden=True)
        args.atos_explore.pruning(group)
        args.atos_explore.update_ref(group, hidden=True)
        args.atos_explore.threshold(group, hidden=True)
        args.atos_explore.keep_opt_level(group, hidden=True)
        args.extra_arguments(group, hidden=True)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')  # hide this group?
        args.build_script(group)
        args.run_script(group)
        args.results_script(group)
        args.prof_script(group)
        args.nbruns(group)
        args.remote_path(group, hidden=True)
        args.cookie(group, hidden=True)
        args.size_cmd(group, hidden=True)
        args.time_cmd(group, hidden=True)
        args.force(group, hidden=True)
        args.legacy(group, hidden=True)
        args.reuse(group, hidden=True)
        args.jobs(group, hidden=True)
        args.build_jobs(group, hidden=True)
        args.run_jobs(group, hidden=True)
        args.exes(group, hidden=True)
        args.clean(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        # positional arguments
        args.base_variants(parser)
        return parser

    @staticmethod
    def atos_explore_genetic(parser=None):
        """ atos explore genetic arguments parser factory. """
        description = (
            "ATOS explore-genetic tool. " +
            "full genetic exploration.")
        if parser == None:
            parser = ATOSArgumentParser(
                prog="atos-explore-genetic")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # exploration options
        group = parser.add_argument_group(
            'Exploration Options')
        args.nbiters(group)
        args.tradeoffs(group)
        args.optim_levels(group)
        args.optim_variants(group)
        args.atos_explore.generations(group)
        args.atos_explore.mutate_prob(group)
        args.atos_explore.mutate_rate(group)
        args.atos_explore.mutate_remove(group)
        args.atos_explore.evolve_rate(group)
        args.atos_explore.nbpoints(group)
        args.atos_explore.weight_class(group)
        args.atos_explore.flags(group, hidden=True)
        args.seed(group, hidden=True)
        args.atos_explore.pruning(group)
        args.atos_explore.update_ref(group, hidden=True)
        args.atos_explore.threshold(group, hidden=True)
        args.atos_explore.keep_opt_level(group, hidden=True)
        args.extra_arguments(group, hidden=True)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')  # hide this group?
        args.build_script(group)
        args.run_script(group)
        args.results_script(group)
        args.prof_script(group)
        args.nbruns(group)
        args.remote_path(group, hidden=True)
        args.cookie(group, hidden=True)
        args.size_cmd(group, hidden=True)
        args.time_cmd(group, hidden=True)
        args.force(group, hidden=True)
        args.legacy(group, hidden=True)
        args.reuse(group, hidden=True)
        args.jobs(group, hidden=True)
        args.build_jobs(group, hidden=True)
        args.run_jobs(group, hidden=True)
        args.exes(group, hidden=True)
        args.clean(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        # positional arguments
        args.base_variants(parser)
        return parser

    @staticmethod
    def atos_explore_flag_values(parser=None):
        """ atos explore flag values arguments parser factory. """
        description = (
            "ATOS explore-flag-values tool. " +
            "flag values exploration.")
        if parser == None:
            parser = ATOSArgumentParser(
                prog="atos-explore-flag-values")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # exploration options
        group = parser.add_argument_group(
            'Exploration Options')
        args.atos_explore.variant_id(group)
        args.atos_explore.nb_values(group)
        args.atos_explore.try_removing(group)
        args.tradeoffs(group)
        args.optim_levels(group)
        args.optim_variants(group)
        args.seed(group, hidden=True)
        args.extra_arguments(group, hidden=True)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')  # hide this group?
        args.build_script(group)
        args.run_script(group)
        args.results_script(group)
        args.prof_script(group)
        args.nbruns(group)
        args.remote_path(group, hidden=True)
        args.cookie(group, hidden=True)
        args.size_cmd(group, hidden=True)
        args.time_cmd(group, hidden=True)
        args.force(group, hidden=True)
        args.legacy(group, hidden=True)
        args.reuse(group, hidden=True)
        args.jobs(group, hidden=True)
        args.build_jobs(group, hidden=True)
        args.run_jobs(group, hidden=True)
        args.exes(group, hidden=True)
        args.clean(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        return parser

    @staticmethod
    def atos_explore_flags_pruning(parser=None):
        """ atos explore flag values arguments parser factory. """
        description = (
            "ATOS explore-flags-pruning tool. " +
            "pruning of useless and inefficent flags.")
        if parser == None:
            parser = ATOSArgumentParser(
                prog="atos-explore-flags-pruning")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # exploration options
        group = parser.add_argument_group(
            'Exploration Options')
        args.atos_explore.variant_id(group)
        args.atos_explore.threshold(group)
        args.atos_explore.tradeoff(group)
        args.atos_explore.update_ref(group)
        args.atos_explore.keep_opt_level(group)
        args.seed(group, hidden=True)
        args.extra_arguments(group, hidden=True)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')  # hide this group?
        args.build_script(group)
        args.run_script(group)
        args.results_script(group)
        args.prof_script(group)
        args.nbruns(group)
        args.remote_path(group, hidden=True)
        args.cookie(group, hidden=True)
        args.size_cmd(group, hidden=True)
        args.time_cmd(group, hidden=True)
        args.force(group, hidden=True)
        args.legacy(group, hidden=True)
        args.reuse(group, hidden=True)
        args.jobs(group, hidden=True)
        args.build_jobs(group, hidden=True)
        args.run_jobs(group, hidden=True)
        args.exes(group, hidden=True)
        args.clean(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        return parser

    @staticmethod
    def atos_explore_acf(parser=None):
        """ atos explore acf arguments parser factory. """
        description = (
            "ATOS explore-acf tool. " +
            "fine grain exploration.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-explore-acf")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # exploration options
        group = parser.add_argument_group(
            'Exploration Options')
        args.atos_explore.file_by_file(group)
        args.per_func_nbiters(group)
        args.atos_explore.hot_threshold(group)
        args.atos_explore.cold_options(group)
        args.atos_explore.cold_attributes(group)
        args.atos_explore.genetic(group)
        args.atos_explore.generations(group, hidden=True)
        args.atos_explore.random(group)
        args.tradeoffs(group)
        args.optim_levels(group)
        args.optim_variants(group)
        args.seed(group, hidden=True)
        args.flags(group, hidden=True)
        args.extra_arguments(group, hidden=True)
        # build and run options
        group = parser.add_argument_group(
            'Profile and Run Options')
        args.prof_script(group)
        args.exes(group, hidden=True)
        args.cookie(group, hidden=True)
        args.reuse(group, hidden=True)
        args.jobs(group, hidden=True)
        args.build_jobs(group, hidden=True)
        args.run_jobs(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        # positional arguments
        args.base_variants(parser)
        return parser

    @staticmethod
    def atos_play(parser=None):
        """ atos play arguments parser factory. """
        description = (
            "ATOS play tool. play an existing variant.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-play")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # objective options
        group = parser.add_argument_group(
            'Selection Options')
        group_ex = group.add_mutually_exclusive_group()
        args.atos_play.objective(group_ex)
        args.tradeoffs(group_ex)
        args.atos_play.nbpoints(group)
        args.atos_play.ref(group, ("--ref",))
        args.atos_play.localid(group)
        args.variant(group)
        args.id(group)
        args.options(group)
        args.targets(group, ("--targets",))
        args.refid(group)
        args.query(group, ("--query",))
        args.atos_graph.cookie(group)
        args.atos_graph.filter(group, ("--filter",))
        # objective options
        group = parser.add_argument_group(
            'Output Options')
        group_ex = group.add_mutually_exclusive_group()
        args.atos_play.printconfig(group_ex)
        args.atos_play.printvariant(group_ex)
        args.atos_play.printtable(group_ex)
        args.atos_play.reverse(group)
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, hidden=True)
        args.version(group, hidden=True)
        # positional arguments
        args.command(parser)
        return parser

    @staticmethod
    def atos_graph(parser=None):
        """ atos graph arguments parser factory. """
        description = (
            "ATOS graph tool. show exploration results.")
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(prog="atos-graph")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        args.atos_graph.configuration_pathes(group)
        # configuration options
        group = parser.add_argument_group(
            'Graph Options')
        args.atos_graph.correl(group)
        args.atos_graph.heat(group)
        args.tradeoffs(group)
        args.atos_graph.highlight(group)
        args.atos_graph.frontier(group)
        args.atos_graph.xd(group)
        args.atos_graph.anonymous(group)
        args.atos_graph.labels(group)
        args.id(group)
        args.atos_graph.xlim(group)
        args.atos_graph.ylim(group)
        # objective options
        group = parser.add_argument_group(
            'Selection Options')
        args.targets(group)
        args.refid(group)
        args.atos_graph.filter(group)
        args.query(group)
        args.atos_graph.cookie(group)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.dryrun(group, hidden=True)
        args.version(group, hidden=True)
        # other optional arguments
        args.atos_graph.outfile(parser)
        args.atos_graph.hide(parser)
        args.atos_graph.follow(parser)
        # positional argument
        args.atos_graph.dbfile(parser)
        return parser

    @staticmethod
    def atos_build(parser=None):
        """ atos build arguments parser factory. """
        description = (
            "ATOS build tool. build a variant.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-build")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # configuration variant options
        group = parser.add_argument_group(
            'Variant Configuration Options')
        args.options(group)
        group_ex = group.add_mutually_exclusive_group()
        args.genprofile(group_ex)
        args.useprofile(group_ex)
        # audit options
        group = parser.add_argument_group(
            'Build Options')
        args.ccregexp(group, hidden=True)
        args.ccname(group, hidden=True)
        args.ldregexp(group, hidden=True)
        args.ldname(group, hidden=True)
        args.arregexp(group, hidden=True)
        args.arname(group, hidden=True)
        args.remote_path(group, ("-b", "--remote_path"), hidden=True)
        args.path(group, hidden=True)
        args.jobs(group, hidden=True)
        args.legacy(group, hidden=True)
        args.blacklist(group, hidden=True)
        args.force(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, hidden=True)
        args.version(group, hidden=True)
        # other options
        args.command(parser)
        args.variant(parser, hidden=True)
        args.internal_flags.local(parser)
        return parser

    @staticmethod
    def atos_run(parser=None):
        """ atos run arguments parser factory. """
        description = (
            "ATOS run tool. run a variant.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-run")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')
        args.command(group)
        args.options(group)
        prof_group = group.add_mutually_exclusive_group()
        args.useprofile(prof_group)
        args.genprofile(prof_group)
        args.nbruns(group)
        args.remote_path(group, ("-b", "--remote_path"), hidden=True)
        args.results_script(group)
        args.size_cmd(group, hidden=True)
        args.time_cmd(group, hidden=True)
        args.record(group)
        args.cookie(group, hidden=True)
        args.run_jobs(group, hidden=True)
        args.reuse(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        # other options
        args.atos_run.silent(parser)
        args.variant(parser, hidden=True)
        args.output(parser, hidden=True)
        args.id(parser, hidden=True)
        args.internal_flags.local(parser)
        args.internal_flags.hashsum(parser)
        return parser

    @staticmethod
    def atos_replay(parser=None):
        """ atos replay arguments parser factory. """
        description = (
            "ATOS explore-replay tool. replay a session.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-replay")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        args.atos_replay.results_path(group)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')
        args.run_script(group)
        args.results_script(group)
        args.nbruns(group)
        args.cookie(group, hidden=True)
        args.atos_replay.no_ref(group)
        args.size_cmd(group, hidden=True)
        args.time_cmd(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, ("--dryrun",), hidden=True)
        args.version(group, hidden=True)
        # positional arguments
        args.atos_replay.variants(parser)
        return parser

    @staticmethod
    def atos_profile(parser=None):
        """ atos profile arguments parser factory. """
        description = (
            "ATOS profile generation tool. " +
            "generate a profile build.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-profile")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        group = parser.add_argument_group(
            'Profile Options')
        args.remote_path(group, ("-b", "--remote_path"), hidden=True)
        args.options(group, ("-g", "--options"))
        args.path(group, hidden=True)
        args.legacy(group, hidden=True)
        args.force(group, hidden=True)
        args.reuse(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, hidden=True)
        args.version(group, hidden=True)
        return parser

    @staticmethod
    def atos_run_profile(parser=None):
        """ atos run profile arguments parser factory. """
        description = (
            "ATOS run profile tool. " +
            "run a variant in profile collection mode.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-run-profile")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # build and run options
        group = parser.add_argument_group(
            'Build and Run Options')
        args.command(group)
        args.options(group)
        prof_group = group.add_mutually_exclusive_group()
        args.useprofile(prof_group)
        args.genprofile(prof_group)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, hidden=True)
        args.version(group, hidden=True)
        return parser

    @staticmethod
    def atos_audit(parser=None):
        """ atos audit arguments parser factory. """
        description = (
            "ATOS audit tool. audit and generate a build template" +
            "to be used by atos-build.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-audit")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # audit options
        group = parser.add_argument_group(
            'Audit Options')
        args.ccregexp(group, hidden=True)
        args.ccname(group, hidden=True)
        args.ldregexp(group, hidden=True)
        args.ldname(group, hidden=True)
        args.arregexp(group, hidden=True)
        args.arname(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, hidden=True)
        args.version(group, hidden=True)
        # other options
        args.command(parser)
        args.output(parser, default="build.audit", hidden=True)
        args.legacy(group, hidden=True)
        args.force(group, hidden=True)
        return parser

    @staticmethod
    def atos_raudit(parser=None):
        """ atos raudit arguments parser factory. """
        description = (
            "ATOS raudit tool. " +
            "audit and generate a run template to be used by atos-run.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-raudit")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # build and run options
        group = parser.add_argument_group(
            'Run and results Options')
        args.results_script(group)
        args.size_cmd(group, hidden=True)
        args.time_cmd(group, hidden=True)
        args.force(group, hidden=True)
        args.legacy(group, hidden=True)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, hidden=True)
        args.version(group, hidden=True)
        # other options
        args.command(parser)
        args.output(parser, default="run.audit", hidden=True)
        return parser

    @staticmethod
    def atos_deps(parser=None):
        """ atos dep arguments parser factory. """
        description = (
            "ATOS dependency and build system generation tool. " +
            "generate the build system from a previous build audit.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-deps")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, hidden=True)
        args.version(group, hidden=True)
        # other options
        args.executables(parser)
        args.exes(group, hidden=True)
        args.atos_deps.input(parser)
        args.output(parser, default="build.mk", hidden=True)
        args.atos_deps.last(parser)
        args.atos_deps.all(parser)
        args.legacy(group, hidden=True)
        args.force(group, hidden=True)
        return parser

    @staticmethod
    def atos_config(parser=None):
        """ atos config arguments parser factory. """
        description = (
            "ATOS config generator. find compilers configuration.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-config")
        parsers.update_parser(parser, description=description)
        args.configuration_path(parser)
        args.atos_config.compiler(parser)
        args.atos_config.printcfg(parser)
        args.atos_config.ppflags(parser)
        args.debug(parser, hidden=True)
        args.version(parser, hidden=True)
        return parser

    @staticmethod
    def atos_cookie(parser=None):
        """ atos cookie arguments parser factory. """
        description = (
            "ATOS cookie generator. generate a cookie.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-cookie")
        parsers.update_parser(parser, description=description)
        args.cookie(parser, hidden=False)
        args.version(parser, hidden=True)
        return parser

    @staticmethod
    def atos_generator(parser=None):
        """ atos gen arguments parser factory. """
        description = (
            "ATOS gen tool. internal API access to ATOS generators.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-generator")
        parsers.update_parser(parser, description=description)
        # configuration options
        group = parser.add_argument_group(
            'Configuration Options')
        args.configuration_path(group)
        # exploration options
        group = parser.add_argument_group(
            'Exploration Options')
        args.atos_generator.generator(group)
        args.base_variants(group)
        args.tradeoffs(group)
        args.optim_levels(group)
        args.optim_variants(group)
        args.nbiters(group)
        args.per_func_nbiters(group)
        args.seed(group, hidden=True)
        args.extra_arguments(group)
        # misc options
        group = parser.add_argument_group(
            'Misc Options')
        args.debug(group, hidden=True)
        args.log_file(group, hidden=True)
        args.quiet(group, hidden=True)
        args.dryrun(group, hidden=True)
        args.version(group, hidden=True)
        # other options
        args.cookie(group, hidden=True)
        args.reuse(group, hidden=True)
        return parser

    @staticmethod
    def atos_lib(parser=None):
        """ atos lib arguments parser factory. """
        description = (
            "ATOS lib tool. internal API access to ATOS library.")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-lib")
        parsers.update_parser(parser, description=description)
        subs = parser.add_subparsers(
            title="atos lib commands",
            dest="subcmd_lib",
            description="see short description of commands below and " +
            "run 'atos lib COMMAND -h' for each command options",
            help="available atos lib commands")
        sub = subs.add_parser("create_db", help="Create a new empty database")
        parsers.atos_lib_createdb(sub)
        sub = subs.add_parser(
            "query", help="Query database results")
        parsers.atos_lib_query(sub)
        sub = subs.add_parser("speedups", help="Get results")
        parsers.atos_lib_speedups(sub)
        sub = subs.add_parser(
            "push", help="Export results to another database")
        parsers.atos_lib_push(sub)
        sub = subs.add_parser(
            "pull", help="Import results from another database")
        parsers.atos_lib_pull(sub)
        sub = subs.add_parser(
            "report", help="Print results")
        parsers.atos_lib_report(sub)
        sub = subs.add_parser(
            "add_result", help="Add result to database")
        parsers.atos_lib_addresult(sub)
        sub = subs.add_parser(
            "config", help="Compiler configuration")
        parsers.atos_lib_config(sub)
        return parser

    @staticmethod
    def atos_web(parser=None):
        """ atos web arguments parser factory. """
        description = (
                "ATOS web tool. web user interface API")
        if parser == None:
            parser = ATOSArgumentParser(prog="atos-web")
        parsers.update_parser(parser, description=description)
        args.atos_web.server(parser)
        args.version(parser, hidden=True)
        subs = parser.add_subparsers(
            title="atos web commands",
            dest="subcmd_web",
            description="see short description of commands below",
            help="available atos web commands")
        sub = subs.add_parser("project", help="Manage projects")
        parsers.atos_web_project(sub)
        sub = subs.add_parser("experiment", help="Manage experiments")
        parsers.atos_web_experiment(sub)
        sub = subs.add_parser("cookie", help="Manage cookies")
        parsers.atos_web_cookie(sub)
        sub = subs.add_parser("target", help="Manage targets")
        parsers.atos_web_target(sub)
        sub = subs.add_parser("run", help="Manage runs")
        parsers.atos_web_run(sub)
        return parser

    @staticmethod
    def atos_lib_createdb(parser=None):
        """ atos lib createdb arguments parser factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(
                prog="atos-lib-createdb",
                description="Create a new empty database")
        args.configuration_path(parser)
        args.atos_lib.type(parser)
        args.atos_lib.shared(parser)
        return parser

    @staticmethod
    def atos_lib_query(parser=None):
        """ atos lib query arguments parser factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(
                prog="atos-lib-query",
                description="Query database results")
        args.configuration_path(parser)
        args.query(parser)
        args.atos_lib.text(parser)
        return parser

    @staticmethod
    def atos_lib_speedups(parser=None):
        """ atos lib speedups arguments parser factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(prog="atos-lib-speedups",
                                        description="ATOS lib tool")
        args.configuration_path(parser)
        args.tradeoffs(parser)
        args.cookie(parser)
        args.query(parser)
        args.targets(parser)
        args.atos_lib.groupname(parser)
        args.refid(parser)
        args.atos_lib.frontier(parser)
        args.atos_lib.table(parser)
        args.atos_lib.reverse(parser)
        return parser

    @staticmethod
    def atos_lib_push(parser=None):
        """ atos lib push arguments parser factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(prog="atos-lib-push",
                                        description="ATOS lib tool")
        args.configuration_path(parser, ("-C", "--C1"))
        args.atos_lib.remote_configuration_path(parser)
        args.query(parser)
        args.atos_lib.replacement(parser)
        args.force(parser)
        return parser

    @staticmethod
    def atos_lib_pull(parser=None):
        """ atos lib pull arguments parser factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(prog="atos-lib-pull",
                                        description="ATOS lib tool")
        args.configuration_path(parser, ("-C", "--C1"))
        args.atos_lib.remote_configuration_path(parser)
        args.query(parser)
        args.atos_lib.replacement(parser)
        args.force(parser)
        return parser

    @staticmethod
    def atos_lib_report(parser=None):
        """ atos lib report arguments parser factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(prog="atos-lib-report",
                                        description="ATOS lib tool")
        args.configuration_path(parser)
        args.targets(parser)
        args.query(parser)
        args.refid(parser)
        args.atos_lib.reverse(parser)
        args.atos_lib.mode(parser)
        args.atos_lib.variants(parser)
        return parser

    @staticmethod
    def atos_lib_addresult(parser=None):
        """ atos lib add_result arguments parser factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(prog="atos-lib-add_result",
                                        description="ATOS lib tool")
        args.configuration_path(parser)
        args.atos_lib.result(parser)
        return parser

    @staticmethod
    def atos_lib_config(parser=None):
        """ atos lib config arguments parser factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(prog="atos-lib-config",
                                        description="ATOS lib tool")
        args.configuration_path(parser)
        args.query(parser)
        args.atos_lib.text(parser)
        args.atos_lib.uniq(parser)
        args.atos_lib.additem(parser)
        args.atos_lib.getitem(parser)
        args.atos_lib.addcpl(parser)
        args.atos_lib.cplflags(parser)
        return parser

    @staticmethod
    def atos_web_project(parser=None):
        """ atos web project arguments parser factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(
                prog="atos-web-project",
                description="Manage web projects")
        args.atos_web.operation(parser)
        return parser

    @staticmethod
    def atos_web_experiment(parser=None):
        """ atos web experiment arguments parser factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(
                prog="atos-web-experiment",
                description="Manage web experiments")
        args.atos_web.operation(parser)
        args.atos_web.project(parser)
        return parser

    @staticmethod
    def atos_web_cookie(parser=None):
        """ atos web cookie arguments parser factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(
                prog="atos-web-cookie",
                description="Manage web cookies")
        args.atos_web.project(parser)
        args.atos_web.experiment(parser)
        args.configuration_path(parser)
        return parser

    @staticmethod
    def atos_web_target(parser=None):
        """ atos web target arguments parser factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(
                prog="atos-web-target",
                description="Manage web targets")
        args.atos_web.operation(parser)
        args.atos_web.project(parser)
        args.atos_web.experiment(parser)
        return parser

    @staticmethod
    def atos_web_run(parser=None):
        """ atos web run argument parsers factory. """
        if parser == None:  # pragma: uncovered
            parser = ATOSArgumentParser(
                prog="atos-web-run",
                description="Manage web runs")
        args.atos_web.operation(parser)
        args.atos_web.project(parser)
        args.atos_web.experiment(parser)
        args.atos_web.target(parser)
        args.configuration_path(parser)

        return parser

class args:
    """
    Container namespace for single options declarators.
    One staticmethod per single option here with the long option
    name, whatever the tool.
    Each method defines a default short and long option string that
    can be overriden in case of conflicts with a tuple of option
    strings passed to the args parameter.
    Some additional methods may group common options.

    For instance, args.version(parser) declare the --version option.
    """

    @staticmethod
    def version(parser, args=("-v", "--version"), hidden=False):
        help_msg = parsers.help_message(
            "output version string", hidden)
        parser.add_argument(
            *args,
             help=help_msg,
             action="version",
             version="atos version " + globals.VERSION)

    @staticmethod
    def quiet(parser, args=("-q", "--quiet"), hidden=False):
        help_msg = parsers.help_message(
            "quiet output", hidden)
        parser.add_argument(
            *args,
             help=help_msg,
             action="store_true")

    @staticmethod
    def dryrun(parser, args=("-n", "--dryrun"), hidden=False):
        help_msg = parsers.help_message(
            "dry run, output commands only", hidden)
        parser.add_argument(
            *args,
             help=help_msg,
             action="store_true")

    @staticmethod
    def configuration_path(parser, args=("-C", "--configuration")):
        parser.add_argument(
            *args,
             dest="configuration_path",
             help="atos configuration working directory",
             default=globals.DEFAULT_CONFIGURATION_PATH)

    @staticmethod
    def legacy(parser, args=("--legacy",), hidden=False):
        help_msg = parsers.help_message(
            "use legacy scheme for audit and exploration", hidden)
        parser.add_argument(
            *args,
             action="store_true",
             help=help_msg)

    @staticmethod
    def blacklist(parser, args=("--blacklist",), hidden=False):
        help_msg = parsers.help_message(
            "initialize the objects blacklist automatically", hidden)
        parser.add_argument(
            *args,
             action="store_true",
             help=help_msg)

    @staticmethod
    def force(parser, args=("-f", "--force"), hidden=False):
        help_msg = parsers.help_message(
            "use atos tools in force rebuild mode, "
            "the full build command will be re-executed", hidden)
        parser.add_argument(
            *args,
             action="store_true",
             help=help_msg)

    @staticmethod
    def build_script(parser, args=("-b", "--build-script")):
        parser.add_argument(
            *args,
             dest="build_script",
             help="build_script to be audited and optimized")

    @staticmethod
    def ccregexp(parser, args=("--ccregexp",), hidden=False):
        help_msg = parsers.help_message(
            "specify the compiler tools basename regexp", hidden)
        parser.add_argument(
            *args,
             dest="ccregexp",
             help=help_msg,
             default=globals.DEFAULT_CCREGEXP)

    @staticmethod
    def ccname(parser, args=("--ccname",), hidden=False):
        help_msg = parsers.help_message(
            "specify the compiler basename, default to CCREGEXP",
            hidden)
        parser.add_argument(
            *args,
             dest="ccname",
             help=help_msg)

    @staticmethod
    def ldregexp(parser, args=("--ldregexp",), hidden=False):
        help_msg = parsers.help_message(
            "specify the linker tools basename regexp", hidden)
        parser.add_argument(
            *args,
             dest="ldregexp",
             help=help_msg,
             default=globals.DEFAULT_LDREGEXP)

    @staticmethod
    def ldname(parser, args=("--ldname",), hidden=False):
        help_msg = parsers.help_message(
            "specify the linker basename, defaults to LDREGEXP", hidden)
        parser.add_argument(
            *args,
             dest="ldname",
             help=help_msg)

    @staticmethod
    def arregexp(parser, args=("--arregexp",), hidden=False):
        help_msg = parsers.help_message(
            "specify the archivers basename regexp", hidden)
        parser.add_argument(
            *args,
             dest="arregexp",
             help=help_msg,
             default=globals.DEFAULT_ARREGEXP)

    @staticmethod
    def arname(parser, args=("--arname",), hidden=False):
        help_msg = parsers.help_message(
            "specify the archiver basename, defaults to ARREGEXP",
            hidden)
        parser.add_argument(
            *args,
             dest="arname",
             help=help_msg)

    @staticmethod
    def path(parser, args=("-p", "--path"), hidden=True):
        help_msg = parsers.help_message(
            "path to profile files", hidden)
        parser.add_argument(
            *args,
             dest="path",
             help=help_msg)

    @staticmethod
    def remote_path(parser, args=("-B", "--remote_path"), hidden=False):
        help_msg = parsers.help_message(
                "remote path to profile files for cross execution", hidden)
        parser.add_argument(
            *args,
            dest="remote_path",
            help=help_msg)

    @staticmethod
    def run_script(parser, args=("-r", "--run-script")):
        parser.add_argument(
            *args,
             dest="run_script",
             help="run_script to be audited and optimized")

    @staticmethod
    def nbruns(parser, default=None, args=("-n", "--nbruns"), hidden=False):
        help_msg = parsers.help_message(
            "number of executions of <run_script>", hidden)
        parser.add_argument(
            *args,
             dest="nbruns",
             type=int,
             help=help_msg,
             default=default)

    @staticmethod
    def results_script(parser, args=("-t", "--results-script")):
        parser.add_argument(
            *args,
             dest="results_script",
             help="results_script for specific instrumentation")

    @staticmethod
    def size_cmd(parser, hidden=False):
        help_msg = parsers.help_message(
            "if specified, overrides bintutils size command "
            "[default: %s]" % globals.DEFAULT_SIZE_CMD, hidden)
        parser.add_argument(
            "--size-cmd",
             dest="size_cmd",
             help=help_msg)

    @staticmethod
    def time_cmd(parser, hidden=False):
        help_msg = parsers.help_message(
            "if specified, overrides posix time command "
            "[default: %s]" % globals.DEFAULT_TIME_CMD, hidden)
        parser.add_argument(
            "--time-cmd",
             dest="time_cmd",
             help=help_msg)

    @staticmethod
    def clean(parser, args=("-c", "--clean"), hidden=False):
        help_msg = parsers.help_message(
            "clean results and profiles before exploration", hidden)
        parser.add_argument(
            *args,
             dest="clean",
             help=help_msg,
             action="store_true")

    @staticmethod
    def debug(parser, args=("-d", "--debug"), hidden=False):
        help_msg = parsers.help_message(
            "debug mode", hidden)
        parser.add_argument(
            *args,
             dest="debug",
             help=help_msg,
             action="store_true")

    @staticmethod
    def log_file(parser, args=("--log-file",), hidden=False):
        help_msg = parsers.help_message(
            "log file for debug mode, defaults to stderr", hidden)
        parser.add_argument(
            *args,
             dest="log_file",
             help=help_msg)

    @staticmethod
    def exes(parser, args=("-e", "--executables"), hidden=False):
        help_msg = parsers.help_message(
            "executables to be instrumented, "
            "defaults to args of command or all generated executables", hidden)
        parser.add_argument(
            *args,
             dest="exes",
             help=help_msg)

    @staticmethod
    def id(parser, args=("-i", "--identifier"), hidden=False):
        help_msg = parsers.help_message(
            "identifier of run [default: executables basename]", hidden)
        parser.add_argument(
            *args,
            dest="id",
            help=help_msg)

    @staticmethod
    def options(parser, args=("-a", "--options")):
        parser.add_argument(
            *args,
            dest="options",
            help="append given options to the compilation commands")

    @staticmethod
    def output(parser, default="None", args=("-o", "--output"), hidden=False):
        help_msg = parsers.help_message(
            "output description file, defaults to CONFIGURATION_PATH/"
            + default, hidden)
        parser.add_argument(
            *args,
             dest="output_file",
             help=help_msg)

    @staticmethod
    def useprofile(parser, args=("-u", "--useprof")):
        parser.add_argument(*args,
                            dest="uopts",
                            help="use profile variant deduced by UOPTS")

    @staticmethod
    def genprofile(parser, args=("-g", "--genprof")):
        parser.add_argument(
            *args,
             dest="gopts",
             help="generate profile variant deduced by GOPTS")

    @staticmethod
    def record(parser, args=("-r", "--record")):
        parser.add_argument(*args,
                             dest="record",
                             action='store_true',
                             help="record results")

    @staticmethod
    def cookie(parser, args=("--cookie",), hidden=False):
        help_msg = parsers.help_message(
            "use to identify results",
            hidden)
        parser.add_argument(
            *args,
             dest="cookies",
             action='append',
             help=help_msg)

    @staticmethod
    def tradeoffs(parser, args=("-s", "--tradeoffs")):
        parser.add_argument(*args,
                             dest="tradeoffs",
                             action='append',
                             type=float,
                             help="selected tradeoff given size/perf ratio")

    @staticmethod
    def variant(parser, args=("-w", "--variant"), hidden=False):
        help_msg = parsers.help_message(
            "identifier of variant",
            hidden)
        parser.add_argument(
            *args,
             dest="variant",
             help=help_msg)

    @staticmethod
    def seed(parser, args=("-S", "--seed"), hidden=False):
        help_msg = parsers.help_message(
            "seed for random generator",
            hidden)
        parser.add_argument(
            *args,
             dest="seed",
             help=help_msg,
             default=0)

    @staticmethod
    def nbiters(parser, args=("-M", "--nbiters")):
        parser.add_argument(
            *args,
             dest="nbiters",
             type=int,
             help="number of iterations for per target exploration",
             default=100)

    @staticmethod
    def per_func_nbiters(parser, args=("-N", "--per-func-nbiters")):
        parser.add_argument(
            *args,
             dest="per_func_nbiters",
             type=int,
             help="number of exploration for per function/file exploration",
             default=None)

    @staticmethod
    def flags(parser, args=("-F", "--flags"), hidden=False):
        help_msg = parsers.help_message(
            "flags list filename",
            hidden)
        parser.add_argument(
            *args,
             dest="flags_file",
             help=help_msg,
             default=None)

    @staticmethod
    def optim_levels(parser, args=("--optim-levels",)):
        parser.add_argument(
            *args,
             dest="optim_levels",
             help="list of optimization levels",
             default="-Os,-O2,-O3")

    @staticmethod
    def optim_variants(parser, args=("-V", "--optim-variants")):
        parser.add_argument(
            *args,
             dest="optim_variants",
             help="list of optimization variants, defaults to all"
             " available variants",
             default=None)

    @staticmethod
    def base_variants(parser):
        parser.add_argument(
            "base_variants",
            nargs=argparse.REMAINDER,
            help="identifiers of variants"
            " on which the exploration will be based")

    @staticmethod
    def executables(parser):
        parser.add_argument(
            "executables",
            nargs=argparse.REMAINDER,
            help="default executables list to optimize")

    @staticmethod
    def command(parser):
        parser.add_argument(
            "command",
            nargs=argparse.REMAINDER,
            help="command to be executed")

    @staticmethod
    def prof_script(parser, args=("-p", "--profile-script")):
        parser.add_argument(*args,
                             dest="prof_script",
                             help="script to get profile information")

    @staticmethod
    def reuse(parser, args=("--reuse",), hidden=False):
        help_msg = parsers.help_message(
            "reuse existing results",
            hidden)
        parser.add_argument(
            *args,
             dest="reuse",
             action='store_true',
             help=help_msg)

    @staticmethod
    def jobs(parser, args=("-j", "--jobs"), hidden=False):
        help_msg = parsers.help_message(
            "use JOBS parallel thread when possible for building",
            hidden)
        parser.add_argument(
            *args,
             dest="jobs",
             type=int,
             help=help_msg,
             default=globals.DEFAULT_BUILD_JOBS)

    @staticmethod
    def build_jobs(parser, args=("--build-jobs",), hidden=False):
        help_msg = parsers.help_message(
            "execute BUILD-JOBS parallel build threads",
            hidden)
        parser.add_argument(
            *args,
             dest="build_jobs",
             type=int,
             help=help_msg)

    @staticmethod
    def run_jobs(parser, args=("--run-jobs",), hidden=False):
        help_msg = parsers.help_message(
            "execute RUN-JOBS parallel run threads",
            hidden)
        parser.add_argument(
            *args,
             dest="run_jobs",
             type=int,
             help=help_msg)

    @staticmethod
    def remote_exec_script(
        parser, args=("--remote-exec-script",), hidden=False):
        help_msg = parsers.help_message(
            "script used to build/run remotely", hidden)
        parser.add_argument(
            *args, dest="remote_exec_script", help=help_msg)

    @staticmethod
    def remote_build_script(
        parser, args=("--remote-build-script",), hidden=False):
        help_msg = parsers.help_message(
            "script used to build remotely", hidden)
        parser.add_argument(
            *args, dest="remote_build_script", help=help_msg)

    @staticmethod
    def remote_run_script(
        parser, args=("--remote-run-script",), hidden=False):
        help_msg = parsers.help_message(
            "script used to run remotely", hidden)
        parser.add_argument(
            *args, dest="remote_run_script", help=help_msg)

    @staticmethod
    def targets(parser, args=("-t", "--targets")):
        parser.add_argument(
            *args,
             dest="targets",
             help="target list")

    @staticmethod
    def refid(parser, args=("-r", "--refid")):
        parser.add_argument(
            *args,
             dest="refid",
             help="reference variant id",
             default="REF")

    @staticmethod
    def query(parser, args=("-q", "--query")):
        parser.add_argument(*args,
                             dest="query",
                             help="results query values")

    @staticmethod
    def extra_arguments(parser, args=("--extra-arg",), hidden=False):
        help_msg = parsers.help_message(
            "argument for generator ('key=value')",
            hidden)
        parser.add_argument(
            *args,
             dest="extra_args",
             action='append',
             help=help_msg)

    class internal_flags:
        """ Namespace for internal atos flags (always hidden). """

        @staticmethod
        def local(parser, args=("--local",)):
            parser.add_argument(
                *args, action="store_true", dest="local",
                 help=argparse.SUPPRESS)  # always hidden

        @staticmethod
        def hashsum(parser, args=("--hashsum",)):
            parser.add_argument(
                *args, dest="hashsum",
                 help=argparse.SUPPRESS)  # always hidden

    class atos_help:
        """ Namespace for non common atos help options. """

        @staticmethod
        def man(parser, args=("-m", "--man")):
            parser.add_argument(
                *args,
                 dest="man",
                 action="store_true",
                 help="display manpage for TOPICS (default if available)")

        @staticmethod
        def text(parser, args=("-t", "--text")):
            parser.add_argument(
                *args,
                 dest="text",
                 action="store_true",
                 help="display textual manual for TOPICS")

        @staticmethod
        def topics(parser):
            parser.add_argument(
                "topics",
                nargs=argparse.REMAINDER,
                help="help topics. Execute 'atos help' for available topics.")

    class atos_deps:
        """ Namespace for non common atos-deps arguments. """

        @staticmethod
        def input(parser, args=("-i", "--input")):
            parser.add_argument(
                *args,
                 dest="input_file",
                 help="input build audit as generated by atos-audit, "
                 "defaults to CONFIGURATION/build.audit")

        @staticmethod
        def last(parser, args=("-l", "--last")):
            parser.add_argument(
                *args,
                 dest="last",
                 help="use last build target in the build audit "
                 "as the default target",
                 action="store_true")

        @staticmethod
        def all(parser, args=("-a", "--all")):
            parser.add_argument(
                *args,
                 dest="all",
                 help="use all build targets as the default targets, "
                 "use it when all built executables need to be optimized",
                 action="store_true")

    class atos_init:
        """ Namespace for non common atos-init arguments. """

        @staticmethod
        def no_run(parser, args=("-N", "--no-run")):
            parser.add_argument(
                *args,
                 dest="no_run", action='store_true', default=False,
                 help="do not run reference configuration")

    class atos_lib:
        """ Namespace for non common atos lib arguments. """

        @staticmethod
        def type(parser, args=("-t", "--type")):
            parser.add_argument(
                *args,
                 dest="type",
                 choices=['results_db', 'json', 'pickle'],
                 help="database type",
                 default='results_db')

        @staticmethod
        def shared(parser, args=("--shared",)):
            parser.add_argument(
                *args,
                 dest="shared",
                 help="create a shared database "
                 "(group has write permission)",
                 action="store_true")

        @staticmethod
        def text(parser, args=("-t", "--text")):
            parser.add_argument(
                *args,
                 dest="text",
                 help="text output format (default: json)",
                 action="store_true")

        @staticmethod
        def groupname(parser, args=("-g", "--group_name")):
            parser.add_argument(
                *args,
                 dest="group_name",
                 help="target group name")

        @staticmethod
        def frontier(parser, args=("-f", "--frontier")):
            parser.add_argument(
                *args,
                 dest="frontier",
                 help="only print frontier points",
                 action="store_true")

        @staticmethod
        def table(parser, args=("--table",)):
            parser.add_argument(
                *args,
                 dest="table",
                 help="output textual table form",
                 action="store_true")

        @staticmethod
        def remote_configuration_path(parser, args=("-R", "--C2")):
            parser.add_argument(
                *args,
                 dest="remote_configuration_path",
                 help="remote configuration path",
                 required=True)

        @staticmethod
        def replacement(parser, args=("-r", "--repl")):
            parser.add_argument(
                *args,
                 dest="replacement",
                 help="values replacement",
                 default="")

        @staticmethod
        def reverse(parser, args=("-X", "--reverse")):
            parser.add_argument(
                *args,
                 dest="reverse",
                 help="swap line/columns",
                 action="store_true")

        @staticmethod
        def mode(parser, args=("-m", "--mode")):
            parser.add_argument(
                *args,
                 dest="mode",
                 choices=['speedup', 'sizered', 'stdev'],
                 help="report type [speedup|sizered|stdev]",
                 default="speedup")

        @staticmethod
        def variants(parser, args=("-v", "--variants")):
            parser.add_argument(
                *args,
                 dest="variants",
                 help="target list")

        @staticmethod
        def result(parser, args=("-r", "--result")):
            parser.add_argument(
                *args,
                 dest="result",
                 help="results values",
                 default="")

        @staticmethod
        def uniq(parser, args=("-u", "--uniq")):
            parser.add_argument(
                *args,
                 dest="uniq",
                 help="omit repeated results",
                 action="store_true")

        @staticmethod
        def additem(parser, args=("-a", "--add")):
            parser.add_argument(
                *args,
                 dest="add_item",
                 help="add config item (key:value)")

        @staticmethod
        def getitem(parser, args=("-g", "--get")):
            parser.add_argument(
                *args,
                 dest="get_item",
                 help="get config item")

        @staticmethod
        def addcpl(parser, args=("--add-cpl",)):
            parser.add_argument(
                *args,
                 dest="add_cpl",
                 help="add compiler description")

        @staticmethod
        def cplflags(parser, args=("--cpl-flags",)):
            parser.add_argument(
                *args,
                 dest="cpl_flags",
                 help="print flags for flags file",
                 action="store_true")

    class atos_opt:
        """ Namespace for non common atos-opt arguments. """

        @staticmethod
        def lto(parser, args=("-l", "--lto")):
            parser.add_argument(*args,
                                 dest="lto",
                                 action='store_true',
                                 help="use use link time optimizations")

        @staticmethod
        def fdo(parser, args=("-f", "--fdo")):
            parser.add_argument(*args,
                                 dest="fdo",
                                 action='store_true',
                                 help="use feedback directed optimizations")

        @staticmethod
        def profile(parser, args=("--profile",)):
            parser.add_argument(*args,
                                 dest="profile",
                                 action='store_true',
                                 help="run in profiling mode")

    class atos_play:
        """ Namespace for non common atos-play arguments. """

        @staticmethod
        def objective(parser, args=("-f", "--objective")):
            parser.add_argument(*args,
                                 dest="obj",
                                 help="defined the objective function",
                                 choices=["time", "size"],
                                 default="time")

        @staticmethod
        def nbpoints(parser, args=("-N", "--nbpoints")):
            parser.add_argument(
                *args,
                 dest="nbpoints",
                 type=int,
                 help="get nb best points given objective or tradeoff",
                 default=1)

        @staticmethod
        def ref(parser, args=("-r", "--ref")):
            parser.add_argument(*args,
                                 dest="ref",
                                 action='store_true',
                                 help="get reference results")

        @staticmethod
        def localid(parser, args=("-l", "--localid")):
            parser.add_argument(*args,
                                 dest="localid",
                                 help="get result identified by local_id")

        @staticmethod
        def printconfig(parser, args=("-p", "--printconfig")):
            parser.add_argument(*args,
                                 dest="printconfig",
                                 action='store_true',
                                 help="print configuration only")

        @staticmethod
        def printvariant(parser, args=("-P", "--printvariant")):
            parser.add_argument(*args,
                                 dest="printvariant",
                                 action='store_true',
                                 help="print configuration variant id only")

        @staticmethod
        def printtable(parser, args=("-T", "--printtable")):
            parser.add_argument(*args,
                                 dest="printtable",
                                 action='store_true',
                                 help="print results table only")

        @staticmethod
        def reverse(parser, args=("-X", "--reverse")):
            parser.add_argument(
                *args,
                 dest="reverse",
                 help="swap line/columns of results table",
                 action="store_true")

    class atos_run:
        """ Namespace for non common atos-run arguments. """

        @staticmethod
        def silent(parser, args=("-s", "--silent")):
            parser.add_argument(
                *args,
                 dest="silent",
                 action='store_true',
                 help="silent mode, do not emit perf/size results")

    class atos_replay:
        """ Namespace for non common atos-replay arguments. """

        @staticmethod
        def results_path(parser, args=("-R", "--replay-dir")):
            parser.add_argument(
                *args,
                 dest="results_path",
                 help="directory for qualified results",
                 default="atos-qualif")

        @staticmethod
        def no_ref(parser, args=("--no-ref",)):
            parser.add_argument(
                *args,
                 dest="no_ref", action='store_true', default=False,
                 help="do not run reference")

        @staticmethod
        def variants(parser):
            parser.add_argument(
                "variants",
                nargs=argparse.REMAINDER,
                help="identifiers of variants")

    class atos_explore:
        """ Namespace for non common atos-explore-* arguments. """

        @staticmethod
        def file_by_file(parser, args=("-f", "--file-by-file")):
            parser.add_argument(
                *args,
                 dest="file_by_file",
                 action='store_true',
                 help="force file-by-file exploration",
                 default=False)

        @staticmethod
        def hot_threshold(parser, args=("-x", "--hot-th")):
            parser.add_argument(
                *args,
                 dest="hot_th",
                 type=int,
                 help="hot functions treshold percentage",
                 default=70)

        @staticmethod
        def cold_options(parser, args=("-Y", "--cold-opts")):
            parser.add_argument(
                *args,
                 dest="cold_opts",
                 help="cold functions options",
                 default="-Os")

        @staticmethod
        def cold_attributes(parser, args=("-Z", "--cold-attrs")):
            parser.add_argument(
                *args,
                 dest="cold_attrs",
                 help="cold functions attributes",
                 default="noinline cold")

        @staticmethod
        def genetic(parser, args=("--genetic",)):
            parser.add_argument(
                *args, dest="genetic", action="store_true",
                 help="use genetic exploration")

        @staticmethod
        def random(parser, args=("--random",)):
            parser.add_argument(
                *args, dest="random", action="store_true",
                 help="use random flags exploration")

        @staticmethod
        def generations(parser, args=("--generations",), hidden=False):
            help_msg = parsers.help_message(
                "number of generations",
                hidden)
            parser.add_argument(
                *args,
                 dest="generations",
                 help=help_msg,
                 default="10")

        @staticmethod
        def flags(parser, args=("-F", "--flags"), hidden=False):
            help_msg = parsers.help_message(
                "flags list filenames",
                hidden)
            parser.add_argument(
                *args, action='append',
                 dest="flags_files",
                 help=help_msg,
                 default=None)

        @staticmethod
        def mutate_prob(parser, args=("--mutate-prob",)):
            parser.add_argument(
                *args,
                 dest="mutate_prob", type=float, default=0.3,
                 help="mutation probability")

        @staticmethod
        def mutate_rate(parser, args=("--mutate-rate",)):
            parser.add_argument(
                *args,
                 dest="mutate_rate", type=float, default=0.3,
                 help="mutation rate")

        @staticmethod
        def mutate_remove(parser, args=("--mutate-remove-rate",)):
            parser.add_argument(
                *args,
                 dest="mutate_remove", type=float, default=0.3,
                 help="mutation remove rate")

        @staticmethod
        def evolve_rate(parser, args=("--evolve-rate",)):
            parser.add_argument(
                *args,
                 dest="evolve_rate", type=float, default=0.2,
                 help="evolve rate")

        @staticmethod
        def nbpoints(parser, args=("--nbpoints",)):
            parser.add_argument(
                *args,
                 dest="nbpoints",
                 type=int, default=None,
                 help="number of selected points for each tradeoff")

        @staticmethod
        def weight_class(parser, args=("--weight-class",)):
            parser.add_argument(
                *args,
                 dest="weight_class",
                 default=None,
                 help="weight class to use for weighting flags")

        @staticmethod
        def variant_id(parser, args=("--variant-id", "--variant_id")):
            parser.add_argument(
                *args,
                 dest="variant_id",
                 help="identifier of base variant",
                 default=None)

        @staticmethod
        def nb_values(parser, args=("--nbvalues",)):
            parser.add_argument(
                *args,
                 dest="nbvalues",
                 help="number of parameter values tested for each parameters",
                 default=10)

        @staticmethod
        def try_removing(parser, args=("--try-removing",)):
            parser.add_argument(
                *args,
                 dest="try_removing", action="store_true",
                 help="try to remove configuration flags")

        @staticmethod
        def tradeoff(parser, args=("--tradeoff",)):
            parser.add_argument(
                *args,
                 dest="tradeoff", type=float,
                 help="selected tradeoff given size/perf ratio",
                 default=5.0)

        @staticmethod
        def threshold(parser, args=("--threshold",), hidden=False):
            help_msg = parsers.help_message(
                "execution time threshold percentage", hidden)
            parser.add_argument(
                *args,
                 dest="threshold",
                 type=float,
                 help=help_msg,
                 default=0.0)

        @staticmethod
        def update_ref(parser, args=("--update-reference",), hidden=False):
            help_msg = parsers.help_message(
                "update reference after removing", hidden)
            parser.add_argument(
                *args, dest="update_reference", action="store_true",
                 help=help_msg)

        @staticmethod
        def keep_opt_level(parser, args=("--keep-opt-level",), hidden=False):
            help_msg = parsers.help_message(
                "Do not remove the optimization level flag while pruning",
                hidden)
            parser.add_argument(
                *args, dest="keep_opt_level", action="store_true",
                 help=help_msg)

        @staticmethod
        def pruning(parser, args=("--pruning",)):
            parser.add_argument(
                *args, dest="pruning", action='store_true',
                help="prune flags at the end of a stage or generation")

    class atos_generator:
        """ Namespace for non common atos-generator arguments. """

        @staticmethod
        def generator(parser, args=("--generator",)):
            parser.add_argument(
                *args,
                 dest="generator",
                 help="generator used for exploration")

    class atos_graph:
        """ Namespace for non common atos-graph arguments. """

        @staticmethod
        def outfile(parser, args=("-o", "--outfile")):
            parser.add_argument(
                *args,
                 dest="outfile", help="output file name")

        @staticmethod
        def hide(parser, args=("-d", "--hide")):
            parser.add_argument(
                *args,
                 dest="show", action="store_false",
                 help="do not show resulting graph")

        @staticmethod
        def follow(parser, args=("--follow",)):
            parser.add_argument(
                *args,
                 dest="follow", action="store_true",
                 help="continuously update graph with new results")

        @staticmethod
        def correl(parser, args=("--correl",)):
            parser.add_argument(
                *args,
                 dest="correlation_graph", action="store_true",
                 help="show correlation graph")

        @staticmethod
        def heat(parser, args=("--heat",)):
            parser.add_argument(
                *args,
                 dest="heat_graph", action="store_true",
                 help="show heat graph")

        @staticmethod
        def highlight(parser, args=("-H", "--highlight")):
            parser.add_argument(
                *args,
                 dest="highlight",
                 help="highlight points given a regexp")

        @staticmethod
        def frontier(parser, args=("-F", "--frontier")):
            parser.add_argument(
                *args,
                 dest="frontier_only", action="store_true",
                 help="display only frontier points")

        @staticmethod
        def xd(parser, args=("-x",)):
            parser.add_argument(
                *args,
                 dest="xd", type=int, default=0,
                 help="highlight different options sets -x[0123]")

        @staticmethod
        def anonymous(parser, args=("-a", "--anonymous")):
            parser.add_argument(
                *args,
                 dest="anonymous", action="store_true",
                 help="anonymous configuration, no configuration id on graph")

        @staticmethod
        def labels(parser, args=("-l", "--cfglbl")):
            parser.add_argument(
                *args,
                 dest="labels",
                 help="atos-configurations labels")

        @staticmethod
        def filter(parser, args=("-f", "--filter")):
            parser.add_argument(
                *args,
                 dest="filter",
                 help="filter in the points given by the regexp")

        @staticmethod
        def configuration_pathes(parser, args=("-D",)):
            parser.add_argument(
                *args,
                 dest="configuration_pathes", action='append',
                 help="additional configuration pathes")

        @staticmethod
        def xlim(parser, args=("--xlim",)):
            parser.add_argument(
                *args,
                 dest="xlim",
                 help="defines the x axis limits")

        @staticmethod
        def ylim(parser, args=("--ylim",)):
            parser.add_argument(
                *args,
                 dest="ylim",
                 help="defines the y axis limits")

        @staticmethod
        def cookie(parser, args=("--cookie",)):
            parser.add_argument(
                *args,
                 dest="cookies",
                 action='append',
                 help="cookies used for results filtering")

        @staticmethod
        def dbfile(parser):
            parser.add_argument(
                dest="dbfile",
                nargs=argparse.REMAINDER,
                help="results file")

    class atos_config:
        """ Namespace for non common atos-config arguments. """

        @staticmethod
        def ppflags(parser, args=("-D",)):
            parser.add_argument(
                *args,
                 dest="flags", action='append',
                 help="additional preprocessing flags")

        @staticmethod
        def compiler(parser, args=("--compiler",)):
            parser.add_argument(
                *args,
                 dest="compilers", action='append',
                 help="path to compiler, "
                 "defaults compilers listed in CONFIGURATION/compilers")

        @staticmethod
        def printcfg(parser, args=("--print-cfg",)):
            parser.add_argument(
                *args,
                 dest="print_cfg", action='store_true',
                 help="only print compiler configuration")

    class atos_web:
        """ Namespace for non common atos-web arguments. """

        @staticmethod
        def server(parser, args=("--server",)):
            parser.add_argument(
                *args,
                dest="server",
                help="Remote server (server:port)",
                required=True)

        @staticmethod
        def operation(parser):
            parser.add_argument(
                "operation",
                nargs=argparse.REMAINDER,
                help="operations to realize, should be 'create', "
                     "'list' or 'details'")

        @staticmethod
        def project(parser, args=("--project",)):
            parser.add_argument(
                *args,
                dest="project",
                type=int,
                help="Current project identifier",
                required=True)

        @staticmethod
        def experiment(parser, args=("--experiment",)):
            parser.add_argument(
                *args,
                dest="experiment",
                type=int,
                help="Current experiment identifier",
                required=True)

        @staticmethod
        def target(parser, args=("--target",)):
            parser.add_argument(
                *("--target",),
                dest="target",
                type=int,
                help="Current target identifier",
                required=True)
