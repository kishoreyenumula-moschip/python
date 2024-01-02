#! /usr/bin/python3

import subprocess
import pandas
import os
import sys

class encoder():
    SOURCE='HDMI'
    WIDTH=3840
    HEIGHT=2160
    FRAMERATE=60
    FORMAT='NV12'
    CODEC='AVC'
    ENCODER='omxh264enc'
    DECODER='omxh264dec'
    TARGET_BITRATE='60000'
    MAX_BITRATE='60000'
    CONTROL_RATE='constant'
    GOPMODE='basic'
    GOPLENGTH='60'
    BFRAMES='0'
    LATENCYMODE='normal'
    IOMODE='4'
    NUM_SLICES='22'
    ENC_CAP="h264"
    ENC_CAP_PROFILE="main"
    ENC_CAP_ALINGMENT="nal"

    def __init__(self):
        print("encoder function is called")

class decoder():
    LOW_LATENCY='1'
    ENTROPY_BUF='9'
    
    def __init__(self):
        print("decoder init is called")

# class decoder():
#      def __init__(self):
#          print("decoder init is called")

def construct_pipeline(encobj,decobj):
    # print("construct pipeline is called")
    l=[f"gst-launch-1.0 v4l2src device=/dev/video0 io-mode={encobj.IOMODE} num-buffers=3600 ! video/x-raw, width={encobj.WIDTH}, height={encobj.HEIGHT}, format={encobj.FORMAT}, framerate={encobj.FRAMERATE}/1 ! ",
    f"{encobj.ENCODER} target-bitrate={encobj.TARGET_BITRATE} control-rate={encobj.CONTROL_RATE} max-bitrate={encobj.MAX_BITRATE} num-slices={encobj.NUM_SLICES} gop-mode={encobj.GOPMODE} gop-lenght={encobj.GOPLENGTH} b-frames={encobj.BFRAMES} prefetch-buffer=TRUE !",
    f" video/x-{encobj.ENC_CAP},profile={encobj.ENC_CAP_PROFILE},alignment={encobj.ENC_CAP_ALINGMENT} ! queue ! ",
    f"{encobj.DECODER} low-latency={decobj.LOW_LATENCY} entropy-buffers={decobj.ENTROPY_BUF} split-input=1 ! queue max-size-bytes=0 !",
    f" fpsdisplaysink name=fpssink text-overlay=false video-sink=\"kmssink bus-id=\"a0070000.v_mix\" hold-extra-sample=TRUE fullscreen-overlay=1 sync=true\" -v "]
   
    #gst-launch-1.0 -v v4l2src device=/dev/video0 io-mode=4 num-buffers=1600 ! video/x-raw, width=3840, height=2160, format=NV12, framerate=60/1 ! omxh265enc target-bitrate=60000 control-rate=low-latency num-slices=22 gop-mode=low-delay-p gop-length=120 b-frames=0 qp-mode=auto prefetch-buffer=TRUE ! video/x-h265, profile=main, alignment=nal ! queue ! omxh265dec low-latency=1 split-input=1 ! queue max-size-bytes=0 ! fpsdisplaysink name=fpssink text-overlay=false video-sink="kmssink bus-id="a0070000.v_mix" hold-extra-sample=TRUE fullscreen-overlay=1 sync=true" -v
    
    piepline=''.join(l)
    print(piepline)

#function to set the resolution
def set_resolution(encobj,split_args):
    if split_args[1]=='4kp60':
        # print("4kp60")
        encobj.WIDTH=3840
        encobj.HEIGHT=2160
        encobj.FRAMERATE=60
    elif split_args[1]=='4kp30':
        # print('4kp30')
        encobj.WIDTH=3840
        encobj.HEIGHT=2160
        encobj.FRAMERATE=30
    elif split_args[1]=='1080p60':
        # print("1080p60")
        encobj.WIDTH=1920
        encobj.HEIGHT=1080
        encobj.FRAMERATE=60
    elif split_args[1]=='1080p30':
        # print('1080p30')
        encobj.WIDTH=1920
        encobj.HEIGHT=1080
        encobj.FRAMERATE=30

#setting control rate constantbitrate, maxbitrate
def  set_controlrate(encobj,split_args):
    
    encobj.TARGET_BITRATE=split_args[4]

    if split_args[5]=='NA':
        if split_args[6]=='NA':
            encobj.CONTROL_RATE='constant'
        elif split_args[6] !='NA':
            encobj.CONTROL_RATE='variable'
    elif split_args[5]=='constant':
        if split_args[6]=='NA':
            encobj.MAX_BITRATE=encobj.TARGET_BITRATE

#encoder setting function
def encoder_setting(split_args):
    # print(split_args)
    encobj=encoder()
    decobj=decoder()
    set_resolution(encobj,split_args)
    if split_args[2]=='4':
        # print('iomode')
        encobj.IOMODE='4'
    elif split_args[2]=='5':
        # print('iomode')
        encobj.IOMODE='5'
    else:
        pass
    
    if split_args[3]=='AVC':
        # print('got avc')
        encobj.ENCODER='omxh264enc'
        encobj.DECODER='omxh264dec'
        encobj.ENC_CAP='h264'
        encobj.ENC_CAP_PROFILE='main'

    elif split_args[3]=='HEVC':
        # print("got hevc")
        encobj.ENCODER='omxh265enc'
        encobj.DECODER='omxh265dec'
        encobj.ENC_CAP='h265'
        encobj.ENC_CAP_PROFILE='high'
    else:
        pass
    set_controlrate(encobj,split_args)
    construct_pipeline(encobj,decobj)    

def read_data(filename):
    #write exception handling for file opening 
    fd=open(filename,"r")
    next(fd)
    for line in fd:
        line.strip()
        split_args=line.split(',')
        split_args[-1]=split_args[-1].rstrip('\n')
        encoder_setting(split_args)
        

def main():
    print("main function is executed")
    n=len(sys.argv)
    print(n,type(n))
    if n==1 or n==2 or n>3:
        print("given iput format is wrong follow below pattern")
        print("./script -l /home/path/file.lst")
        sys.exit(0)
    
    elif sys.argv[1] != '-l':
        print("Given flag is not valid")
        print("./script -l /home/path/file.lst")
        sys.exit(0)
    else:
        path=sys.argv[2]
       #print(path,type(path))
        split_path=path.split('/')
        #print(split_path)
        filename=''.join(split_path[-1:])
        # print("filename is :",filename)
        #this read data fucntion is used to read the data
        read_data(filename)

if __name__=="__main__":
    main()
