#!/usr/bin/env python

""" An executable which proxies for a subprocess; upon a signal, it sends that
signal to the process identified by a pidfile. """

import os
import sys
import signal
import time


class PidProxy:
    pid = None
    def __init__(self, args):
        self.setsignals()
        self.reaped_parent = False

        try:
            self.pidfile, cmdargs = args[1], args[2:]
            self.command = os.path.abspath(cmdargs[0])
            self.cmdargs = cmdargs
        except (ValueError, IndexError):
            self.usage()
            sys.exit(1)

    def getpidfromfile(self):
        try:
            with open(self.pidfile, 'r') as f:
                return int(f.read().strip())
        except:
            return None

    def go(self):
        self.pid = os.spawnv(os.P_NOWAIT, self.command, self.cmdargs)
        while 1:
            time.sleep(5)
            try:
                self.pid = self.getpidfromfile()
                if self.pid is None:
                    break
                pid, sts = os.waitpid(self.pid, os.WNOHANG)
            except OSError:
                pid, sts = None, None
            if pid:
                break

    def usage(self):
        print("pidproxy.py <pidfile name> <command> [<cmdarg1> ...]")

    def setsignals(self):
        signal.signal(signal.SIGTERM, self.passtochild)
        signal.signal(signal.SIGHUP, self.passtochild)
        signal.signal(signal.SIGINT, self.passtochild)
        signal.signal(signal.SIGUSR1, self.passtochild)
        signal.signal(signal.SIGUSR2, self.passtochild)
        signal.signal(signal.SIGQUIT, self.passtochild)
        signal.signal(signal.SIGCHLD, self.reap)

    def reap(self, sig, frame):
        if not self.reaped_parent:
            os.waitpid(-1, 0)
            self.reaped_parent = True
            return
        try:
            pid = self.getpidfromfile()
            if pid is None:
                pid = self.pid
            _, _ = os.waitpid(pid, 0)
            sys.exit(0)
        except:
            pass

    def passtochild(self, sig, frame):
        pid = self.getpidfromfile()
        if pid is None:
            pid = self.pid
        os.kill(pid, sig)
        if sig in [signal.SIGTERM, signal.SIGINT, signal.SIGQUIT]:
            sys.exit(0)


def main():
    pp = PidProxy(sys.argv)
    pp.go()

if __name__ == '__main__':
    main()
