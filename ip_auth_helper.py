#/usr/bin/python
import sys
import redis

import logging

# create logger with 'spam_application'
logger = logging.getLogger('squid_ip_auth')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/tmp/squid-ip.log')
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

#init Redis Client
r = redis.StrictRedis(host='localhost', port=6379, db=0)


def grant(ret):
    sys.stdout.write("OK {}\n".format(ret))
    sys.stdout.flush()


def deny():
    sys.stdout.write('ERR\n')
    sys.stdout.flush()

while 1:
    line = sys.stdin.readline()
    if not line:
        break
    req = line.split(' ')
    curip=req[0].rstrip('\n')
    logger.info('received %s' % curip)
    user = r.get(curip)
    if (user):
        logger.info('ip %s is %s' % (curip, user ))
        grant("user={}".format(user))
    else:
        deny()