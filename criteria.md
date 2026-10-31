# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The fixture is an invented widget project; the lab accounts
   and its one dummy credential are throwaways, labelled as such.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 15 names what the tool
   cannot do: one controller as a single point of failure,
   operations that stay yours, XML configuration, plugins of
   varying quality and maintenance, stepwise scaling, an
   ageing interface, and builds that run with Jenkins' own
   permissions unless you separate them onto agents.
8. **The ethics rule is in the text, early.** Jenkins is
   machinery for running other people's code on your machine,
   so the safety line is drawn where it belongs: chapter 9
   states the never-echo-a-secret rule and the rotate-on-leak
   rule, chapter 13 makes the case that a job definition *is*
   code execution and that build privileges must be granted
   like it, and no real credential appears anywhere in this
   guide — the single stored credential is an invented dummy,
   used to prove the store never shows secrets back.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a small shared Linux sandbox (about
7 GB of memory, several other labs running alongside), so
boot timings are given as ranges and the guide says so.
Jenkins **LTS 2.580.2** ran from the genuine `jenkins.war`,
downloaded from `get.jenkins.io` with its published SHA-256
verified (`d98032d2…be3251`, transcript t00), on **OpenJDK
21.0.12.1**. All transcripts live in
`jenkins-lab/transcripts/`; the fixture and job definitions
are `jenkins-lab/Jenkinsfile`, `build.sh`, `VERSION`,
`hello-build-config.xml` and `orbit-pipeline-config.xml`;
the setup scripts are `lab-admin-init.groovy`,
`lab-proxy-init.groovy` and `resolve_plugins.py`.

Two environment events are disclosed because they shaped
chapters. First, the machine's pre-installed Java **vanished
mid-lab** (the sandbox image was replaced under the running
work). Java was restored by the distribution route: the
`openjdk-21-jdk-headless` and `openjdk-21-jre-headless`
packages were downloaded as `.deb` files and *extracted*,
not installed. Ubuntu's packages point their configuration
files at absolute paths under `/etc`, so the extracted
tree's symlinks were replaced with the packages' own
extracted `/etc` copies; and the JRE shipped with **no
certificate bundle at all**, which the lab rebuilt from the
system CA bundle with `keytool` — learning, with a diagnostic
program as witness, that the store must be **JKS** (121 root
certificates visible to the JVM's password-less load) and
not PKCS12 (0 visible). Chapter 16 tells this as the
troubleshooting entry it genuinely is; the same failure
reaches any reader who assembles Java by hand.
Second, the sandbox's network: direct bulk downloads from
Java stalled while the same file arrived in seconds through
the sandbox's proxy — the update-centre story in chapter 10
is reported with its measurements, not smoothed over.

Run for real, with transcripts as evidence:

- Download and checksum of the war, and the version inside
  it confirmed at startup (t00).
- Plain first boot: startup log, unlock page served, the
  initial administrator password generated — redacted in the
  transcript before it entered this repository, and the
  redaction re-verified by searching the finished checkout
  for password-shaped strings (t01).
- Scripted setup: `-Djenkins.install.runSetupWizard=false`
  plus an init script creating the admin account from
  environment variables; wrong password → 401, no password →
  403, right password → the API (t02).
- CSRF: a job-creating POST without a crumb refused (403),
  the same POST with a crumb accepted (t03).
- Freestyle job `hello-build`: three builds — #1 SUCCESS
  with its artifact fetched back (t04), #2 FAILURE on the
  previous build's leftover checkout, kept verbatim (t06),
  #3 SUCCESS after the one-line fix — plus the queue detour:
  Jenkins' disk-space monitor took the node offline over a
  512 MB `/tmp`, and the build ran once `java.io.tmpdir`
  pointed at a roomy disk (t05).
- The real JENKINS_HOME tree, before and after plugins:
  configuration, jobs, users, secrets, workspaces, and the
  56 plugin files, with sizes (t05).
- Plugins: the update-centre check's behaviour measured
  three ways (t08), then the dependency closure of
  `workflow-aggregator` and `git` computed from the real
  catalogue — 56 plugins — downloaded, loaded after restart
  with **zero failures**, and confirmed through the plugin
  manager API (chapter 10).
- Pipeline job `orbit-pipeline` reading its Jenkinsfile
  from the fixture git repository: #1 FAILURE on the Git
  plugin's local-checkout safety guard, kept verbatim (t09);
  #2 SUCCESS after the named system property was set, with
  the full stage-by-stage console and its archived artifact
  (t10); #3 started **by polling** after a one-line commit,
  cause "Started by an SCM change", building the bumped
  version (t11).
- Credentials: a labelled dummy credential created in the
  global store; the API returning its metadata without the
  secret; the on-disk value shown to be an encrypted blob
  (t12).
- Clean shutdown via `POST /exit`, with the port verified
  released and no process remaining (t13).

Documented-only, and labelled as such where they appear:

- The graphical **setup wizard** — described in chapter 4;
  the lab drove the scripted route instead (the wizard's
  plugin step is the same update centre chapter 10 ran).
- **Package and container installs** — chapter 3 installs
  the war live; the `.deb`/container routes are described
  from the official download pages.
- **Agents** — chapter 11 entirely: no second machine was
  available to the lab, so SSH/inbound/cloud agent routes
  are taught from the documentation.
- **Webhooks** — chapter 8: the lab's Jenkins had no
  incoming path from a code host, so polling is the proven
  trigger and webhooks are the explained one.
- **Credential binding in a running pipeline**
  (`withCredentials`) — chapter 9 proves the store (creation,
  non-disclosure, encryption at rest) and shows the standard
  binding pattern from the plugin's documentation rather
  than a live upload.
- **Configuration as Code, multibranch pipelines, backup
  plugins, matrix authorization grids** — pointed to and
  characterised, not configured; the manual backup they
  automate (copying JENKINS_HOME) is proven by the tree in
  t05 and the restore logic in chapter 12.

One judgement call to record: the Git plugin's
local-checkout guard was relaxed in the lab
(`ALLOW_LOCAL_CHECKOUT=true`) for the lab's own fixture
folder, after its error message named the property and its
reason. Chapter 7 presents that as what it was — a security
guard understood and consciously excepted on a disposable
machine — and recommends real remote URLs everywhere else.
