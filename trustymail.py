#!/usr/bin/python

import argparse
import logging

COMMENT_PREFIX='#'


def WritePostgrey(path, addresses):
  try:
    with open(path, 'w') as pconf:
      for addr in addresses:
        pconf.write('%s\n' % addr)
  except IOError as e:
    logging.error('failure updating postgrey: %s', str(e))


def WriteSpamAss(path, addresses):
  try:
    with open(path, 'w') as pconf:
      for addr in addresses:
        if '@' not in addr:
          addr = '*@%s' % addr
        pconf.write('whitelist_from %s\n' % addr)
  except IOError as e:
    logging.error('failure updating spamassassin: %s', str(e))


def main():
  parser = argparse.ArgumentParser(description='Update mail server trusted parties.')
  parser.add_argument('-T', '--trusted_senders_file', type=file,
                      help='file containing trusted senders',
                      required=True)
  parser.add_argument('-P', '--postgrey', action='store_true', help='configure postgrey')
  parser.add_argument('--postgrey_file', 
                      default='/etc/postgrey/whitelist_clients.local', 
                      help='postgrey whitelist file')
  parser.add_argument('-S', '--spamassassin', action='store_true', help='configure spamassassin')
  parser.add_argument('--spamassassin_file',
                      default='/etc/spamassassin/local_whitelist.cf',
                      help='spamassassin whitelist file')
  parser.add_argument('--stdout', action='store_true', help='log to stdout')
  args = parser.parse_args()
  addresses=[]
  if args.stdout:
    logging.basicConfig(level=logging.INFO)
  for line in args.trusted_senders_file:
    line=line.strip()
    if line and line[0] is not COMMENT_PREFIX:
      addresses.append(line)
  addresses.sort()
  if args.spamassassin and args.spamassassin_file:
    logging.info('updating spamassassin file %s', args.spamassassin_file)
    WriteSpamAss(args.spamassassin_file, addresses)
  if args.postgrey and args.postgrey_file:
    logging.info('updating postgrey file %s', args.postgrey_file)
    WritePostgrey(args.postgrey_file, addresses)


if __name__ == "__main__":
    main()
