# Very early alpha.

# datasub

version number: 0.0.1
author: Wannes Rombouts

# Overview

A GraphQL cache mapping queries to subscriptions.

# Installation / Usage

To install use pip:

    $ pip install datasub


Or clone the repo:

    $ git clone https://github.com/wapiflapi/datasub.git
    $ python setup.py install

# Contributing

TBD

# Example

TBD

# Todo

- [x] Provide option to build delegating schemas
- [x] Pass through queries and mutations
- [ ] Add monitoring-cache
- [ ] Expose subscriptions on cache diffs.
  Multiple levels of diffs possible:
    - per request, per node gid, ...
    - monitor user's requests and our responses
    - monitor our requests and server responsse
- [ ] Figure out how to do without __typename
- [ ] Enable auto-polling.
- [ ] Add websocket transport for subscriptions/gql.
- [ ] Figure out when/how to reload schemas.
  Apparently best practice is committing the schema.sdl,
  give user the option to pass it as an command line option?
- [ ] Add support for X-Request-ID
