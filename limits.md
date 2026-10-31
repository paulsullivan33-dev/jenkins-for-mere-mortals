# Limits

An honest chapter: what Jenkins cannot do, what it does
awkwardly, and when to choose something else. The lab met
several of these personally; none of them are reasons to
avoid Jenkins, and all of them are reasons to choose it
with open eyes.

**One controller, one point of failure.** The classic
Jenkins design has a single controller holding all state.
If it stops, builds stop and history is unavailable until
it returns. High-availability controllers exist
(commercially, and via careful storage tricks), but they
are not the free download's nature. Your mitigation is
chapter 12: the whole of Jenkins is one folder, restorable
in minutes on another machine.

**You are the operations team.** Updates, plugin updates,
Java updates, disk growth, the machine itself: yours.
Hosted CI exists precisely to sell this burden away. If
your repositories live on a code host with its own CI and
nothing needs your private network, the hosted road may
honestly be the better one — the sibling guide *GitHub
Actions for Mere Mortals* teaches it.

**Configuration is history, not tidy code.** Job
definitions are XML files in JENKINS_HOME — precise,
backable-up, and not how a human would choose to write
them. Pipelines move the *recipe* into the repository,
which solves the important half. For the rest — global
settings, security, plugin lists — the ecosystem's answer
is the **Configuration as Code** plugin (JCasC: one YAML
file describing the controller), taught here only as a
pointer: know it exists before your Jenkins grows a second
administrator.

**Plugins vary.** The catalogue is a commons: most plugins
are excellent, some are abandoned, a few have been the
subject of security advisories. The core's discipline —
signed catalogue, advisory warnings, health reporting —
helps, but the judgment "install few, maintained, popular"
(chapter 10) remains yours to exercise.

**Scaling is stepwise.** Beyond a few dozen busy jobs,
Jenkins wants agents (chapter 11), a bigger controller,
and thought about where build records accumulate. It
scales — very large estates run on it — but each step is
a project, not a toggle.

**The interface shows its age.** Jenkins' web UI is dense,
two decades of features deep, and the modernised views are
still arriving. Everything is *findable*, and the API
underneath is consistent and scriptable — this lab did
nearly everything through the API for that reason — but a
newcomer should expect to search the interface a few times
before its geography sticks.

**Builds run as Jenkins' user.** Unless agents, containers,
or per-job sandboxing say otherwise, a job's commands have
the filesystem rights of the Jenkins process. That is the
flip side of "if it can be typed, Jenkins can run it":
type carefully, and give the Jenkins user no more of the
machine than the jobs need.

None of these stopped the lab, and for a self-hosted,
reach-anything, no-per-build-bill automation server they
remain a fair price. The point of this chapter is that the
price is real, quoted, and yours to accept on purpose.
