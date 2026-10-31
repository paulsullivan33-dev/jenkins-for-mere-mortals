# What Jenkins is

By the end of this chapter you can say what problem Jenkins
solves, in one sentence, without using the words "DevOps" or
"pipeline" — and check: if you can explain why "it worked on
my machine" is the disease Jenkins is the cure for, you have
the idea.

## The disease: works on my machine

Software is built in steps: fetch the source code, turn it
into a program, run the tests, package the result. On one
person's machine those steps live in that person's memory.
A file they forgot to share, a tool only they installed, a
command they always run first — any of these makes the
build pass for them and fail for everyone else, including
the machine that has to ship it.

**Continuous integration (CI)** is the discipline that fixes
this: every change to the code is fetched by a neutral
machine, built from scratch, and tested, as soon as it is
made — so a breakage is found in minutes, by the person who
just caused it, instead of weeks later by someone else.
**Continuous delivery (CD)** extends the same idea: the
packaged result is always ready to release, and releasing
it is one more automated step rather than a ceremony.

CI/CD is a habit, not a product. Jenkins is the machine
that carries the habit out.

## What Jenkins does

Jenkins is a program that waits for work and then follows
recipes:

- You define **jobs**: "fetch this project, run these
  commands, keep these files as the result."
- Jenkins runs a job when told to — by a person clicking a
  button, by a clock, by noticing the code changed, or by
  another system knocking on its door.
- Each run is a **build**, numbered and kept: what started
  it, how long it took, everything it printed, whether it
  succeeded, and the files it produced.
- Jenkins shows all of this in a web page, and offers it
  through an API, so other tools can ask "did the last
  build pass?" without a human opening a browser.

That is the whole job description. Jenkins does not know
how to compile your language or test your framework — it
runs the same commands you would run, in the same order,
and keeps the receipts. The knowledge lives in the recipe;
Jenkins supplies the discipline, the memory, and the
audience.

## Where it came from, and where it fits

Jenkins began in 2004 as Hudson, a Sun Microsystems
project, and was renamed Jenkins in 2011 after a dispute
over the name; it is free software (MIT licence) stewarded
by the Continuous Delivery Foundation. It became the
default CI server of the 2010s, and a great deal of the
world's software has passed through it.

Its neighbours divide roughly by where the work runs:

- **Hosted CI** (GitHub Actions, GitLab CI, CircleCI) runs
  on the code host's machines. Nothing to install; the
  recipe lives in the repository; you rent the discipline
  instead of owning the machine. The sibling guide,
  *GitHub Actions for Mere Mortals*, teaches that world.
- **Jenkins** runs on a machine you control. That costs you
  the running of it — installs, updates, backups — and buys
  you two things hosted services cannot: it can reach
  anything on your own network, and it is not priced per
  build. Inside a company network, behind a firewall, or
  on a home workbench, that trade is often the whole
  decision.

Jenkins is also **general-purpose** in a way its rivals are
not: a job can run any commands at all, so people use it to
rebuild documentation overnight, mirror repositories,
rotate backups, and poke other systems on a schedule. If it
can be typed at a command line, Jenkins can be made to do
it, remember it, and show you the log.

## What Jenkins is not

- **Not a build tool.** It does not compile anything itself;
  it runs your compiler, your test runner, your script.
- **Not a code host.** Projects live in git (or another
  version control system); Jenkins fetches them.
- **Not magic about secrets or safety.** It has a proper
  credential store — chapter 9 — but a recipe that prints
  a password prints it to a log Jenkins keeps. Chapter 13
  covers the few settings that matter.
- **Not zero-maintenance.** Chapter 16 is honest about the
  cost: you own the updates, the plugins, and the backups.

The next chapter names the parts, so that everything after
it — installs, jobs, failures — has somewhere to live.
