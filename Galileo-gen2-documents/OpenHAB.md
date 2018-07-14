### **OpenHAB 2.2**

Run container:

```sh
$ id -u openhab
998

$ cat /etc/group | grep group_openhab
group_openhab:x:1001:openhab,donghm

$ docker run --name openhab --net=host --tty \
-v /etc/localtime:/etc/localtime:ro \
-v /etc/timezone:/etc/timezone:ro \
-v /home/donghm/finnal/openhab/conf:/openhab/conf \
-v /home/donghm/finnal/openhab/userdata:/openhab/userdata  \
-v /home/donghm/finnal/openhab/addons:/openhab/addons \
-d -e USER_ID=998 -e GROUP_ID=1001 \
openhab/openhab:2.2.0-amd64-debian

// check OpenHAB logs
$ tailf openhab/userdata/logs/openhab.log
```

### **Persistent MySQL**

link: https://community.openhab.org/t/openhab2-mysql-persistence-setup/15829

```sh
> create database openhab;
> create user 'openhab'@'localhost' identified by 'openhab';
> grant all privileges on openhab.* to 'openhab'@'localhost';
```
