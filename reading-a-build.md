# Reading a build

By the end of this chapter you can open any finished build
and answer three questions from its record alone: what ran,
what it printed, and why it ended the way it did. The check
is the lab's failed build in the last section — you will be
able to name its cause from its log, unaided.

## The build page

Every build has a page: `/job/<name>/<number>/`. It shows
the result, when it started, how long it took, what started
it ("Started by user …", "Started by an SCM change"), its
**changes** (the commits it included, for code jobs), its
artifacts for download, and its **console output** — the
full text of the run. The console is the ground truth;
everything else is a summary of it.

## A successful console, line by line

The lab's first pipeline console is the clearest specimen
(transcript `t10` keeps all of it). The important lines:

```text
Started by user labadmin
Running on Jenkins in …/workspace/orbit-pipeline
Cloning the remote Git repository
Checking out Revision edc406e… (refs/remotes/origin/main)
+ ./build.sh
Build complete: orbit-widgets 1.4.0
Archiving artifacts
Finished: SUCCESS
```

Read it as a story with a fixed cast: Jenkins announces
the build, the node and workspace; the checkout reports
*which exact commit* it took — when a build surprises you,
that line is the first suspect; your commands appear with
a `+` in front (the shell echoing itself), their output
underneath; Jenkins' own actions (archiving, finishing)
close the tale. **Finished:** is always the last word, and
the word after it is the result.

The **result words** mean: **SUCCESS** — everything ran
and nothing reported trouble. **UNSTABLE** — everything
ran, but a checker (usually the test reporter) flagged
problems. **FAILURE** — a step failed; the build stopped
there. **ABORTED** — a person or a timeout stopped it.
**NOT_BUILT** — it never started, usually a queue casualty.

## The workspace, and why builds remember

Between builds, a job's **workspace** folder keeps whatever
the last build left there. Usually that is invisible. The
lab's *second* freestyle build made it visible
(transcript `t06`, kept verbatim):

```text
+ git clone /home/…/fixture-repo src
fatal: destination path 'src' already exists and is not an empty directory.
Build step 'Execute shell' marked build as failure
Skipped archiving because build is not successful
Finished: FAILURE
```

Build #1 had cloned the project into `src/` inside the
workspace and left it there; build #2's identical clone
command refused to overwrite it. Nothing about Jenkins was
broken — the *recipe* assumed a clean room that Jenkins
does not provide by default. The fixes are all ordinary:
delete the folder at the start of the step (the lab added
`rm -rf src`, and build #3 passed), or use the source
management section of the job, which manages its checkout
properly, or tick a "delete workspace before build" option
(where a plugin offers one). The general lesson is worth
more than the specific fix: **a build must be written to
survive its own leftovers**, because the second run is the
one that tells the truth about your recipe.

## Reading failure like a mechanic

When a build is red, the order of reading is: the
**Finished:** line confirms it failed; scan upward for the
**first** thing that looks like an error — later errors are
usually echoes; check whether the failing command is yours
(a step) or Jenkins' (a checkout, an archive, a plugin).
Yours means the recipe or the project; Jenkins' means the
machine or the configuration — and chapter 16 collects the
ones this lab met in the wild.
