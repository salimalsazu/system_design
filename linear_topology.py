from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel

class CustomTopo(Topo):
    def build(self):
        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add links with parameters
        self.addLink(h1, s1, bw=10, delay='5ms', loss=1)
        self.addLink(h2, s1, bw=20)
        self.addLink(s1, s2, bw=15, delay='10ms')
        self.addLink(h3, s2, bw=10)

def run():
    topo = CustomTopo()
    net = Mininet(topo=topo, controller=Controller)
    net.start()

    # Test connectivity
    print("Testing network connectivity...")
    net.pingAll()

    # Open CLI for further testing
    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')  # Enable Mininet logs
    run()