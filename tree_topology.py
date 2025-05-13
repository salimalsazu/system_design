from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def createTreeTopo(depth=3, fanout=2):
    # Create an empty network with default controller
    net = Mininet(controller=Controller, switch=OVSSwitch)
    
    # Add controller to the network
    c0 = net.addController('c0')
    
    # Dictionary to store switches at each level
    switches = {}
    
    # Create switches for each level
    switch_count = 1
    for level in range(depth):
        switches[level] = []
        # Number of switches at this level = fanout^level
        num_switches_at_level = fanout ** level
        
        for i in range(num_switches_at_level):
            switch = net.addSwitch(f's{switch_count}')
            switches[level].append(switch)
            switch_count += 1
    
    # Connect switches between levels
    for level in range(depth-1):
        for i, parent_switch in enumerate(switches[level]):
            # Calculate children indices
            child_start_idx = i * fanout
            child_end_idx = child_start_idx + fanout
            
            # Connect parent to its children
            for child_switch in switches[level+1][child_start_idx:child_end_idx]:
                net.addLink(parent_switch, child_switch)
    
    # Add hosts to the lowest level switches
    host_count = 1
    for switch in switches[depth-1]:
        # Add fanout number of hosts to each leaf switch
        for _ in range(fanout):
            host = net.addHost(f'h{host_count}')
            net.addLink(switch, host)
            host_count += 1
    
    return net

def main():
    # Set log level for debugging
    setLogLevel('info')
    
    # Create network with specified depth and fanout
    depth = 3  # Can be changed to any value
    fanout = 2  # Can be changed to any value
    
    info(f'*** Creating tree topology with depth {depth} and fanout {fanout}\n')
    info(f'*** Number of hosts will be {fanout ** depth}\n')
    
    net = createTreeTopo(depth, fanout)
    
    # Start network
    net.start()
    
    # Print basic network info
    info('*** Network is running\n')
    info(f'*** Total switches: {len(net.switches)}\n')
    info(f'*** Total hosts: {len(net.hosts)}\n')
    
    # Start CLI
    CLI(net)
    
    # Stop network
    net.stop()

if __name__ == '__main__':
    main()