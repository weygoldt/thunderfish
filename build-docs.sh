#!/bin/bash

die() { echo "ERROR: $*"; exit 2; }
warn() { echo "WARNING: $*"; }

for cmd in mkdocs pdoc3; do
    command -v "$cmd" >/dev/null ||
        warn "missing $cmd: run \`pip install $cmd\`"
done

PACKAGE="thunderfish"
PACKAGEROOT="$(dirname "$(realpath "$0")")"
BUILDROOT="$PACKAGEROOT/site"

echo
echo "Clean up documentation of $PACKAGE"
echo

rm -rf "$BUILDROOT" 2> /dev/null || true
mkdir -p "$BUILDROOT"

if command -v mkdocs >/dev/null; then
    echo "Building general documentation for $PACKAGE"
    echo

    cd "$PACKAGEROOT"
    mkdocs build --config-file .mkdocs.yml --site-dir "$BUILDROOT"
    cd - > /dev/null
fi

if command -v pdoc3 >/dev/null; then
    echo
    echo "Building API reference docs for $PACKAGE"
    echo

    cd "$PACKAGEROOT"
    pdoc3 --html --config latex_math=True --config sort_identifiers=False --output-dir "$BUILDROOT/api-tmp" $PACKAGE
    mv "$BUILDROOT/api-tmp/$PACKAGE" "$BUILDROOT/api"
    rmdir "$BUILDROOT/api-tmp"
    cd - > /dev/null
fi

echo
echo "Done. Docs in:"
echo
echo "    file://$BUILDROOT/index.html"
echo
