# MyDJKit boundary checks — SOURCED by scripts/check.sh, never executed on its own.
# Fixtures: tests/boundary_checks_test.sh (run by the build command). Rules: AGENTS.md, "Architecture boundaries".

# Project code: the package, the hooks and the root scripts. Kit-owned scripts/ and .claude/ are not ours.
proj='^(djasistan/|hooks/|[^/]+\.py:)'

hits=$(scan_grep '(import|from)[[:space:]]+(pyrekordbox|sqlcipher3)' | grep -E '^djasistan/(camelot|audit|engine)\.py:')
if [ -n "$hits" ]; then
  echo "FAIL [boundary]: the harmony core imports a Rekordbox database library:"
  echo "$hits"; fail=1
fi

hits=$(scan_grep '\.commit\(|os\.replace\(' | grep -E "$proj" | grep -v '^djasistan/rbwrite\.py:')
if [ -n "$hits" ]; then
  echo "FAIL [boundary]: only djasistan/rbwrite.py may write the Rekordbox database:"
  echo "$hits"; fail=1
fi

hits=$(scan_grep 'Library/(Cookies|Safari|Containers/com\.apple\.Safari)|Application Support/(Google/Chrome|BraveSoftware|Firefox|Microsoft Edge|Arc)|\.mozilla/firefox|\.config/google-chrome' | grep -E "$proj")
if [ -n "$hits" ]; then
  echo "FAIL [boundary]: project code names a browser profile or cookie folder:"
  echo "$hits"; fail=1
fi

hits=$(scan_grep '[A-Za-z0-9._%+-]+@(gmail|hotmail|outlook|yahoo|icloud|me|proton(mail)?)\.[a-z]{2,}|/Users/[A-Za-z][A-Za-z0-9._-]*/|/home/[A-Za-z][A-Za-z0-9._-]*/' | grep -vE '^(scripts|setup)/|^tests/boundary_checks_test\.sh:' ; scan_grep '/Users/[A-Za-z][A-Za-z0-9._-]*/' | grep -E '^scripts/(gate_config|boundary_checks)\.sh:' | grep -v 'scan_grep')
priv=$(scan_grep '' | grep '^private/' | cut -d: -f1 | sort -u)
if [ -n "$hits$priv" ]; then
  echo "FAIL [boundary]: personal data in a tracked file (this repository is public):"
  [ -n "$hits" ] && echo "$hits"
  [ -n "$priv" ] && echo "$priv"
  fail=1
fi
