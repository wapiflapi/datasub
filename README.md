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
- [ ] Add websocket transport for subscriptions/gql.
- [ ] Figure out when/how to reload schemas.
  Apparently best practice is committing the schema.sdl,
  give user the option to pass it as an command line option?
- [ ] Update requirements (warning:graphql_ws needs recent commit!)
