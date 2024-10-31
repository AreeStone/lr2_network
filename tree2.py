from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink  # Для управления весом связей
from mininet.log import setLogLevel


def create_network():
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)

    # Добавляем контроллер
    c0 = net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6633)

    # Создаем коммутаторы с приоритетом для настройки Root Bridge
    s1 = net.addSwitch('s1', protocols='OpenFlow13', stp=True, dpid="0000000000000001")
    s2 = net.addSwitch('s2', protocols='OpenFlow13', stp=True, dpid="0000000000000002")
    s3 = net.addSwitch('s3', protocols='OpenFlow13', stp=True, dpid="0000000000000003")
    s4 = net.addSwitch('s4', protocols='OpenFlow13', stp=True, dpid="0000000000000004")
    s5 = net.addSwitch('s5', protocols='OpenFlow13', stp=True, dpid="0000000000000005")

    # Настраиваем приоритеты для выбора Root Bridge
    s1.setPriority(32768)
    s2.setPriority(32768)
    s3.setPriority(32768)
    s4.setPriority(32768)
    s5.setPriority(4096)  # Делаем s5 корневым коммутатором (Root Bridge)

    # Создаем хосты
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')

    # Подключаем хосты к коммутаторам
    net.addLink(h1, s1)
    net.addLink(h2, s4)
    net.addLink(h3, s5)
    net.addLink(h4, s5)

    # Настройка связей с указанием стоимости (cost) для выбора статуса портов
    net.addLink(s1, s2, cost=10)
    net.addLink(s2, s3, cost=10)
    net.addLink(s3, s4, cost=10)
    net.addLink(s2, s5, cost=5)  # Делаем связь с Root Bridge (s5) более предпочтительной
    net.addLink(s3, s5, cost=15)

    # Запускаем сеть
    net.start()

    # Проверка статусов портов STP для каждого коммутатора
    print("*** STP port status:")
    for switch in [s1, s2, s3, s4, s5]:
        switch.cmd('ovs-vsctl show')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    create_network()