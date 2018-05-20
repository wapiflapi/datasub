# Very early alpha.

# datasub

version number: 0.0.1
author: Wannes Rombouts

# Overview

A GraphQL cache mapping queries to subscriptions.

# Installation

Clone the repo and install:

    $ git clone https://github.com/wapiflapi/datasub.git
    $ python setup.py install  # or `develop` for hacking.

# Usage

As an early alpha the usage is mainly geared towards testing.

    $ python -m datasub --help

To run `datasub` as a front to GitHub's API with `hupper` providing auto-reload on file changes:

    $ DATABASE_URL='sqlite:///datasub.sqlite' DATASUB_REMOTE_AUTHORIZATION="bearer XXX" hupper -m datasub --debug https://api.github.com/graphql --setup-db

This stores info in sqlite file. Given the `--setup-db` option the database is configured,


# Todo

- [x] Provide option to build delegating schemas
- [x] Pass through queries and mutations
- [ ] Add monitoring-cache
- [ ] Expose subscriptions on cache diffs.
  Multiple levels of diffs possible:
    - per request, per node gid, ...
    - monitor user's requests and our responses
    - monitor our requests and server responses
- [ ] Figure out how to do without __typename
- [ ] Enable auto-polling.
- [ ] Add websocket transport for subscriptions/gql.
- [ ] Figure out when/how to reload schemas.
  Apparently best practice is committing the schema.sdl,
  give user the option to pass it as an command line option?
- [ ] Add support for X-Request-ID
- [ ] Forward authentication
- [ ] Make sure monitoring never prevents request completion. (crashes, etc.)
- [ ] monitor user errors
