# Agents

This chapter is taught from the documentation, and says so:
the lab's Jenkins ran every build on its own built-in node,
because one machine was the honest way to learn everything
else in this guide. What follows is the model, the reasons,
and the routes — labelled as read, not run.

## Why agents exist

Chapter 2 introduced the split: the **controller** decides,
**agents** do. Three pressures push builds off the
controller:

- **Safety.** A build is arbitrary code from a repository,
  running with the permissions of whatever runs it. On the
  controller, that code sits next to Jenkins' credentials,
  keys, and configuration. On an agent, it sits next to a
  disposable workspace.
- **Capacity.** Builds are hungry and bursty. Agents let
  ten builds run on ten machines while the controller keeps
  answering web pages.
- **Variety.** One project needs Linux, another a Mac for
  an iOS build, a third a big machine for an hour. Agents
  carry **labels** (`linux`, `mac`, `gpu`), and a pipeline
  asks for what it needs: `agent { label 'mac' }`.

Each agent provides **executors** (build slots) and a root
folder for workspaces. The controller hands it work over a
connection and collects the console and artifacts back;
the build record lives on the controller either way.

## The ways an agent joins

- **SSH agents.** The controller connects to a machine over
  SSH, copies a small agent program, and runs it. The
  commonest route for permanent machines in a machine room
  or a home lab. Needs the SSH Build Agents plugin, an SSH
  credential (chapter 9's store holds it), and Java on the
  agent.
- **Inbound agents.** The agent reaches *out* to the
  controller (over a dedicated port) instead of being
  reached — right for machines behind NAT or in clouds
  where inbound SSH is not on offer. The agent is started
  by a command or a service on its own machine.
- **Cloud and container agents.** Plugins let Jenkins start
  an agent per build — a Docker container, a Kubernetes
  pod, a cloud VM — and throw it away afterwards. Every
  build gets a provably clean room (chapter 6's leftover
  problem, abolished), at the price of the machinery to run
  the cloud.
- **The built-in node.** The controller itself, with its
  executors settable — including to **zero**, which is the
  standard recommendation for any Jenkins beyond a learning
  lab: the controller should orchestrate, never execute.

## What doesn't change

Jobs, pipelines, triggers, credentials scoping, and the
console all behave identically wherever a build lands;
the console even names the machine in its second line
("Running on *agent-name* in …"). Moving a working lab from
this guide to an agent is an afternoon's configuration, not
a rewrite — which is exactly why learning on the built-in
node first is a legitimate road, as long as you know it is
the training-wheels configuration and not the destination.
