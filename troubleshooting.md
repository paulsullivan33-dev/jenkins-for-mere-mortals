# Troubleshooting

Every entry here happened to this guide's lab (or sits one
step away from one that did), in the order you are most
likely to meet them. The general method underneath all of
them: read the console to the **first** error, read the
log for the minute the thing happened, and change one
thing at a time.

**A build sits in the queue forever — "Waiting for next
available executor."**
The executors are busy, or the node is offline. Look at
**Manage Jenkins → Nodes**: if the built-in node is
*temporarily offline*, Jenkins will tell you which monitor
did it. In the lab it was the **disk-space monitor**: the
machine's `/tmp` partition (512 MB) was below the 1 GB
temp-space threshold, so the node refused work on a disk
that was not actually full. Fixes, in order of honesty:
free real space; point Jenkins' temporary directory at a
roomier disk (`-Djava.io.tmpdir=/path/on/the/big/disk`);
or, knowingly, lower the monitor's threshold in the node's
monitor settings. Transcript `t05` keeps the exact log
line: *Making Built-In Node offline temporarily due to the
lack of disk space*.

**Second build fails where the first passed — "destination
path already exists" (or any leftover-file error).**
Workspaces persist between builds (chapter 6). Make the
recipe clean up after itself, use the job's SCM section
(which manages checkouts properly), or delete the workspace
before the build. The lab's fix was one line — `rm -rf src`
— and build #3 passed.

**Pipeline refuses a checkout — "references a local
directory, which may be insecure."**
The Git plugin will not check out from a folder path
unless you allow it (chapter 7). Prefer a real `https://`
or `ssh://` remote; for a genuinely local lab, start
Jenkins with `-Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true`,
knowing why the guard exists.

**POST requests get 403 while GET works.**
You are missing the **CSRF crumb**. Fetch one from
`/crumbIssuer/api/json` *with the same session cookies*,
and send it as the `Jenkins-Crumb` header. A crumb fetched
under one session does nothing under another — the lab's
transcripts (`t03`) show the refused-then-accepted pair.

**401 versus 403 at the API.**
401 means *bad credentials* — wrong username or password.
403 means *no credentials, or no permission*. The two
numbers separate "wrong key" from "no key"; the lab's
scripted-setup checks (chapter 4) rely on exactly that.

**Every HTTPS call fails — "the trustAnchors parameter
must be non-empty."**
Your Java has no certificate bundle. On Debian/Ubuntu the
bundle comes from **ca-certificates-java**; a hand-assembled
Java may lack it entirely. The subtle version, which the
lab diagnosed to the bottom (transcript `t07`): a trust
store in **PKCS12** format loaded the way the JVM loads
its default store (with no password) exposed **zero**
certificates, while the same certificates in a **JKS**
store exposed all 121 — which is why the system bundle is
JKS. Verify with any small Java HTTPS fetch before blaming
Jenkins.

**The update centre hangs; plugin installs never finish.**
Jenkins downloads a multi-megabyte catalogue before it can
offer anything (chapter 10). On restrictive networks the
direct route can stall while ordinary downloads through a
proxy succeed in seconds. Configure Jenkins' own proxy
(**Manage Jenkins → Plugins → Advanced**), give the check
time — the lab's took on the order of ten minutes — and
watch `JENKINS_HOME/updates/` for the catalogue landing.

**"Failed to start Jetty" at startup.**
Something already holds Jenkins' port — most often
yesterday's Jenkins, still running. Find the listener,
stop the old process cleanly (`POST /exit`, or kill the
*Java* process — on some setups a wrapper script takes
the signal and the JVM keeps the port; check the port, not
the pid you aimed at). Then start again.

**Jenkins won't start after an upgrade.**
Stop. Put back the JENKINS_HOME copy you took first
(chapter 14's rule), start the old version, and read the
release notes for what changed. An upgrade you cannot
reverse is not an upgrade, it is a wager.

**It's slow.**
Look for the ordinary causes before the exotic ones: many
kept builds (discard them), plugins checking in, a
workspace on a slow disk, builds running on the controller
alongside its web work. The log timestamps tell you where
the minutes went; Jenkins prints its readiness line —
*Jenkins is fully up and running* — so a slow boot is
measurable, not a feeling.
