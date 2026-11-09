#!/usr/bin/env python3
"""PreToolUse(Bash) gate: refuse Rekordbox DB writes when Rekordbox is open or the pending sets fail the BPM/key audit.

A command counts as a DB write when it runs one of WRITERS. The pending sets live in state/pending_sets.json
(written by the selection step); a write with no pending file is refused too, so nothing skips the audit.
"""
import json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Only an actual run counts (python … <writer>.py); a name inside a heredoc, grep or commit message does not.
WRITERS=re.compile(r'python[\w.]*(\s+-\S+)*\s+\S*\b(install|import_new|apply_sets|fix_bundles|update_install)\.py\b')
def deny(msg):
    print(json.dumps({"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":msg}}))
    sys.exit(0)
cmd=(json.load(sys.stdin).get('tool_input') or {}).get('command','')
if not WRITERS.search(cmd): sys.exit(0)
if subprocess.run(['pgrep','-x','rekordbox'],capture_output=True).returncode==0:
    deny('Rekordbox açık: DB yazmadan önce Rekordbox kapatılmalı.')
if 'import_new.py' in cmd: sys.exit(0)   # importing files into the collection does not build sets
pending=ROOT/'state/pending_sets.json'
if not pending.exists(): deny('state/pending_sets.json yok: setler BPM/ton denetiminden geçmeden Rekordbox\'a yazılamaz.')
sys.path.insert(0,str(ROOT))
from djasistan.audit import main
import io,contextlib
buf=io.StringIO()
with contextlib.redirect_stdout(buf): ok=main(str(pending))
if not ok: deny('Set denetimi başarısız (en az %80 uyumlu geçiş, yasaklı sanatçı yok):\n'+buf.getvalue())
