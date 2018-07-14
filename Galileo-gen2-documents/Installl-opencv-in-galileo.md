


### **Install needed package for webcam to use on galileo gen 2**

```sh
# opkg install libopencv-gpu2.4 libopencv-stitching2.4 libopencv-videostab2.4 libv4l-dev libv4l-dbg opencv

# opkg install python-opencv

```

Then run code to detect the faces (in github). If have an error: `Select timeout`, fix with this command:

```sh
# rmmod uvcvideo  
# modprobe uvcvideo nodrop=1 timeout=5000
```

If faces detection on openCV use python is so slow, let check resolution and decrease it

```sh
// check current resolution of webcam
root@galileo:~# v4l2-ctl --get-fmt-video
Format Video Capture:
	Width/Height  : 640/480
	Pixel Format  : 'YUYV'
	Field         : None
	Bytes per Line: 1280
	Size Image    : 614400
	Colorspace    : SRGB

root@galileo:~# v4l2-ctl --all
// get all current capibilities of webcam
```

To check all the resolutions supported by the webcam on each encode as the frame per seconds supported, you must run the `v4l2-ctl --list-formats-ext` command:

```sh
ioctl: VIDIOC_ENUM_FMT
	Index       : 0
	Type        : Video Capture
	Pixel Format: 'YUYV'
	Name        : YUV 4:2:2 (YUYV)
		Size: Discrete 640x480
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.040s (25.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.067s (15.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
			Interval: Discrete 0.200s (5.000 fps)
		Size: Discrete 160x120
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.040s (25.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.067s (15.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
			Interval: Discrete 0.200s (5.000 fps)
		Size: Discrete 320x240
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.040s (25.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.067s (15.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
			Interval: Discrete 0.200s (5.000 fps)
		...
		...
		Size: Discrete 960x720
			Interval: Discrete 0.100s (10.000 fps)
			Interval: Discrete 0.200s (5.000 fps)
		Size: Discrete 1024x576
			Interval: Discrete 0.100s (10.000 fps)
			Interval: Discrete 0.200s (5.000 fps)
		Size: Discrete 1184x656
			Interval: Discrete 0.100s (10.000 fps)
			Interval: Discrete 0.200s (5.000 fps)
		Size: Discrete 1280x720
			Interval: Discrete 0.133s (7.500 fps)
			Interval: Discrete 0.200s (5.000 fps)
		Size: Discrete 1280x960
			Interval: Discrete 0.133s (7.500 fps)
			Interval: Discrete 0.200s (5.000 fps)
			Index       : 1
	Type        : Video Capture
	Pixel Format: 'MJPG' (compressed)
	Name        : MJPEG
		Size: Discrete 640x480
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.040s (25.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.067s (15.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
			Interval: Discrete 0.200s (5.000 fps)
		Size: Discrete 160x120
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.040s (25.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.067s (15.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
			Interval: Discrete 0.200s (5.000 fps)
		Size: Discrete 320x240
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.040s (25.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.067s (15.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
			Interval: Discrete 0.200s (5.000 fps)
		...
		...
		...
		Size: Discrete 1280x720
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.040s (25.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.067s (15.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
			Interval: Discrete 0.200s (5.000 fps)
		Size: Discrete 1280x960
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.040s (25.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.067s (15.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
			Interval: Discrete 0.200s (5.000 fps)
		
```

**Note**: If these kinds of details are unnoticed and the wrong settings are made, the video or picture capture will fail and cause problems when working with OpenCV

To change the resolution and frames per second using v4l2-ctl, see the bellow commands:

```sh
// Set the resolution to 320x240
root@clanton:~# v4l2-ctl --set-fmt-video width=320,height=240,pixelformat=0

// Frame rate set to 30.000 fps
root@clanton:~# v4l2-ctl --set-parm=30 
```

In the first command to change resolution, option:
	
- ***pixelformat=0*** present ***pixel format is "YUYV"*** 
- ***pixelformat=1*** present ***pixel format is "MJPG"*** (compressed)


## **Streaming video**

1. Use gstreamer
	```sh
	opkg install http://iotdk.intel.com/repos/1.1/iotdk/i586/gstreamer_0.10.36-r2_i586.ipk
	```
2. Use openCV
	

## **Python pip**

```sh
# opkg install http://feeds.angstrom-distribution.org/feeds/v2016.12/ipk/glibc/i586/python/python-pip_8.1.2-r0.0_i586.ipk
```

**ipk repos**: http://feeds.angstrom-distribution.org/feeds/v2016.12/ipk/glibc/i586/python/
