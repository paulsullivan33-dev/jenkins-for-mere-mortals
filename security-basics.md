# Security basics

By the end of this chapter you know the handful of Jenkins
security settings that carry the weight, two of which you
have already met working: the refused requests of chapter 4
and the checkout guard of chapter 7. Jenkins' full security
surface is large; this chapter is the honest minimum —
the settings to have right before a Jenkins faces anyone
but you.

## Accounts and who may do what

Jenkins has its own user database (the lab's road) and can
also delegate to LDAP, your code host, or a single-sign-on
provider. On top of sign-in sits **authorization** — who
may do what. The built-in choices are coarse ("anyone can
do anything" — only ever on a throwaway) and "logged-in
users can do anything" (the lab's setting: sign-in required,
all signed-in users equal). Real installations use
**Matrix Authorization**: a grid of users against
permissions — view, build, configure, administer — granted
per person or per group, globally and per folder. The
principle to carry: *build* is a low privilege, *configure*
is code execution in slow motion (a job definition is a
shell script with a web form on it), and *administer* is
everything. Grant accordingly.

Two defaults deserve knowing. **Anonymous** should have
nothing beyond, at most, viewing on a trusted network.
And **agent connections** (chapter 11) and the **script
console** are administrator-grade powers: the script
console runs Groovy as the Jenkins process itself, which
the lab used deliberately — treat access to it as root.

## The crumb (you have met this one)

Chapter 4's `403` was Jenkins' **CSRF protection**: every
state-changing request must carry a **crumb**, a token
issued per session from `/crumbIssuer/api/json`, proving
the request originates from Jenkins' own pages or from a
client that authenticated and fetched one. It is on by
default; leave it on. The companion habit for scripts:
API tokens, not passwords. A user can mint **API tokens**
in their profile for automation; a leaked token is
revocable without changing a password anyone knows.

## Guards you benefit from without noticing

Modern Jenkins arrives with several seatbelts fastened,
and the lab tripped over one on purpose-built evidence:
the Git plugin's refusal to check out **local directories**
(chapter 7) exists because a job definition is not
necessarily written by someone who should be able to read
the whole disk. Its sibling protections include refusing
to serve arbitrary files from job directories and marking
build output that contains HTML. When one of these stops
you, the error message names the system property that
relaxes it — read the message, understand the guard, and
relax it only for a stated reason, as the lab did.

## The short list

Before a Jenkins is reachable by anyone else:

1. Sign-in required; anonymous gets nothing (or read-only,
   deliberately).
2. A real authorization strategy — matrix if more than one
   human uses it; "logged-in users can do anything" only
   for a trusted handful.
3. CSRF protection on (default), API tokens for scripts.
4. Jenkins and plugins updated — security fixes land in
   both, announced on jenkins.io/security. Enable the
   update notifications in **Manage Jenkins** and read the
   warnings it shows about your installed versions; it
   knows.
5. Builds off the controller (chapter 11) once the Jenkins
   matters; a build is untrusted code by definition.
6. JENKINS_HOME treated as the secret it is: it contains
   every credential, encrypted under keys that also live in
   it — so file permissions on that folder *are* the
   security model for everything Jenkins knows.
7. TLS in front of it (a reverse proxy or Jenkins' own
   HTTPS) before passwords travel a network you do not own
   entirely.

None of this is exotic. It is the difference between a
tool and an incident.
