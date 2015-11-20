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
  parser.add_argument('-A', '--spamassassin_file', help='spamassassin whitelist file')
  parser.add_argument('-P', '--postgrey_file', help='postgrey whitelist file')
  parser.add_argument('-S', '--trusted_senders_file', type=file, help='file containing trusted senders', required=True)
  args = parser.parse_args()
  addresses=[]
  for line in args.trusted_senders_file:
    line=line.strip()
    if line and line[0] is not COMMENT_PREFIX:
      addresses.append(line)
  addresses.sort()
  if args.spamassassin_file:
    logging.info('updating spamassassin file %s', args.spamassassin_file)
    WriteSpamAss(args.spamassassin_file, addresses)
  if args.postgrey_file:
    logging.info('updating postgrey file %s', args.postgrey_file)
    WritePostgrey(args.postgrey_file, addresses)


if __name__ == "__main__":
    main()
