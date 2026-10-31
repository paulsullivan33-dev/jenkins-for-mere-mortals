# First boot and setup

By the end of this chapter Jenkins is running, unlocked,
and has an administrator account you chose — reached by
either of two roads: the graphical wizard, described, or
the scripted road the lab drove, which you can repeat
character for character. The check at the end is the same
for both roads: wrong password refused, no password
refused, right password in.

## The first boot

Start Jenkins and watch its log. Two moments matter:

```text
Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:
[32 characters, printed once, in the log]
```

and, a little later, the line that means "ready":

```text
Jenkins is fully up and running
```

On the lab's small machine the first boot took about
85 seconds — Jenkins unpacks its web application into
JENKINS_HOME and generates its keys on that first run.
Later boots took 20–40 seconds. The initial password is
also kept in a file, `JENKINS_HOME/secrets/initialAdminPassword`,
readable only by the user Jenkins runs as. The lab's
transcript `t01` shows this boot with the password itself
**redacted** — a habit worth copying: a password that
appears in a log you share is a password you have given
away, even a temporary one.

Open `http://localhost:8080/` and Jenkins shows the
**Unlock Jenkins** page, asking for that password.

## The wizard road (described)

Paste the password in, and the setup wizard offers:
**Install suggested plugins** (the sensible default — it
installs the plugins most people need, including Git and
Pipeline, from the update centre), then creates your admin
account, then asks for the Jenkins URL (accept the default
unless you know yours differs). That is genuinely all of
it, and for a first personal install it is the right road.
This guide does not pretend the lab clicked through it:
the lab drove the second road, because a guide's lab must
be able to start over at 2 a.m. without a mouse — and
because the second road is the one you will want for any
Jenkins you rebuild more than once.

## The scripted road (the lab's, live)

Two switches change everything:

```console
$ JENKINS_HOME=$HOME/jenkins-home \
  java -Djenkins.install.runSetupWizard=false \
       -jar jenkins.war --httpPort=8080
```

`-Djenkins.install.runSetupWizard=false` says *do not wait
for a human at the wizard*. But then nothing creates your
admin account — that is the job of an **init script**.
Jenkins runs every Groovy script in
`JENKINS_HOME/init.groovy.d/` at startup, before it
declares itself ready. The lab's script (kept in full at
`jenkins-lab/lab-admin-init.groovy`) does three things:
reads a username and password from **environment
variables** (so the password is in no file), creates the
account, and turns on "logged-in users can do anything"
authorization so the new admin is truly an admin.

With that in place the lab could prove the setup from the
command line alone (transcript `t02`):

```console
$ curl -s -u labadmin:WRONG http://localhost:8080/api/json
401
$ curl -s http://localhost:8080/api/json
403
$ curl -s -u labadmin:RIGHT http://localhost:8080/api/json
{ ...the whole state of Jenkins, as JSON... }
```

**401** for a wrong password, **403** for none at all, and
the front door open for the right one: that trio is the
signature of a correctly locked Jenkins. (`labadmin` and
its password are the lab's throwaway pair, invented for a
machine that was deleted afterwards. Yours should be a
real password, kept the way you keep passwords.)

One more security feature introduces itself the first time
you *change* anything by script: Jenkins protects every
form post with a **CSRF crumb** — a token tied to your
session that proves the request came from its own pages
(or from someone who fetched a token first). The lab's
first attempt to create a job by API without one was
answered `403`, and succeeded once the crumb from
`/crumbIssuer/api/json` was attached (transcript `t03`).
Chapter 13 returns to this; file it now as: *reading is
open to your password, writing also wants the crumb.*

You now have a Jenkins with nobody's jobs in it. Time to
fix that.
