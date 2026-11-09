# Fixtures for scripts/boundary_checks.sh: each case must turn its check red, each clean twin green.
checks="$(pwd)/scripts/boundary_checks.sh" status=0
scan_grep() { grep -rHInE -e "$1" . | sed 's|^\./||'; }
expect() {  # expect <red|green> <FAIL line or -> <path> <file content>
  dir=$(mktemp -d) && mkdir -p "$dir/$(dirname "$3")" && printf '%s\n' "$4" > "$dir/$3"
  out=$(CDPATH= cd -- "$dir" && fail=0 && . "$checks" && exit "$fail"); rc=$?
  rm -rf "$dir"
  case "$1:$rc" in
    red:0|green:[!0]*) printf '%s\n' "FAIL: $3 should turn the check $1: $out"; status=1 ;;
    red:*) case "$out" in *"$2"*) ;; *) printf '%s\n' "FAIL: $3 is red without '$2': $out"; status=1 ;; esac ;;
  esac
}
expect red 'harmony core imports' djasistan/engine.py 'from pyrekordbox import Rekordbox6Database'
expect green - djasistan/rbread.py 'from pyrekordbox import Rekordbox6Database'
expect red 'only djasistan/rbwrite.py' select_sets.py 'db.commit()'
expect red 'only djasistan/rbwrite.py' djasistan/libpool.py 'os.replace(a, b)'
expect green - djasistan/rbwrite.py 'db.commit(); os.replace(a, b)'
expect red 'browser profile' djasistan/x.py 'p = "~/Library/Application Support/Google/Chrome/Default"'
expect green - djasistan/x.py 'p = "~/.gamdl/cookies.txt"'
expect red 'personal data' README.md 'contact: someone@gmail.com'
expect red 'personal data' docs/x.md 'see /Users/someone/Music'
expect red 'personal data' private/sets.json '{}'
expect red 'personal data' docs/y.md 'see /Users/Someone/Music'
expect red 'personal data' scripts/gate_config.sh 'p=/Users/Someone/bin/'
expect green - scripts/review.sh 'p=/Users/Someone/bin/'
expect green - docs/x.md 'see ~/Music and noreply@anthropic.com'
[ "$status" = 0 ] && echo "boundary fixtures: ok"
exit "$status"
