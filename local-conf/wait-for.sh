#!/bin/sh

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 host port command..."
  exit 1
fi

host="$1"
port="$2"
shift 2
cmd="$@"

echo "Waiting for $host:$port ..."

while ! nc -z "$host" "$port"; do
  echo "Still waiting for $host:$port ..."
  sleep 1
done

echo "$host:$port is available. Running command: $cmd"
exec $cmd
