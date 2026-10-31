# Freestyle and pipeline

By the end of this chapter you can read a Jenkinsfile and
say what will happen when it runs — and you will have seen
one run, staged and archived, by a Jenkins that read it
from the project's own repository. The check is the file
itself, below: cover the right-hand comments and narrate it.

## Two ways to keep a recipe

Chapter 5's freestyle job keeps its recipe **inside
Jenkins**: the configuration lives in Jenkins' own files,
edited through its pages. That is convenient for a first
job and a real liability afterwards: the recipe is not
versioned with the code, not reviewed with the code, and
not recoverable from the code if Jenkins is lost. Change
the project and the Jenkins-side recipe must be changed
separately, by hand, by someone who remembers.

A **pipeline** job keeps its recipe **inside the project**,
in a file named **Jenkinsfile** at the repository root.
Jenkins fetches the project, reads the file, and follows
it. The recipe is then reviewed, branched, and rolled back
with everything else. This is how most teams use Jenkins
now, and it is the form worth learning properly. Pipelines
arrive as plugins — in the lab, the 56-plugin Pipeline
family of chapter 10.

## The lab's Jenkinsfile, whole

This is the complete Jenkinsfile of Orbit Widgets, exactly
as committed (`jenkins-lab/Jenkinsfile`):

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh './build.sh'
            }
        }
        stage('Keep the result') {
            steps {
                archiveArtifacts artifacts: 'dist/**'
            }
        }
    }
}
```

Anatomy, outside in:

- **`pipeline { … }`** — the whole recipe, in the
  *declarative* style: you describe stages; Jenkins works
  out the rest. (A second, *scripted* style exists — plain
  Groovy code — flexible and harder to read; learn
  declarative first.)
- **`agent any`** — "run this on any available executor."
  This is where chapter 11's agents get named when a build
  needs a particular kind of machine.
- **`stages` / `stage('…')`** — the named phases, run in
  order, shown as columns in Jenkins' stage view. A stage
  that fails stops the pipeline; later stages are skipped
  and shown as such.
- **`steps`** — what a stage does. **`sh`** runs a shell
  command. **`archiveArtifacts`** is the same "keep these
  files" action the freestyle job used.

A pipeline job also gets one stage for free:
**Declarative: Checkout SCM** fetches the project before
your first stage runs.

## Running it (live)

The lab's pipeline job, `orbit-pipeline`, is defined by
`jenkins-lab/orbit-pipeline-config.xml`: a pipeline whose
definition is "the Jenkinsfile from this git repository."
Its first run failed in an interesting, modern way
(transcript `t09`):

```text
ERROR: Checkout of Git remote '…' aborted because it references
a local directory, which may be insecure. You can allow local
checkouts anyway by setting the system property
'hudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT' to true.
```

The lab's repository was a folder on the same machine, and
Jenkins' Git plugin refuses local-folder checkouts by
default — deliberately: on a shared controller, a job that
can read *any* local folder can read folders it has no
business reading. The guard is right; the lab's exception
was also legitimate (the folder was the lab's own fixture),
so Jenkins was restarted with the named property set, and
that decision — *a security guard, understood, then
consciously relaxed for a stated reason* — is the pattern
to copy. On a real setup, with the repository at an
`https://` or `ssh://` address, the question never arises.

Build #2 then ran end to end (transcript `t10`): checkout
of commit `edc406e`, the Build stage printing
`Build complete: orbit-widgets 1.4.0`, the archiving stage,
`Finished: SUCCESS`, and `dist/release.txt` in the build's
artifacts. Same marker as the freestyle job — deliberately:
the project did not change; only where the recipe lives did.

## Which should you use?

Freestyle for the genuinely small: one machine, one
project, one person who will remember the form. Pipeline
for anything a team touches, anything that must survive a
Jenkins rebuild, and anything whose recipe deserves review.
You can also grow into it: many real Jenkinsfiles began as
a freestyle job's steps, copied into a file.
