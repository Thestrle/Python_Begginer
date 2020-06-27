#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Custom SSH client.
1. It somehow _supports_ async execution.
2. It provides exit status.
3. It jams stdin (ssh -nT).
Run like something "python ssh.py box user=bs command='echo aaa; echo bbb >&2; sleep 40; exit 23'" to test
'''
import logging
logging.basicConfig(level=logging.INFO,
                    datefmt='%F %T %z',
                    format='%(asctime)s:%(name)s:%(levelname)s:%(module)s: %(message)s',
                    #filename='/var/log/ws-bs.log',
                   )
logger = logging.getLogger('ssh-client')

import os
import time         # for sleep & time
import subprocess   # for proxy handling
import socket       # for socket.error
import paramiko

POLL_TIMEOUT = 0.01
CONFIG = os.path.expanduser('~/.ssh/config')
KNOWN_HOSTS = os.path.expanduser('~/.ssh/known_hosts')
USER = os.environ.get('USER', os.environ.get('LOGNAME'))
CONNECT_TIMEOUT = 2
EXEC_TIMEOUT = 32

def load(filename):
    if os.path.exists(filename):
        with open(filename) as fp:
            return fp.read()

class MySSHClient(paramiko.SSHClient):
    'Not for any other use. Just quite ubruptly expose the channel.'

    def exec_command(
        self,
        command,
        bufsize=-1,
        timeout=None,
        get_pty=False,
        environment=None,
    ):
        self.channel = self._transport.open_session(timeout=timeout)
        if get_pty:
            self.channel.get_pty()
        self.channel.settimeout(timeout)
        if environment:
            self.channel.update_environment(environment)
        self.channel.exec_command(command)
        stdin = self.channel.makefile('wb', bufsize)
        stdout = self.channel.makefile('r', bufsize)
        stderr = self.channel.makefile_stderr('r', bufsize)
        self.io = (stdin, stdout, stderr)

    def exit_status_ready(self):
        return self.channel.exit_status_ready()

    def recv_exit_status(self):
        return self.channel.recv_exit_status()

    def wait_for_completion(self, poll_timeout=POLL_TIMEOUT, exec_timeout=EXEC_TIMEOUT):
        tx = time.time() + float(exec_timeout)
        n = 0L
        while not self.exit_status_ready():
            n += 1L
            if time.time() > tx:
                raise paramiko.SSHException('Execution timeout exceeded', n)
            time.sleep(poll_timeout)
        return self.channel.recv_exit_status()

    def fetch_output(self):
        stdout = self.io[1].read().decode()
        stderr = self.io[2].read().decode()
        return stdout, stderr
#end class MySSHClient

class SSH(object):

    def __init__(self, *av, **kw):
        self.ssh = MySSHClient()
        self.args = (av, kw)
        self.config = paramiko.SSHConfig()
        if os.path.exists(CONFIG):
            with open(CONFIG) as fp:
                self.config.parse(fp)

    def arg(self, name, default=None):
        if name == 'host':
            if name not in self.args[1]:
                return self.args[0][0] if self.args[0] else default
        return self.args[1].get(name, default)

    @staticmethod
    def knows_host(host):
        host = host.lower()
        kh = load(KNOWN_HOSTS)
        if not kh:
            return False
        for r in [tuple([e.lower() for e in s.split().pop(0).split(',')])
                  for s in kh.splitlines()]:
            for e in r:
                if e == host:
                    return True
        return False

    def __enter__(self):
        host = self.arg('host')
        logger.debug('Entering host=%s, args=%s', `host`, `self.args`)
        assert host, 'No "host=" arg specified.'

        self.ssh.load_system_host_keys()

        # don't "refresh" existing keys automagically, but add new silently
        policy = paramiko.RejectPolicy if self.knows_host(host) else paramiko.AutoAddPolicy
        logger.debug('Policy: {}'.format(policy.__name__))
        self.ssh.set_missing_host_key_policy(policy())

        host_config = self.config.lookup(host)
        if 'proxycommand' in host_config: # http://www.programcreek.com/python/example/4561
            proxy = paramiko.ProxyCommand(
                subprocess.check_output(
                    [os.environ['SHELL'], '-c', 'echo %s' % host['proxycommand']]
                ).strip()
            )
            logger.info('Proxy: %s', `proxy`)
        else:
            proxy = None
            logger.debug('No proxy')

        kw = self.args[1].copy()
        kw.update({
            'port': self.arg('port', 22),
            'username': self.arg('user', USER),
            'timeout': self.arg('timeout', CONNECT_TIMEOUT),
            'auth_timeout': self.arg('auth_timeout', self.arg('timeout', CONNECT_TIMEOUT)),
            'banner_timeout': self.arg('banner_timeout', self.arg('timeout', CONNECT_TIMEOUT)),
            'sock': proxy,
        })
        call = dict([(k, kw[k])
                     for k in ('port', 'username', 'password', 'pkey',
                               'key_filename', 'timeout', 'allow_agent',
                               'look_for_keys', 'compress', 'sock',
                               'gss_auth', 'gss_kex', 'gss_deleg_creds', 'gss_host',
                               'banner_timeout', 'auth_timeout')
                     if k in kw]
                   ) # build valid args

        try:
            self.ssh.connect(host, **call)
        except paramiko.BadHostKeyException as exc:
            logger.error('host key could not be verified: %s', `exc`)
            return None
        except paramiko.AuthenticationException as exc:
            logger.error('authentication failed: %s', `exc`)
            return None
        except paramiko.SSHException as exc:
            logger.error('SSH ooops: %s', `exc`)
            return None
        except socket.error as exc:
            logger.error('SSH connect: %s', `exc`)
            return None
        return self

    def __exit__(self, et, ev, etb):
        self.ssh.close()
        logger.debug('Leaving host %s', `self.arg('host')`)

    def start(self, *av, **kw):
        command = ' '.join(av)
        command = '{ %s; } <"%s"' % (command, os.devnull) # jam stdin off
        kw['get_pty'] = False # plz, no ttys here
        kw['timeout'] = kw.get('timeout', EXEC_TIMEOUT)

        logger.info('Running %s %s', `command`, `kw`)
        try:
            self.ssh.exec_command(command, **kw)
        except paramiko.SSHException as exc:
            logger.error('SSH Exception on %s: %s', `command`, `exc`)
            raise
        self.ssh.io[0].close() # = open(os.devnull) somewhere deeper...

    def run(self, *av, **kw):
        try:
            self.start(*av, **kw)
        except paramiko.SSHException as exc:
            return None, None, None
        except Exception as exc:
            logger.error('Exception on %s %s: %s', `av`, `kw`, `exc`)
            return None, None, None
        try:
            rc = self.ssh.wait_for_completion()
        except paramiko.SSHException as exc:
            logger.error('Run time exception on %s %s: %s', `av`, `kw`, `exc`)
            return None, None, None
        logger.debug('SSH(%s) %s: done %s', self.arg('host'), `av`, `rc`)
        return (rc,) + self.ssh.fetch_output()
#end class SSH

if __name__ == '__main__':
    import sys

    av = []
    kw = {}
    for arg in sys.argv[1:]:
        if '=' in arg:
            n, v = arg.split('=', 1)
            try:
                kw[n] = int(v)
            except:
                kw[n] = v
        else:
            av.append(arg)
    av = tuple(av)

    with SSH(*av, **kw) as ssh:
        if ssh:
            rc, out, err = ssh.run(kw.get('command', 'ls -la'))
            if rc is not None:
                print('RC=%d' % (rc,))
                if out:
                    print('O> ' + '\nO> '.join(out.splitlines()))
                if err:
                    print('E> ' + '\nE> '.join(err.splitlines()))
            else:
                print('Command failed (timeout?)')
        else:
            print('Sorry, guys!')
