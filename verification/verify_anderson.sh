#!/bin/bash
# Compila y audita la formalizacion Lean de Anderson (cadamcat/anderson-ac-lean4). Resultados en /logs.
set -u
COMMIT=38116e1a
export ELAN_HOME=/vol/elan HOME=/vol/home TMPDIR=/vol/tmp XDG_CACHE_HOME=/vol/cache
mkdir -p "$HOME" "$TMPDIR" "$XDG_CACHE_HOME"
export PATH="$ELAN_HOME/bin:$PATH"
stamp() { echo "=== $(date -u +%FT%TZ) $*"; df -h /vol | tail -1; }

stamp apt
apt-get update -qq && apt-get install -y -qq --no-install-recommends git curl ca-certificates zstd >/dev/null || exit 10

stamp elan
curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o /tmp/elan-init.sh || exit 11
sh /tmp/elan-init.sh -y --no-modify-path --default-toolchain none || exit 11

stamp clone
git config --global --add safe.directory '*'
git config --global core.autocrlf false
git clone -q https://github.com/cadamcat/anderson-ac-lean4.git /vol/repo || exit 12
cd /vol/repo || exit 12
git checkout -q "$COMMIT" || exit 12
echo "HEAD $(git rev-parse HEAD)"
cat lean-toolchain
sha256sum AndersonAC/Challenge.lean

stamp cache
lake exe cache get 2>&1 | grep -v '^Downloaded' | tail -3

stamp verify
timeout 18000 bash scripts/verify.sh > /logs/anderson_verify.log 2>&1
CODE=$?
echo "VERIFY_EXIT $CODE"
grep -E "depends on axioms|error|sorry|Build completed|build failed" /logs/anderson_verify.log | tail -40 | cut -c1-200

stamp nonvacuity
timeout 3600 lake env lean Verification/NonVacuity.lean > /logs/anderson_nonvacuity.log 2>&1
echo "NONVACUITY_EXIT $?"
tail -5 /logs/anderson_nonvacuity.log | cut -c1-200

stamp leanchecker
timeout 7200 lake env leanchecker AndersonAC.Blueprint.Main > /logs/anderson_leanchecker.log 2>&1
echo "LEANCHECKER_EXIT $?"
tail -3 /logs/anderson_leanchecker.log | cut -c1-200
stamp fin
exit "$CODE"
