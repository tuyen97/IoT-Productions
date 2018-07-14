### **Galileo 2**

Cấu hình:

- Sử dụng chip Quark SoC x1000 với tần số ***400MHz***
- Có ***256 MB RAM*** 
- Chạy trên ***embedded Linux kernel v3.8***
- IP: ***10.42.0.85***

Tại sao lại cần dùng Galileo?

Tùy thuộc vào mục đích của project, ta có thể sử dụng các Ardunio boards để tiết kiệm chi phí khi chỉ cần dùng các board mạch chỉ có vi điều khiển.

Còn khi ta cần 1 board mạch có khả năng xử lý mạnh mẽ hơn và có thêm các đặc điểm dưới đây như:

- Lưu thông tin vào thẻ nhớ (SD card) để ***logging***
- Connect and transmit dữ liệu thông qua mạng Internet
- Người dùng cần khả năng truyền và hiển thị các **logs file** hoặc dữ liệu tại thời điểm hiện tại thông qua các web server, do đó cần phải triển khai được web server trên board mạch.
- Board mạch phải có cổng USB để connect tới các thiết bị ngoại vi như webcam để thu thập hình ảnh để sử dụng và truyền đi như 1 loại dữ liệu.
- Truy cập vào internet thông qua kết nối ***ethernet or wifi***. Ta sẽ phải cần thời gian chính xác cho dữ liệu thu thập được khi lưu vào thẻ nhớ (SD card), ngay cả khi board mạch reboots, do đó cần có ***Real Time Clock (RTC)*** .


# Custom setup procedure for Intel Galileo v1/v2


### Download the image

http://iotdk.intel.com/images/iot-devkit-latest-mmcblkp0.direct.bz2

### Get a SD card

Get a micro SD card, 2Gb minimum.

An adapter to read the SD card from your laptop is required. The SD card adapter is best. The USB adapter also works.

### Get a DHCP server

In my case, I'll use a simple home router with DHCP server included.
You need to be able to read the IP addresses assignated from the DHCP server.
Home routers have this option in the admin page.

## Flash the SD card

On your PC :
```
bunzip2 -c iot-devkit-latest-mmcblkp0.direct.bz2
file iot-devkit-latest-mmcblkp0.direct
```
Result : it's a disk dump ! We'll use dd to create the micro SD card.
Be careful with dd : if you dump from the image file to the wrong device, like your hard disk instead of the SD card, you'll wipe your disk.
```
sudo su
fdisk -l
umount /dev/my_device_partition
dd bs=1M if=iot-devkit-latest-mmcblkp0.direct of=/dev/my_device
```
On my PC, I used the SD card port.
The ```/dev/my_device_partition`` was ```/dev/sdb1```
and ```/dev/my_device``` was ```/dev/sdb```.

## Resize


### Resize partition

The image was created with a small partition, but we need to install a lot of packages.
That's why we need to resize the partition and filesystem.
```
donghm@donghm:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            3,9G  4,0K  3,9G   1% /dev
tmpfs           789M  1,5M  788M   1% /run
/dev/sda7        92G   72G   16G  83% /
none            4,0K     0  4,0K   0% /sys/fs/cgroup
none            5,0M     0  5,0M   0% /run/lock
none            3,9G   11M  3,9G   1% /run/shm
none            100M   64K  100M   1% /run/user
/dev/sdb1        50M  9,3M   41M  19% /media/donghm/5586-3D43
/dev/sdb2       1,2G  1,2G     0 100% /media/donghm/56bea387-98cc-4d93-a36a-268fbcc0213f

donghm@donghm:~$ sudo fdisk /dev/sdb
Command (m for help): p

Disk /dev/sdb: 3965 MB, 3965190144 bytes
122 heads, 62 sectors/track, 1023 cylinders, total 7744512 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x000a69e4

   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1   *        2048      106495       52224   83  Linux
/dev/sdb2          106496     7744511     3819008   83  Linux

Command (m for help): d
Partition number (1-4): 2

Command (m for help): p

Disk /dev/sdb: 3965 MB, 3965190144 bytes
122 heads, 62 sectors/track, 1023 cylinders, total 7744512 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x000a69e4

   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1   *        2048      106495       52224   83  Linux

Command (m for help): n
Partition type:
   p   primary (1 primary, 0 extended, 3 free)
   e   extended
Select (default p): p
Partition number (1-4, default 2): 
Using default value 2
First sector (106496-7744511, default 106496): 106496
Last sector, +sectors or +size{K,M,G} (106496-7744511, default 7744511): 7744511

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.

WARNING: Re-reading the partition table failed with error 16: Device or resource busy.
The kernel still uses the old table. The new table will be used at
the next reboot or after you run partprobe(8) or kpartx(8)
Syncing disks.

donghm@donghm:~$ sudo resize2fs /dev/sdb2
resize2fs 1.42.9 (4-Feb-2014)
Filesystem at /dev/sdb2 is mounted on /media/donghm/56bea387-98cc-4d93-a36a-268fbcc0213f; on-line resizing required
old_desc_blocks = 1, new_desc_blocks = 1
The filesystem on /dev/sdb2 is now 954752 blocks long.

