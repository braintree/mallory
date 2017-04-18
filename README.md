# Mallory

Reverse proxy for HTTPS services, with SSL verification.

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)
[![Build Status](https://secure.travis-ci.org/braintree/mallory.png)](http://travis-ci.org/braintree/mallory)

## DEPRECATED

Braintree no longer uses or maintains this project. It remains available for
research and derivative works, subject to the project's license.

## Installation

Execute:

    $ pip install mallory

Or install it yourself with:

    $ python setup.py install

## Usage

    $ mallory \
      --port 8001 \
      --ssl-key /etc/ssl/private/proxy-hostname.example.com-key.pem \
      --ssl-cert /etc/ssl/certs/proxy-hostname.example.com-cert.pem \
      --pid-file /var/run/mallory.pid \
      --verify-ca-cert /etc/ssl/certs/ca-certificates.crt \
      https://destination.example.com

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
