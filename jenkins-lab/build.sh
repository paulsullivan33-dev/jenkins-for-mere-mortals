#!/bin/sh
# Orbit Widgets — a tiny invented project used as this guide's fixture.
set -eu
VERSION=$(cat VERSION)
mkdir -p dist
{
  echo "ORBIT-WIDGETS BUILD MARKER"
  echo "orbit-widgets version $VERSION"
  date -u +"built at %Y-%m-%dT%H:%M:%SZ"
} > dist/release.txt
echo "Build complete: orbit-widgets $VERSION"
