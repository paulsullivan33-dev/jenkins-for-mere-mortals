# Backups and housekeeping

By the end of this chapter you can state Jenkins' entire
backup strategy in one sentence, and you have seen the
real folder it applies to. The sentence: **back up
JENKINS_HOME** — all of it, keys and all — because nothing
outside it matters and everything inside it does.

## The tree, from the lab

Transcript `t05` keeps the lab's own listing. In shape:

```text
JENKINS_HOME/
  config.xml                  the controller's settings
  jobs/<job>/config.xml       each job's definition
  jobs/<job>/builds/<n>/      each build: log, result, artifacts
  users/                      accounts
  credentials.xml             the credential store (encrypted)
  secret.key, secrets/        the keys that encrypt it
  plugins/                    one .jpi file per plugin
  workspace/<job>/            working folders (rebuildable)
  init.groovy.d/              startup scripts, if any
  nodeMonitors.xml, queue.xml the small state files
```

The lab's whole home was **66 MB** before plugins — most
of it the unpacked web application. Yours will grow with
build history: every console log and kept artifact is in
there, which is why the housekeeping below exists.

## Doing the backup

The honest method is a copy of the folder, taken while
Jenkins is stopped (or quiet), to somewhere that is not
the same disk. Two refinements:

- **Include the keys.** `credentials.xml` without
  `secret.key` and `secrets/` is a box of encrypted blobs
  nobody can open. A backup missing them restores a Jenkins
  that has forgotten every secret — chapter 9's lesson from
  the other side.
- **You may skip `workspace/`.** Workspaces are caches;
  jobs re-fetch and rebuild. Skipping them can cut a backup
  enormously. Everything else is the record.

Plugins exist to automate this (thinBackup is the classic:
scheduled copies of the configuration, optionally with job
records) — described, not run in the lab. The manual copy
is the floor: know it works before you automate it.
Restoring is the reverse: put the folder where JENKINS_HOME
points, start the same Jenkins version (or newer), and
everything — jobs, history, users, credentials — is back,
because none of it ever lived anywhere else.

## Housekeeping: keep the disk from filling

Jenkins watches its own disk. Its **node monitors** check,
among other things, free space in JENKINS_HOME and in the
temporary directory, against thresholds (1 GB by default).
A monitor that runs out of patience takes the node
**temporarily offline** rather than let builds die mid-write
on a full disk — which is precisely what the lab met from
the other direction: a machine whose `/tmp` was a 512 MB
partition could never satisfy a 1 GB threshold, so the
node refused all work until Jenkins' temporary directory
was pointed somewhere roomier (transcripts `t05` and
`t06`'s prehistory; chapter 16 has the diagnosis path).

The steady-state defences are boring and sufficient:

- **Discard old builds.** Every job has a log-rotation
  setting (keep the last *N* builds, or *N* days) —
  freestyle jobs in their main form, pipelines via
  `options { buildDiscarder(logRotator(numToKeepStr: '20')) }`.
  Set it when you create the job, not when the disk fills.
- **Archive less.** Artifacts are for keeps; build trees
  are not. Archive the release file, not the folder.
- **Watch the watchers.** A node that keeps going offline
  is telling you a disk is genuinely filling — usually
  build history or workspaces. Believe it early.
