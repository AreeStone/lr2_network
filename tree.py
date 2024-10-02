from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def treeTopo():
    net = Mininet(controller=RemoteController)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1', mac='00:00:00:00:00:01')
    h4 = net.addHost('h4', ip='10.0.0.4', mac='00:00:00:00:00:04')
    h5 = net.addHost('h5', ip='10.0.0.5', mac='00:00:00:00:00:05')
    h6 = net.addHost('h6', ip='10.0.0.6', mac='00:00:00:00:00:06')

    info('*** Adding switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')

    info('*** Creating links\n')
    net.addLink(h1, s1)
    net.addLink(h4, s4)
    net.addLink(h5, s2)
    net.addLink(h6, s4)

    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, s4)

    info('*** Starting network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network')
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    treeTopo()
