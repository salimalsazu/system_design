from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink



def createNetwork():
    # Initialize Mininet
    net = Mininet(controller=Controller, switch=OVSSwitch, link=TCLink)

    # Add controller
    info('*** Adding controller\n')
    net.addController('c0')


    # Add switches
    info('*** Adding switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    # Add router (implemented as a host)
    info('*** Adding router\n')
    router = net.addHost('r0')

       # Add hosts for subnet 1 (172.16.20.x)
    info('*** Adding hosts for subnet 1\n')
    h1 = net.addHost('h1', ip='172.16.20.11/24', defaultRoute='via 172.16.20.1')
    h2 = net.addHost('h2', ip='172.16.20.22/24', defaultRoute='via 172.16.20.1')
    h3 = net.addHost('h3', ip='172.16.20.33/24', defaultRoute='via 172.16.20.1')

    # Add hosts for subnet 2 (172.16.30.x)
    info('*** Adding hosts for subnet 2\n')
    h4 = net.addHost('h4', ip='172.16.30.44/24', defaultRoute='via 172.16.30.1')
    h5 = net.addHost('h5', ip='172.16.30.55/24', defaultRoute='via 172.16.30.1')
    h6 = net.addHost('h6', ip='172.16.30.66/24', defaultRoute='via 172.16.30.1')

    # Add links
    info('*** Creating links\n')

    # Connect hosts to switches
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s2)
    net.addLink(h5, s2)
    net.addLink(h6, s2)

    # Connect switches to router
    # net.addLink(s1, router)
    # net.addLink(s2, router)
    net.addLink(s1, router, bw=5)
    net.addLink(s2, router, bw=5)

    # Start network
    info('*** Starting network\n')
    net.start()

    # Configure router
    info('*** Configuring router\n')
    # Enable IP forwarding
    router.cmd('sysctl net.ipv4.ip_forward=1')
    
    # Configure router interfaces
    router.cmd('ip addr flush dev r0-eth0')
    router.cmd('ip addr flush dev r0-eth1')
    router.cmd('ip addr add 172.16.20.1/24 dev r0-eth0')
    router.cmd('ip addr add 172.16.30.1/24 dev r0-eth1')
    
    # Add static routes if needed
    router.cmd('ip route add 172.16.20.0/24 dev r0-eth0')
    router.cmd('ip route add 172.16.30.0/24 dev r0-eth1')




    # Start CLI
    CLI(net)

    # Clean up
    net.stop()



if __name__ == '__main__':
    setLogLevel('info')
    createNetwork()
    
    
    


"""
sudo python3 two_subnet_network.py

1. Basic Connectivity Tests
mininet> h1 ping h2
mininet> h2 ping h3
mininet> h1 ping h4
mininet> h3 ping h6

2. Network Interface Verification
mininet> r0 ip addr show 
mininet> h1 ip addr show
mininet> h4 ip addr show

3. Routing Table Verification
mininet> r0 ip route 

mininet> h1 ip route
mininet> h4 ip route

4. Advanced Tests
a. Test TCP connectivity using iperf
mininet> h4 iperf -s &
mininet> h1 iperf -c 172.16.30.44


Traceroute between subnets:
mininet> h1 traceroute 172.16.30.44

Additional Exercises

# Modify link creation with bandwidth parameter (in Mbps)
net.addLink(s1, router, bw=10)
net.addLink(s2, router, bw=10)

# Add delay parameter (in ms)
net.addLink(s1, router, delay='10ms')

Implement access control using iptables:

mininet> r0 iptables -A FORWARD -s 172.16.20.0/24 -d 172.16.30.0/24 -j ACCEPT
mininet> r0 iptables -A FORWARD -s 172.16.30.0/24 -d 172.16.20.0/24 -j ACCEPT


Troubleshooting
If pings fail:

Check router interface configuration using ip addr show

Verify IP forwarding is enabled with sysctl net.ipv4.ip_forward

Check host default gateway settings

Check switch connectivity with ovs-ofctl show s1

If router interfaces aren't configured correctly:

Manually configure using commands in the CLI:

mininet> r0 ip addr add 172.16.20.1/24 dev r0-eth0 mininet> r0 ip addr add 172.16.30.1/24 dev r0-eth1

If IP forwarding isn't working:

Manually enable it:

mininet> r0 sysctl net.ipv4.ip_forward=1

If routes are missing: mininet> r0 ip route add 172.16.20.0/24 dev r0-eth0 mininet> r0 ip route add 172.16.30.0/24 dev r0-eth1
"""