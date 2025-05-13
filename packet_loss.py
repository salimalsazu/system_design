from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink  # Link এর জন্য TCLink ব্যবহার করতে হবে
from mininet.log import setLogLevel

class LossyTopo(Topo):
    def build(self):
        # হোস্ট ও সুইচ তৈরি
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')

        # লিংক তৈরি (h1 থেকে s1 পর্যন্ত ১০% প্যাকেট loss)
        self.addLink(h1, s1, cls=TCLink, loss=10)  # প্যাকেট হারানো ১০%
        self.addLink(h2, s1, cls=TCLink)  # সাধারণ লিংক

def run():
    topo = LossyTopo()
    net = Mininet(topo=topo, controller=Controller, link=TCLink)  # TCLink ব্যবহার বাধ্যতামূলক

    net.start()

    print("Testing connectivity with 10% packet loss on h1 ↔ s1")
    net.pingAll()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
