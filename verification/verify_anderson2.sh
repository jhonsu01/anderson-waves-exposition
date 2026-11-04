#!/bin/bash
# Repite la comprobacion del kernel desde cero y prueba la no vacuidad. Usa el volumen ya compilado.
set -u
export ELAN_HOME=/vol/elan HOME=/vol/home TMPDIR=/vol/tmp XDG_CACHE_HOME=/vol/cache
export PATH="$ELAN_HOME/bin:$PATH"
stamp() { echo "=== $(date -u +%FT%TZ) $*"; }
apt-get update -qq && apt-get install -y -qq --no-install-recommends git ca-certificates >/dev/null
git config --global --add safe.directory '*'
cd /vol/repo || exit 1
echo "HEAD $(git rev-parse HEAD)"

stamp nonvacuity
git fetch -q origin
git log -1 --format='main %H %ad' --date=iso origin/main
mkdir -p /tmp/nv
if git show origin/main:Verification/NonVacuity.lean > /tmp/nv/NonVacuity.lean; then
  timeout 3600 lake env lean /tmp/nv/NonVacuity.lean > /logs/anderson_nonvacuity.log 2>&1
  echo "NONVACUITY_EXIT $?"
  tail -8 /logs/anderson_nonvacuity.log | cut -c1-220
else
  echo "NONVACUITY_NOT_FOUND"
fi

stamp leanchecker_fresh
timeout 7200 lake env leanchecker --fresh AndersonAC.Blueprint.Main > /logs/anderson_leanchecker.log 2>&1
echo "LEANCHECKER_FRESH_EXIT $?"
tail -3 /logs/anderson_leanchecker.log | cut -c1-200
stamp fin
