# Installing Jenkins

By the end of this chapter Jenkins is downloaded, proven
genuine with its checksum, and ready to boot. The lab's
route — the single **war file** — is the one this chapter
runs live; the package and container routes are described
for the reader whose machine suits them better.

## What Jenkins needs

Jenkins is written in Java, so it needs a **Java runtime**:
the current long-term-support line (the 2.479+ series,
including the lab's 2.580.2) runs on **Java 17 or Java 21**.
Check before anything else:

```console
$ java -version
openjdk version "21.0.12.1" 2026-08-18
```

Memory is the other honest requirement. Jenkins idles in a
few hundred megabytes and grows with jobs and plugins; give
it a machine with 2 GB free if you can, more if builds share
the box. The lab ran it capped at 640–768 MB of heap
(`-Xmx640m`) on a small shared machine and it behaved —
builds included.

A caution the lab earned the hard way: Java installations
that are "almost" complete can run Jenkins while quietly
breaking its encrypted web traffic — the distribution's
certificate bundle is a separate piece (`ca-certificates-java`
on Debian/Ubuntu), and without it every HTTPS call Jenkins
makes fails with a baffling error. Chapter 16 tells that
story in full. If your Java came from your system's normal
packages, you already have it; just don't be surprised by
the failure mode if you ever assemble Java by hand.

## The download, and proving it

Jenkins publishes two flavours: weekly releases, and the
**LTS (long-term support)** line — a stabilised release
roughly every twelve weeks with backported fixes. Choose
LTS unless you have a reason not to. Both live at
`jenkins.io/download`, and the war file itself comes from
the mirror network at `get.jenkins.io`.

```console
$ curl -sLO https://get.jenkins.io/war-stable/2.580.2/jenkins.war
$ curl -sLO https://get.jenkins.io/war-stable/2.580.2/jenkins.war.sha256
$ cat jenkins.war.sha256
d98032d2401c540a35613a82ed358921fcf3166d5e6eaaaf60a7941845be3251  jenkins.war
$ sha256sum -c jenkins.war.sha256
jenkins.war: OK
```

The checksum is not ceremony. A war file is a program you
are about to give your build credentials to; the published
SHA-256 is how you know the program is the one the Jenkins
project shipped, not a copy that passed through extra hands.
The lab's exact session is transcript `t00`. One lab note:
the "latest LTS" pointer (`updates.jenkins.io`) answered
with the previous point release's number while the mirrors
already carried 2.580.2 — version pointers can lag a day
behind the files; the version *inside* the war (printed at
every startup) is the truth.

## The three ways to install

**The war file** (the lab's route) is one file, run
directly:

```console
$ java -jar jenkins.war --httpPort=8080
```

Nothing is installed system-wide; Jenkins unpacks what it
needs into JENKINS_HOME. Moving it means moving a file and
a folder. This is the best route for learning, for small
servers, and for anyone who wants to see the whole thing.

**System packages** (`.deb`, `.rpm`, Windows and macOS
installers, from the same download page) add a service that
starts at boot, a `jenkins` user, and standard paths
(JENKINS_HOME at `/var/lib/jenkins` on Linux). Choose this
for a machine whose whole job is Jenkins.

**A container** (`jenkins/jenkins:lts` in Docker) packages
the same war with its Java. Neat on a container host; the
one extra idea to learn is that builds *inside* the
container can only see what the container can see.
Described here, not run in the lab.

Whichever route: pick JENKINS_HOME before the first boot
and give it room. On the war route you choose it yourself:

```console
$ export JENKINS_HOME=$HOME/jenkins-home
```

The lab used an out-of-the-way directory and a
less-crowded port (18097, because small test ports were
already spoken for on that machine). On your own machine,
the default **8080** is fine, and the rest of this guide
uses it in examples.

Now boot it — the next chapter is waiting at the login page.
