import jenkins.model.Jenkins
import hudson.security.HudsonPrivateSecurityRealm
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy

// Scripted first setup for this guide's lab: create one admin account.
// Name and password arrive as environment variables, never written to disk.
def user = System.getenv('JENKINS_LAB_USER')
def pass = System.getenv('JENKINS_LAB_PASSWORD')
def j = Jenkins.get()
def realm = new HudsonPrivateSecurityRealm(false)
realm.createAccount(user, pass)
j.setSecurityRealm(realm)
def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
j.setAuthorizationStrategy(strategy)
j.save()
println "Lab setup: admin account '${user}' created by init script"
