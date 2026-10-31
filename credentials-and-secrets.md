# Credentials and secrets

By the end of this chapter you know where Jenkins keeps
secrets, what it does to protect them, and the one rule
that protects you back. The lab's proof is small and
complete: it stored a dummy credential, then asked Jenkins
for it three ways — and never got the secret back.

## Why a store at all

Builds need secrets: the password that uploads the release,
the token that talks to an API, the key that signs the
package. The two bad places for them are *in the code*
(where every copy of the repository carries them forever)
and *typed into job forms as plain text* (where anyone who
can see the configuration can read them). Jenkins' answer
is a **credential store**: secrets kept in one place, by
ID, handed to a build only while it runs.

## What the store does (live)

Credentials live under **Manage Jenkins → Credentials**,
in **scopes**: *system* (for Jenkins' own machinery, like
agent connections), *global* (available to jobs), and
per-folder or per-user scopes for finer control. Each
credential has an **ID** — the only thing a job ever names
— a kind (username-and-password, secret text, secret file,
SSH key, certificate), and the secret itself.

The lab added one through the script console, a labelled
dummy (transcript `t12`):

```text
id: orbit-widget-uploader, username: widget-bot
(the password is an invented lab value, worth nothing)
```

Then the three questions. Through Jenkins' own API, the
credential comes back as metadata only — `id`,
`description`, `typeName` — **the secret is not in the
answer**, because there is no "show me the password"
operation; Jenkins is write-only about secrets by design.
On disk, in `JENKINS_HOME/credentials.xml`, the username
sits in plain text but the password is an encrypted blob:

```text
<password>{AQAAABAAAAAwBtOsDVzuBkpaCOcJRJEi8OD+mPn9…}</password>
```

The `{…}` form means "encrypted with this Jenkins' own
keys" — the keys in `JENKINS_HOME/secrets/` and
`secret.key`. Two lessons ride on that. First, an attacker
who copies `credentials.xml` alone gets blobs; it is the
**whole JENKINS_HOME**, keys included, that must be
guarded (and backed up — chapter 12 — since losing the
keys loses the secrets). Second, *encrypted at rest* is
not *safe in use*: the moment a build uses a secret, the
secret exists in that build's environment.

## Using a credential, and the rule

In a pipeline, the standard pattern binds a credential to
environment variables for one block, and Jenkins **masks**
the values if they appear in the console:

```groovy
withCredentials([usernamePassword(
    credentialsId: 'orbit-widget-uploader',
    usernameVariable: 'UPLOAD_USER',
    passwordVariable: 'UPLOAD_PASS')]) {
    sh 'upload-tool -u "$UPLOAD_USER" -p "$UPLOAD_PASS" release.txt'
}
```

(This binding step is supplied by the Credentials Binding
plugin; the lab proved the store underneath it rather than
a live upload — see `criteria.md`.)

And the rule, which no tooling replaces:

> **Never echo a secret, and never let a tool print it
> into the console.** Console logs are kept, copied, and
> screenshotted. Masking is a safety net for accidents, not
> a licence to print. If a secret ever does appear in a
> log, the secret is burned: rotate it, because deleting
> the build deletes the evidence, not the exposure.

Rotate on a schedule anyway, prefer short-lived tokens
where the other end offers them, and give each job the
fewest credentials it can do its work with — a release job
needs the upload key; a test job does not.