donghm@donghm:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            3,9G  4,0K  3,9G   1% /dev
tmpfs           789M  1,5M  788M   1% /run
/dev/sda7        92G   72G   16G  83% /
none            4,0K     0  4,0K   0% /sys/fs/cgroup
none            5,0M     0  5,0M   0% /run/lock
none            3,9G   46M  3,9G   2% /run/shm
none            100M   64K  100M   1% /run/user
/dev/sdb1        50M  9,3M   41M  19% /media/donghm/5586-3D43
/dev/sdb2       3,6G  1,2G  2,3G  35% /media/donghm/56bea387-98cc-4d93-a36a-268fbcc0213f

=>>> DONE

```

Freeee space is now available.


### Boot your Intel Galileo with the SD card

Boot your galileo with the SD card, check your router DHCP table to get the IP address of your board, then ssh.
```
ssh root@X.X.X.X
```
You're on the board, running linux.

## Initial Setup

### Add third party repo with more packages
This one is for eglibc !
```
wget http://storage.tokor.org/pub/galileo/packages/opkg.conf -O /etc/opkg/opkg.conf
rm /etc/opkg/base-feeds.conf
opkg update
```
### Set the date
```
opkg install ntpdate
ntpdate -s fr.pool.ntp.org
date
```
No coin battery is installed on my galileo (you can),
so I need to get the time from a NTP server
each time I boot, or ask a manual update with ntpdate.

### Add packages

```
opkg install nano vim
opkg install libmraa0 upm
opkg install packagegroup-core-buildessential
opkg install libusb-1.0-dev bluez5-dev bluez5 opencv opencv-dev opencv-apps libopencv-core-dev libopencv-core2.4 libopencv-calib3d-dev libopencv-calib3d2.4 libopencv-contrib-dev libopencv-contrib2.4 libopencv-features2d-dev libopencv-features2d2.4 libopencv-flann-dev libopencv-flann2.4 libopencv-gpu-dev libopencv-gpu2.4 libopencv-imgproc-dev libopencv-imgproc2.4 libopencv-legacy-dev libopencv-legacy2.4 libopencv-ml-dev libopencv-ml2.4 libopencv-nonfree-dev libopencv-nonfree2.4 libopencv-photo-dev libopencv-photo2.4 libopencv-stitching-dev libopencv-stitching2.4 libopencv-superres-dev libopencv-superres2.4 libopencv-video-dev libopencv-video2.4 libopencv-videostab-dev libopencv-videostab2.4  libopencv-highgui-dev  libopencv-highgui2.4 libopencv-objdetect2.4 libopencv-objdetect-dev opencv-staticdev libopencv-ts-dev libopencv-ts2.4 alsa-server alsa-lib-dev alsa-dev alsa-utils-aconnect alsa-utils-speakertest alsa-utils-midi alsa-dev libsndfile-bin libsndfile-dev flex bison git espeak i2c-tools libsqlite3-0 sqlite3 apache2 apache2-scripts modphp lirc lirc-dev rsync v4l-utils 
opkg install alsa-dev --force-overwrite alsa-lib-dev
opkg install nodejs
```

### Add NodeJS packages
It may take hours to install everything (npm works with sources), but you don't have to install all the packages if you don't want to wait.
You can also write the commands in a script and launch this script to avoid waiting.
```
npm cache clear
npm install -g mraa
npm install -g cylon-intel-iot cylon cylon-gpio cylon-i2c
npm install -g cylon-mqtt cylon-api-mqtt cylon-neurosky
npm install -g cylon-ble bluetooth-obd
npm install -g bleno
npm install -g midi
npm install -g smoothie browserify 
npm install -g cylon-api-socketio cylon-api-http
npm install -g cylon-opencv
npm install -g cylon-joystick rolling-spider temporal cli
npm install -g sleep
```

### WiFi and bluetooth - Optionnal

If you have a Wifi-BT adapter :
Shutdown, plug the Wifi-BT adapter in the pci express port and boot.
```
systemctl status connman
connmanctl
> enable wifi
> scan wifi
> services
*AO Wired                ethernet_984fee002ec7_cable
```

As we are running galileo over the network,
the wired network is already live and set as autoconnect.
You should see the wifi networks available in the list.
```
> agent on
> connect wifi_c8f7332a01bb_494e54454c5f34_managed_psk
> config wifi_c8f7332a01bb_494e54454c5f34_managed_psk --autoconnect yes --ipv4 dhcp
> services
*AO Wired                ethernet_984fee002ec7_cable
*AR INTEL_4              wifi_c8f7332a01bb_494e54454c5f34_managed_psk
```
Quick connman and check the status :
```
iwconfig
```
The wifi is a backup for the wired network, and the balance is managed by connman.
Unplug the ethernet cable and the wifi will be online. Check router DHCP table for IP address of the Wifi card.

You can now go to the labs section.
