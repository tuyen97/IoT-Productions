### **Fix static ip for galileo**

Create file `/etc/network/interfaces` with bellow content:

```sh
#auto enp0s20f6
iface enp0s20f6 inet static
address 192.168.1.10
netmask 255.255.255.0
broadcast 192.168.1.255
gateway 192.168.1.1
dns-nameservers 8.8.8.8 8.8.4.4
```

And config DNS and static ip that make galileo can connect internet in file `/var/lib/connman/ethernet_984fee0314f4_cable/settings`:

```sh
[ethernet_984fee0314f4_cable]
Name=Wired
AutoConnect=true
Modified=2018-03-06T10:46:04.067959Z
IPv4.method=manual
IPv6.method=auto
IPv6.privacy=disabled
Nameservers=8.8.8.8;8.8.4.4;
IPv4.netmask_prefixlen=24
IPv4.local_address=192.168.60.231
IPv4.gateway=192.168.60.1
IPv6.DHCP.DUID=0001000122312d9f984fee0314f4
```

And finally config name servers by using `connman` service:

```sh
# cd /var/lib/connman/
# connmanctl config ethernet_984fee0314f4_cable --nameservers 192.168.1.1
```

Add repos to file `/etc/opkg/iotdk.conf`

```sh
src iotdk-all http://iotdk.intel.com/repos/1.5/iotdk/all
src iotdk-i586 http://iotdk.intel.com/repos/1.5/iotdk/i586
src iotdk-quark http://iotdk.intel.com/repos/1.5/iotdk/quark
src iotdk-x86 http://iotdk.intel.com/repos/1.5/iotdk/x86
```

Then run update and upgrade command:

```sh
# opkg update
 
# opkg upgrade
```

**Galileo mac address**:

```sh
98:4F:EE:03:14:F4
```
