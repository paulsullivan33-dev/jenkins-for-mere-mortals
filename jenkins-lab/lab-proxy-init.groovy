import jenkins.model.Jenkins
import hudson.ProxyConfiguration

// This lab's sandbox reaches the internet through a proxy whose address
// (with its sign-in) is published in the process environment. Read it from
// there at startup so no credential is ever written into this file.
def raw = System.getenv('https_proxy') ?: System.getenv('HTTPS_PROXY')
if (raw) {
  def u = new URI(raw)
  def ui = u.userInfo?.split(':', 2)
  def pc = new ProxyConfiguration(u.host, u.port,
      ui ? ui[0] : null, (ui && ui.size() > 1) ? ui[1] : null,
      'localhost,127.0.0.1')
  Jenkins.get().proxy = pc
  Jenkins.get().save()
  println "Lab setup: Jenkins proxy set from environment (${u.host}:${u.port})"
}
