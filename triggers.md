# Triggers

By the end of this chapter you can start a build four
ways and choose between them on purpose. One of them —
polling — is proven live here: the lab committed a change
and Jenkins started build #3 by itself, with the cause
written in its record: *Started by an SCM change*.

## By hand

**Build Now** on the job page; `POST /job/<name>/build`
with a crumb from a script (chapter 4). Manual builds are
how you learn, and how you re-run after fixing something.
A job can also declare **parameters** — values asked for at
build time (a version to release, a branch to build) —
which turn Build Now into a small form.

## By clock

Freestyle jobs offer **Build periodically**; pipelines
take a `triggers { cron('…') }` block in the Jenkinsfile.
The schedule is cron syntax with one Jenkins kindness:
`H` in a field means "a hashed, spread-out minute" —
`H 2 * * *` is "nightly, at some minute past 2 chosen
steadily for this job", so a hundred jobs do not all fire
at 02:00 sharp. Use `H` unless you truly need a fixed
minute. Clock builds suit nightlies, mirrors, and reports:
work that should happen whether or not the code changed.

## By polling (proven live)

**Poll SCM** is the same schedule with a question attached:
at each tick, Jenkins asks the repository "anything new
since the last build?" and builds only if the answer is
yes. The lab set the pipeline job to poll every minute —
lab pace; real projects use five to fifteen — then
committed a change to the fixture (VERSION 1.4.0 → 1.4.1,
commit `b49aa94`). Without anyone touching Jenkins
(transcript `t11`):

```text
cause: Started by an SCM change
Build complete: orbit-widgets 1.4.1
```

Polling's costs are real: Jenkins must reach the
repository on every tick, and the delay between a commit
and its build is up to one interval. Its virtue is that it
works anywhere the repository is reachable — no incoming
connections to Jenkins required — which is why it remains
the workhorse behind firewalls.

## By webhook (described honestly)

The natural alternative: the code host notices the push
and *calls Jenkins* — an HTTP POST to a job-specific
address (the GitHub plugin's is `/github-webhook/`). The
build starts in seconds and no polling traffic exists.
The requirement is the catch: the host must be able to
**reach** your Jenkins. A Jenkins on a home or office
network, invisible from the internet, cannot receive
GitHub's call — the lab's Jenkins was exactly such a
machine, so this guide teaches webhooks as a diagram and
does not pretend to have run one. The recipe, for a Jenkins
that *is* reachable: install the code host's plugin, tick
the job's "build when a change is pushed" trigger, add the
webhook in the repository's settings pointing at
`<your-jenkins>/github-webhook/`, and make one test commit.

## Choosing

| You want… | Use |
|---|---|
| to learn, or to re-run after a fix | by hand |
| nightly work regardless of changes | the clock |
| builds after changes, Jenkins unreachable from outside | polling |
| builds after changes, Jenkins reachable | webhook |

Everything above can also be combined with quiet rules —
a **quiet period** (wait a few minutes after a change, in
case more commits are coming) and per-branch behaviour in
multibranch pipelines — but the four ways are the whole
vocabulary. Builds that start themselves need secrets
handled with care, which is the next chapter.
