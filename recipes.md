# Recipes

Small, complete jobs for a Jenkins you now understand.
Each names its road: the ones the lab drove are marked
live; the form-based ones follow the same screens chapters
5 and 8 used.

**Nightly build of a pipeline** (in the Jenkinsfile):

```groovy
pipeline {
    agent any
    triggers { cron('H 2 * * *') }
    options { buildDiscarder(logRotator(numToKeepStr: '14')) }
    stages { /* …as chapter 7… */ }
}
```

`H` spreads the minute so your fleet of jobs does not fire
at 02:00 sharp; the discarder keeps the disk honest
(chapter 12).

**Keep old builds from eating the disk** (freestyle):
open the job, tick **Discard old builds**, set days or a
count — 20 builds is a sane default for a busy job. Do it
at creation time; chapter 12 explains why the folder
grows.

**Copy a job instead of rebuilding it**: from the job page,
**New Item** → name the new one → **Copy from** the old.
Via the API, the same trick the lab used: GET the job's
`config.xml`, POST it to `createItem` under a new name
(with a crumb) — which is also how you keep job definitions
in git as plain files, as this guide's lab does
(`jenkins-lab/hello-build-config.xml`).

**Ask about a build from the command line** (live — this
shape of call appears throughout the lab's transcripts):

```console
$ curl -s -u you:TOKEN \
  'http://localhost:8080/job/orbit-pipeline/lastBuild/api/json?tree=result,duration'
{"result":"SUCCESS","duration":…}
```

`lastBuild` can be `lastSuccessfulBuild` or a number;
`tree=` picks the fields. This is the call a dashboard, a
chat bot, or a desk display makes to ask "is it green?".

**Fail loudly when the marker is missing.** A build that
prints the wrong thing is worse than one that fails. End
fragile steps with a check — in shell,
`grep -q 'Build complete' out.txt` — so SUCCESS actually
means the work happened. (The lab's builds were checked
exactly this way: the marker line in the console, and the
artifact fetched back.)

**Never let a secret near the console.** Wrap secret use
in `withCredentials` (chapter 9), prefer `-p` flags read
from the environment over secrets in the command text —
command text is echoed into logs — and rotate anything
that does leak. The console forgets nothing.

**Back up before you upgrade.** Copy JENKINS_HOME
(chapter 12), *then* swap the war or update plugins. A
downgrade is "stop, put the folder back, start" only if
the copy exists.

**Give a job a description.** One sentence, in the job's
own description field, saying what it builds and whose it
is. Six months from now this is the difference between a
tool and an archaeological site. The lab's pipeline job
carries one; yours should too.
