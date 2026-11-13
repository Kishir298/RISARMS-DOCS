# Progress — release readiness session (2026-11-13, phase 2)

Continues [recovery-2026-11-13.md](recovery-2026-11-13.md). Every row records
what was changed, what proved it, and whether it is verified. Rows marked
**verified** were checked by a command whose output is quoted in this document
or in the CI run listed.

## 1. CI diagnosis

| # | Finding | Evidence | Fix | Status |
|---|---|---|---|---|
| 1 | ASCS `ci.yml` was **rejected before any job ran** — job-level `env` used the `runner` context, which GitHub does not allow there | the failed run had `total_count: 0` jobs; `actionlint` reports `context "runner" is not allowed here` | move the value into the step-level `env` | verified — CI **success** on `c2f4464` |
| 2 | RESCS `live-tests.yml` was rejected — `secrets` used in job- and step-level `if` | `actionlint`: `context "secrets" is not allowed here` | map secrets into job `env`, gate with `env.*`, print each target as available/UNAVAILABLE | verified — RESCS `CI` **success** on `cdbd6fa` |
| 3 | Feature pushes produced **no run at all** for most workflows (`branches: [main]` only) | run history showed no entry for the pushed SHAs | push triggers now include `feat/**` and `fix/**` | verified — runs now exist for every pushed branch |
| 4 | `macos-15-intel` is not a GitHub runner label (Intel macOS is `macos-13`) | `actionlint` [runner-label] error in CORE/ASIS/ASCS/RESCS `release.yml` | label corrected | implemented; a release run has not been dispatched |

## 2. Desktop application

| # | Change | Files | Test evidence | Status |
|---|---|---|---|---|
| 5 | **Single-flight sync**: the 60 s timer and `connection.restored` could start two workers over the same queues | `risarms_ui/app.py` | full suite 227 passing; the guard itself needs a Tk event loop, so it is not behaviour-tested on this host | implemented, partially verified |
| 6 | **Doctor verified the wrong package**: `import client` was satisfied by this repo's legacy `client/` package, so a missing CORE-CLIENT was undetectable | `risarms_ui/entrypoint.py`, `tests/test_desktop_doctor.py` | `1 passed`, asserts the value equals `importlib.metadata.version("core-client")` | verified |
| 7 | **Real two-client messaging E2E**: launches `core web`, two independent cookie jars, WSS ticket push | `tests/integration/test_core_messaging_e2e.py` | `2 passed` (HTTP + WSS) | verified |
| 8 | **Durable queue across restart** and **no duplicate sends** | `tests/test_messaging.py` | `10 passed` in that file | verified |

## 3. Installer pipeline

| # | Change | Status |
|---|---|---|
| 9 | Linux release job now builds from a virtualenv made with `/usr/bin/python3`, because `apt install python3-tk` does not add Tk to the `setup-python` interpreter | implemented; `actionlint` clean |
| 10 | Windows job appends Inno/WiX directories to `PATH` and **fails early** if `iscc`, `candle`, `light` or `heat` is missing | implemented; `actionlint` clean |
| 11 | Added an Apple Silicon macOS job (`macos-14`) beside Intel (`macos-13`) | implemented |
| 12 | The Tk gate is now `python -c "import tkinter"`; `--doctor` requires a display and would fail on any headless runner | implemented |
| 13 | **No installer artifact was produced.** Two `brew install python-tk@3.14` attempts exceeded 10 minutes each (tcl-tk builds from source) and the only Tk-enabled interpreter here is the 3.9.6 system Python, below `requires-python >= 3.10` | **blocked locally** |

To produce artifacts without this host:
1. GitHub → Actions → **desktop-release** → *Run workflow* (branch
   `feat/risarms-ui-desktop`), or push a `v*` tag.
2. Download `risarms-desktop-macos-x86_64`, `-macos-arm64`, `-windows-x86_64`,
   `-linux-x86_64`.
3. Install each on a clean machine and record the hashes here.

## 4. Documentation and requirements

| # | Change | Status |
|---|---|---|
| 14 | `docs/desktop-integration` merged with `origin/main` (8 commits); conflicting deletions from main kept; recovery report preserved | verified — merge commit, tree clean |
| 15 | `requirements.txt` pointed at a workspace-root file that does not exist; replaced with an installable toolchain list | verified — `pip install -r` in a fresh venv imports pytest, ruff, PyInstaller, keyring, websockets |

## 5. CI results recorded in this session

| Repo | Branch | Commit | Workflow | Conclusion |
|---|---|---|---|---|
| RISARMS-ui | `feat/risarms-ui-desktop` | `1bdbeea` | CI (3.10–3.14) | **success** |
| TIVISS | `fix/ci-test-dependencies` | `2ec78e1` | CI (3.11–3.13) | **success** |
| ASCS | `fix/doctor-offline-smoke` | `c2f4464` | CI (3.12/3.13, Windows, smoke×3) | **success** |
| RESCS | `fix/cli-configuration-diagnostics` | `cdbd6fa` | CI (3.11–3.13) | **success** |
| CORE | `feat/desktop-control-channel` | `4720e69` | CI (3.10–3.14) | see §6 |

Job-level logs remain unreadable here (no `gh`, anonymous log download is 403),
so conclusions come from the runs API, which is authoritative for pass/fail.

## 6. Remaining blockers

1. **Installer artifacts** — needs a Tk-enabled Python ≥3.10 or a CI dispatch.
2. **CORE feature-branch CI conclusion** — the run was still queued when this
   document was written; re-check the runs page.
3. **Pull requests** — cannot be created without authentication; compare links
   are listed in [recovery-2026-11-13.md](recovery-2026-11-13.md) §10.
4. **Hardware validation** — no HP CORE-HOST, second desktop, LAN/TLS chain or
   24-hour run was available.
5. **Display-dependent behaviour** — window rendering, keyboard navigation and
   the sync guard's timer interaction cannot be exercised without Tk.
