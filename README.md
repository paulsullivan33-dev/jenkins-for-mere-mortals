# Jenkins for Mere Mortals

Every programmer knows the moment. The code works on your
machine, you send it to everyone else, and it breaks — a file
forgotten, a library missing, a step only you knew about.
**Continuous integration** is the habit of letting a neutral
machine do the boring, breakable steps every single time:
fetch the code, build it, test it, and report honestly.
**Jenkins** is the best-known machine for that job — a free,
open-source **automation server** that has been running
builds since 2011 (and before that as Hudson). You give it
**jobs** — recipes that say "check out this project, run
these commands, keep these results" — and Jenkins runs them
when you ask, on a schedule, or when the code changes,
keeping the full history of what happened each time.

This guide explains Jenkins in plain terms: what a job, a
build, and a pipeline actually are, how to install Jenkins
from its single downloadable file, how to set it up, and how
to run real work through it. The centrepiece is a tiny
invented project, **Orbit Widgets**, which the lab builds
twice — once with a point-and-configure job, and once with
a **Jenkinsfile**, the recipe file that lives in the project
itself and is the way most teams use Jenkins today.

The lab behind this guide ran the real thing: **Jenkins LTS
2.580.2**, downloaded from the official mirror with its
published SHA-256 checksum verified, running on **OpenJDK
21**. It booted Jenkins from scratch, set it up without
clicking through the wizard, created both kinds of job,
watched builds succeed, and — just as usefully — watched
three builds fail for three different, ordinary reasons,
each one kept in the transcripts exactly as it happened:
a build that waited because Jenkins thought the disk was
full, a build that failed because a previous build's files
were still in the way, and a pipeline refused permission
to read a folder on its own machine. The lab also installed
**56 plugins** (the whole Pipeline family and Git), stored
a dummy credential and proved Jenkins never shows it back,
and let Jenkins notice a code change by itself and start a
build nobody asked for.

What the lab could not do, it did not fake. Nobody clicked
through the graphical setup wizard, so the wizard itself is
described, not demonstrated. Build agents — extra machines
that do the work — are explained from the documentation.
Webhooks from a code host need a network path this lab
does not have, so they are taught honestly as a diagram and
a set of steps. `criteria.md` keeps the full ledger of what
was run and what was only read.

## What this guide covers

- [**What Jenkins is**](what-jenkins-is.md) —
  continuous integration and continuous delivery in plain
  terms, where Jenkins fits, and what it is not
- [**The moving parts**](the-moving-parts.md) —
  the controller, jobs, builds, executors, workspaces,
  artifacts, and the one folder — JENKINS_HOME — that
  holds all of it
- [**Installing Jenkins**](installing-jenkins.md) —
  the war file, the checksum that proves it is genuine,
  the Java it needs, and the package and container
  alternatives
- [**First boot and setup**](first-boot-and-setup.md) —
  the unlock password, the setup wizard, and the scripted
  route that skips both: an init script that creates the
  admin account at startup
- [**Your first job**](your-first-job.md) —
  a freestyle job that fetches a small project, builds it,
  and keeps the result — created and run for real
- [**Reading a build**](reading-a-build.md) —
  console output line by line, the result words (SUCCESS,
  FAILURE, UNSTABLE), artifacts, and how a failed build
  explains itself
- [**Freestyle and pipeline**](freestyle-and-pipeline.md) —
  the two kinds of job, the anatomy of a Jenkinsfile,
  and a pipeline read from the project's own repository
- [**Triggers**](triggers.md) —
  starting builds by hand, on a timer, by polling the code
  for changes (proven live), and by webhook (explained
  honestly)
- [**Credentials and secrets**](credentials-and-secrets.md) —
  Jenkins' own credential store, why secrets stay encrypted
  and are never shown back, and the rule: never echo a
  secret into a build log
- [**Plugins**](plugins.md) —
  how plugins supply most of Jenkins' abilities, the update
  centre, and what this lab's network taught about
  installing them
- [**Agents**](agents.md) —
  why builds should not run on the controller, and the ways
  extra machines join in — taught from the documentation
- [**Backups and housekeeping**](backups-and-housekeeping.md) —
  the real JENKINS_HOME tree from the lab, why backing it up
  is the whole backup, and the disk-space monitor that
  guards it
- [**Security basics**](security-basics.md) —
  accounts and permissions, the CSRF crumb the lab met on
  its first form post, and the few settings that matter most
- [**Recipes**](recipes.md) —
  a nightly build, throwing old builds away, copying a job,
  checking a build from the command line, and more
- [**Limits**](limits.md) —
  one controller doing everything, XML files instead of
  tidy configuration, plugin quality that varies, and the
  honest cases for a hosted service instead
- [**Troubleshooting**](troubleshooting.md) —
  the node that took itself offline, the checkout that was
  refused, the workspace that kept yesterday's files, and
  the other traps this guide's lab fell into
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Running Jenkins for a large organisation: hundreds of
agents, high-availability controllers, and the commercial
distributions built on top of Jenkins are their own subject.
Deep build tooling — Maven, Gradle, npm, Docker builds —
belongs to those tools' own guides; here they appear only
as commands a job can run. Configuration as Code and the
Jenkins CLI are pointed at, not taught in full. And this
guide never puts a real password, token, or key anywhere:
the one credential it creates is a labelled dummy, used to
prove the store keeps secrets secret.

## How to use this guide

Read chapter 1 for the model and chapter 2 before
installing anything — knowing which part holds what turns
later confusion into a named problem. Chapters 3 and 4 get
you a running Jenkins with an admin account; chapter 5
builds something real in the same sitting. Chapter 6 is
worth reading slowly: the console output is how Jenkins
explains everything, including every failure you will ever
meet. The lab's transcripts live in
`jenkins-lab/transcripts/`; the fixture project files are
`jenkins-lab/Jenkinsfile`, `jenkins-lab/build.sh` and
`jenkins-lab/VERSION`, the two job definitions are
`jenkins-lab/hello-build-config.xml` and
`jenkins-lab/orbit-pipeline-config.xml`, and the setup
scripts are `jenkins-lab/lab-admin-init.groovy` and
`jenkins-lab/resolve_plugins.py`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Git for Mere Mortals](https://paulsullivan33-dev.github.io/git-for-mere-mortals/)
- [GitHub Actions for Mere Mortals](https://paulsullivan33-dev.github.io/github-actions-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/jenkins-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/jenkins-for-mere-mortals/blob/main/LICENSE-CODE).
