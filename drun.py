#! /usr/bin/env python
# -*- coding: utf8 -*-

# Run docker container as a CLI tool

import getpass
import json
import os
import sys
import subprocess

def run(cmd):
    p = subprocess.Popen(cmd, stdout=None, stderr=None)
    res = p.wait()
    if res != 0:
        exit(res)

def run_out(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = p.wait()
    out = p.stdout.read()
    if res != 0:
        print out
        exit(res)
    return out

def fail(s=None):
    if s != None:
        print s
    exit(1)


args = sys.argv
args.pop(0)

if len(args) == 0 or args[0] in ["--help", "help"]:
    print "Usage: drun <subcmd> [arg]"
    print "  drun install username/image[:version] - install image from dockerhub"
    print "  drun remove  username/image[:version] - uninstall image"
    print "  drun username/image[:version] [args]  - run image as CLI program"
    exit(0)

subcmd = args.pop(0)

if subcmd in ["install", "inst", "i", "-i"]:
    if len(args) == 0:
        fail("Usage: drun install username/image[:version]")
    for arg in args:
        run(["docker", "pull", arg])

elif subcmd in ["remove", "rm", "erase", "-r", "-e"]:
    if len(args) == 0:
        fail("Usage: drun remove username/image[:version]")
    for arg in args:
        run(["docker", "rmi", arg])

else:
    user = getpass.getuser()
    pwd  = os.getcwd()

    insp = run_out(["docker", "inspect", subcmd])
    info = json.loads(insp)
    tool = info[0]["ContainerConfig"]["Labels"]["tool"]

    cmd = ["docker", "run", "-it", "--rm", "-v", pwd + ":/workspace"]
    cmd.extend(["-e", "DRUN_USER=" + user])
    cmd.extend(["-e", "DRUN_TOOL=" + tool])
    cmd.append(subcmd)
    cmd.extend(["bash", "/dcont.sh"])
    cmd.extend(args)
    run(cmd)

