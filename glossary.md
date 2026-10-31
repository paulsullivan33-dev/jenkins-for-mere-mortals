# Glossary

**Agent** — a machine that runs builds on the controller's
orders, so the work happens away from the configuration,
credentials and history. Joined by SSH, inbound connection,
or a cloud plugin.

**Artifact** — a file a build publishes: Jenkins copies it
from the workspace into the build's permanent record, where
it survives workspace wipes.

**Build** — one run of a job: numbered, dated, and kept
with its console output, result, changes and artifacts.

**CI / CD** — continuous integration: building and testing
every change automatically, soon after it is made.
Continuous delivery: keeping the result always ready to
release, with release itself an automated step.

**Controller** — the Jenkins program and its machine: holds
configuration, jobs, history, users and credentials, serves
the web UI and API, and directs agents. (Older material
says "master".)

**Credentials** — Jenkins' stored secrets (passwords,
tokens, keys), kept encrypted in JENKINS_HOME, named by ID,
handed to builds only while they run, and never displayed
back by any Jenkins screen.

**Crumb** — the CSRF token Jenkins requires on every
state-changing request, fetched from `/crumbIssuer/api/json`
and tied to your session.

**Declarative pipeline** — the Jenkinsfile style that
describes stages and steps in a fixed structure
(`pipeline { agent … stages { … } }`). The other style,
*scripted*, is free-form Groovy.

**Executor** — a build slot on a node. Two executors run
two builds at once; further builds wait in the queue.

**Freestyle job** — a job configured in Jenkins' web forms;
its recipe lives inside Jenkins rather than in the project.

**Init script** — a Groovy file in
`JENKINS_HOME/init.groovy.d/` that Jenkins runs at every
startup; the scripted way to create accounts and set
configuration without the wizard.

**Jenkinsfile** — the pipeline recipe file at a project's
root, versioned with the code. Jenkins reads it at the
start of each build of a pipeline job.

**JENKINS_HOME** — the one directory holding everything
Jenkins knows: configuration, jobs, builds, users, secrets,
plugins. Backing it up is backing up Jenkins.

**Job** — a stored recipe: where code comes from, what to
run, what to keep, when to run it.

**LTS** — the long-term-support Jenkins line: a stabilised
release about every twelve weeks with backported fixes;
the one to install unless you need the newest weekly.

**Node** — any machine Jenkins can run builds on: the
built-in node (the controller itself) or an agent.

**Node monitor** — Jenkins' self-checks on a node (disk
space, temp space, clock, responsiveness); a failing
monitor can take a node temporarily offline.

**Pipeline job** — a job whose recipe is a Jenkinsfile,
fetched from the project's repository (or written in the
job form, for small experiments).

**Plugin** — a `.jpi` file in `JENKINS_HOME/plugins/` adding
a capability: job types, source systems, credential kinds,
notifications. Most of Jenkins arrives this way.

**Poll SCM** — a trigger that asks the repository on a
schedule whether anything changed, and builds only if so.

**Stage** — a named phase of a pipeline (`Build`, `Test`,
`Keep the result`), run in order and drawn as a column in
the stage view.

**Trigger** — whatever starts a build: a person, a clock,
polling, a webhook, another job.

**Update centre** — Jenkins' plugin catalogue and update
service: the signed list Jenkins downloads to know what
exists and what is newer than what you run.

**War file** — `jenkins.war`, the whole Jenkins program in
one Java archive: `java -jar jenkins.war` is an install.

**Webhook** — an HTTP call from a code host to Jenkins
("something was pushed"), starting builds without polling;
needs a network path from the host to your Jenkins.

**Workspace** — a job's working folder on a node, where
builds check out code and do their work. It persists
between builds unless something cleans it.
