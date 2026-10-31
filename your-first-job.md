# Your first job

By the end of this chapter a real job exists, has run, and
has kept its result: the check is a small text file Jenkins
hands back to you, made by the build, containing a marker
only the build could have written.

## The project: Orbit Widgets

Jenkins needs something to build, so the lab invented a
project small enough to see whole. **Orbit Widgets** is a
folder in git with three files (all in `jenkins-lab/`):

- `VERSION` — one line: `1.4.0`
- `build.sh` — the build: it writes a `dist/release.txt`
  saying what was built and when, and prints
  `Build complete: orbit-widgets 1.4.0`
- `Jenkinsfile` — which chapter 7 is about; ignore it here.

Your own first job should be equally plain: a project with
one command that obviously works or obviously fails. You
are testing Jenkins, not the project.

## Freestyle: the form-filling job

A **freestyle** job is configured in Jenkins' web pages:
a name, some optional source settings, some **build steps**
(commands to run), and some **post-build actions** (what to
keep). The lab created its job — `hello-build` — through
the API rather than the mouse, but the XML it sent
(`jenkins-lab/hello-build-config.xml`) is exactly what the
web form would have saved, and its heart is one build step:

```sh
rm -rf src
git clone /path/to/fixture-repo src
cd src
./build.sh
```

plus one post-build action: **archive the artifacts**
matching `src/dist/**` — copy those files out of the
workspace into the build's permanent record.

In the web UI the same job is five minutes of clicking:
**New Item → Freestyle project**, add build step
**Execute shell**, add post-build action **Archive the
artifacts**. Everything else on the long freestyle form —
the parameters, the quiet periods, the notifications — is
for later; a first job deserves to be boring.

## Running it

Press **Build Now** (or, as the lab did, POST to
`/job/hello-build/build` — with the crumb, chapter 4).
Jenkins queues the build, an executor picks it up, and
build **#1** appears in the job's history. The lab's first
attempt taught a lesson before it taught anything else:
the build sat in the queue — *Waiting for next available
executor* — because the built-in node had taken itself
**offline**: Jenkins' disk-space monitor had found the
machine's tiny temporary-files partition below its 1 GB
comfort threshold and refused to start work on a "full"
disk that was not full. Restarting Jenkins with its
temporary directory pointed at a roomy disk
(`-Djava.io.tmpdir=…`) fixed it, and the queued build ran
by itself the moment the node came back. Transcript `t05`
keeps the monitor's own log line; chapter 16 keeps the
lesson. The moral for a first job: *if a build waits
forever, look at the node, not the job.*

## The result

Build #1, whole and entire (transcript `t04`):

```text
result: SUCCESS
duration_ms: 545
artifacts: ['src/dist/release.txt']
```

and the artifact, fetched back from the finished build:

```text
ORBIT-WIDGETS BUILD MARKER
orbit-widgets version 1.4.0
built at 2026-10-30T23:30:40Z
```

Half a second of work — small projects build fast — but
every idea in this guide is present in it: a job definition,
a queued run, an executor, a workspace, commands, a result,
and an artifact kept after the fact. The next chapter
teaches you to read the record Jenkins kept, because that
record — the console output — is where Jenkins explains
every success and every failure from now on.
