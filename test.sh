#!/bin/bash

set -e

_id=$RANDOM

create() {
    curl -s -H "Content-Type: application/json" http://127.0.0.1:8000/api/customer/ --data "{\"login\": \"henk$_id\"}"
    echo
}

# Two requests to create same login virtually at the same time
create &
create

# And one request afterward to show how the response should be
sleep 0.5
create
