# The moving parts

By the end of this chapter you can point at each of Jenkins'
ideas and say where it lives: on a screen, in an address, or
in a folder on disk. The check is the last section — a real
listing of the folder that holds an entire Jenkins, taken
from this guide's lab.

## The controller

Jenkins itself is one program, and the machine it runs on
is the **controller** (older guides say "master"; the word
changed, the thing didn't). The controller holds the
configuration, the job definitions, the build history, the
user accounts and the credentials. It also has a web server
built in: everything you do with Jenkins, you mostly do
through its web pages or the same machinery underneath,
its HTTP API.

The controller can also run builds itself, on its **built-in
node** — the lab in this guide does exactly that, because
one small machine is the honest way to learn. Chapter 11
explains why bigger setups hand the work to **agents**:
separate machines the controller directs. For now, one
sentence is enough: the controller decides, executors do.

## Jobs, builds, executors

A **job** is a stored recipe: where the code comes from,
what commands to run, what to keep, when to run. Jobs sit
on Jenkins' home page as a list. A **build** is one run of
a job — numbered (#1, #2, #3…), dated, and kept. A build
has a **result**: SUCCESS, FAILURE, UNSTABLE (it ran, but
something it checked — usually tests — reported trouble),
or ABORTED (someone stopped it).

Builds run on **executors**: slots. The controller starts
with two. Two executors means two builds can run at once;
a third waits in the **queue**, and Jenkins' home page shows
it waiting, with the reason ("Waiting for next available
executor" is a sentence you will meet in real life — this
lab did, in transcript `t04`'s prehistory, when the only
node had taken itself offline; chapter 12 tells that story).

Each job gets a **workspace**: a folder on disk where its
builds check out code and do their work. Workspaces persist
between builds, which is sometimes a feature (a cache) and
sometimes a trap (yesterday's files breaking today's build —
chapter 6 has the lab's real example).

Files a build wants to *publish* — the program it built,
the report it generated — are **artifacts**. Jenkins copies
them out of the workspace into the build's own permanent
record, so they survive even if the workspace is wiped.

## JENKINS_HOME: the folder that is Jenkins

Everything above lives in one directory, chosen by the
environment variable **JENKINS_HOME**. Inside it:

- `config.xml` — the controller's own settings
- `jobs/` — one folder per job, its configuration and its
  builds, each build with its log and its artifacts
- `users/` — one folder per account
- `secrets/` and `secret.key` — the keys that encrypt the
  credential store
- `credentials.xml` — the stored credentials, encrypted
- `plugins/` — the installed plugins, one file each
- `workspace/` — the jobs' working folders

Here is the shape of it, from the lab's own Jenkins after
its first builds (transcript `t05` has the full listing):

```text
home1/
  config.xml
  jobs/
    hello-build/
  users/
    labadmin_…/
  secrets/
    initialAdminPassword
    master.key
  workspace/
    hello-build/
```

Two consequences follow, and the rest of this guide leans
on both. First, **backing up Jenkins means copying that
folder** — chapter 12. Second, when something is wrong,
the truth is usually in that folder or in the log Jenkins
writes while it runs — chapter 16.

## Plugins: most of Jenkins is optional

A fresh Jenkins is deliberately small: it can run shell
commands, keep history, and not much more. Reading git
repositories, pipelines, most credential types, most ways
of notifying you — all of that arrives as **plugins**,
numbered in the thousands, installed from the **update
centre** inside Jenkins. Chapter 10 covers them; for now,
hold the shape: the core is the referee, plugins are the
players, and almost every error message that names a class
you have never heard of is a plugin asking for attention.
