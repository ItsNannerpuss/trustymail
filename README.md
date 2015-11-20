# trustymail

Takes a list of email addresses or domains of trusted senders and generates whitelist files for Postgrey, SpamAssassin, etc.

## Running

The sender list should be a plaintext file with one email address or domain per line.  Comments prefixed with *#* are permitted.

    -S: Path to the sender list.
    -A: Path to the spamassassin whitelist. (optional)
    -P: Path to the postgrey whitelist. (optional)

Example:

`python trustymail.py -S ~/senders.txt -A /etc/spamassassin/local_whitelist.cf -P /etc/postgrey/whitelist_clients.local`

## Postgrey Support

Postgrey supports a default local whitelist file in /etc/postgrey/whitelist_clients.local.  The whitelist file will
match either full addresses or domains (no wildcard required).

## SpamAssassin Support

SpamAssassin should load any *.cf file in its configuration directory, so we can specify any file name under the config
path.

SpamAssassin uses the whitelist_from command with either a fully qualified address, or a wildcard (*@domain.com).

