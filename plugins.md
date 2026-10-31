# Plugins

By the end of this chapter you know what a plugin is, where
they come from, and how the lab got 56 of them installed
on a network that fought back — so you can recognise each
part of that story if it ever happens to you.

## What plugins are

A plugin is a file — `something.jpi` in
`JENKINS_HOME/plugins/` — that teaches Jenkins a new trick:
a job type, a source system, a notification channel, a
credential kind, a whole dashboard. The core is small by
design; nearly everything chapters 5–9 used beyond plain
shell steps arrived as plugins. Git support, pipelines,
credential binding, your code host's webhooks: plugins.
There are over a thousand in the catalogue, maintained by
the Jenkins project and by volunteers and vendors.

Plugins depend on other plugins. Asking for "Pipeline"
brings a family — in the lab's case the Pipeline suite
plus Git came to **56 files, about 41 MB** — because a
pipeline needs its parser, its step libraries, its
visualisers, each separately versioned. This is normal;
the update centre works it out for you.

## The update centre

**Manage Jenkins → Plugins** is the shop front. It talks
to the **update centre**: a catalogue file (a few megabytes
of JSON, listing every plugin, its versions, and its
dependencies) that Jenkins downloads and checks against a
signature from the Jenkins project — so a tampered
catalogue is refused. **Available** lists what you could
install; **Installed** what you have; installing ticks the
boxes, downloads the files, and usually wants a restart.
Checking for updates is the same machinery on a schedule,
which is why chapter 4's log mentioned "check updates
server" at every boot.

Scripted installs exist too: the **Jenkins plugin
installation manager tool** (`jenkins-plugin-manager.jar`)
takes a list of plugin IDs and a war file, and prepares a
plugins folder offline — the route used for container
images and reproducible setups.

## The lab's story (honest version)

This lab's Jenkins could not fetch its catalogue the
ordinary way, and the reason is instructive. Jenkins first
failed every HTTPS call with
`the trustAnchors parameter must be non-empty` — the Java
installation underneath it had **no certificate bundle at
all**, so it trusted nobody (chapter 16 tells how that was
rebuilt). With trust repaired, a small HTTPS file fetched
fine from Java, but the multi-megabyte catalogue download
**stalled mid-body** on the lab network's direct route —
while the same file arrived in 8 seconds through the
network's proxy (3,484,863 bytes; transcript `t08` keeps
the measurements). Jenkins' own check, set to use the
proxy, did land its catalogue eventually — on the order of
ten minutes. The install itself was finished the manual
way: the catalogue JSON was read directly, the dependency
closure of `workflow-aggregator` and `git` was computed
from it (56 plugins — the script is
`jenkins-lab/resolve_plugins.py`), the files were fetched
as ordinary downloads into `plugins/`, and Jenkins was
restarted. The plugin manager's answer, in full:

```text
plugins loaded: 56
failed to load: 0
has workflow-job: True
has git: True
```

On an ordinary connection none of this chapter's second
half happens to you: you tick boxes and restart. But if
plugin installs ever hang on your network, you now know the
three places to look — Java's trust, the size of the file,
and whether Jenkins knows about your proxy
(**Manage Jenkins → Plugins → Advanced** holds its proxy
settings).

## Living with plugins

Install few, on purpose: every plugin is code running with
Jenkins' privileges, written to varying standards. Prefer
the widely-used and maintained (the catalogue shows
install counts and health). Update in small batches, read
the security advisories — plugin vulnerabilities are the
commonest Jenkins security news — and remember chapter 12:
`plugins/` is part of JENKINS_HOME, so a backup of the
folder is a backup of your exact plugin set.
