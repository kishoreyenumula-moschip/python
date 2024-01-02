#! /usr/bin/python3

import subprocess
import os
import openpyxl
import sys

pipeline='NULL'
enc_pipeline='NULL'
dec_pipeline='NULL'
end_pipeline='NULL'
class inputsrc():
    width=1920
    height=1080
    format='NV12'
    framerate=60
    io_mode=4
    def __init__(self):
        print("input src is called")

class encoder_s():
    codec='AVC'
    encoder='omxh264enc'
    decoder='omxh264dec'
    cap='video/x-h264'
    target_bitrate='60000'
    control_rate='constant'
    max_bitrate='60000'
    num_slice='8'
    gopmode='basic'
    goplen='60'
    bframes='0'
    latency_mode='normal'
    profile='main'
    alignment='au'

    def __init__(self):
        pass
        #print("encoder class is called")
#decoder class
class decoder_s():
    decoder='omxh264dec'
    entropy_buf='9'
    low_latency='0'
    def __init__(self):
        pass
        #print("decoder class is called ")

def setinput_pipeline():
    l=[f"gst-launch-1.0 -v v4l2src device=/dev/video0 io-mode={inputsrc.io_mode} num-buffers=1600 ! video/x-raw, width={inputsrc.width}, height={inputsrc.height}, format={inputsrc.format}, framerate={inputsrc.framerate}/1 ! " ]
    global pipeline 
    pipeline=''.join(l)
    #print(pipeline)

#joining the pipeline
def join_pipeline():
    print('join pipeline is called')
    print(pipeline+enc_pipeline+dec_pipeline+end_pipeline)

def set_input_src():
    #print("setting the input src")
    #iobj=inputsrc()
    if sys.argv[6]=='4kp60':
        inputsrc.height=2160
        inputsrc.width=3840
        inputsrc.format='NV12'
        inputsrc.framerate=60
    elif sys.argv[6]=='4kp30':
        inputsrc.height=2160
        inputsrc.width=3840
        inputsrc.format='NV12'
        inputsrc.framerate=30
    elif sys.argv[6]=='1080p60':
        inputsrc.height=1080
        inputsrc.width=1920
        inputsrc.format='NV12'
        inputsrc.framerate=60
    elif sys.argv[6]=='1080p30':
        inputsrc.height=1080
        inputsrc.width=1920
        inputsrc.format='NV12'
        inputsrc.framerate=30
        
    if sys.argv[8]=='4':
        inputsrc.io_mode=4
    else:
        inputsrc.io_mode=5

    setinput_pipeline()
#setting the codec
def set_codec(split_args):
    if split_args[3]=='AVC':
        encoder_s.encoder='omxh264enc'
        encoder_s.decoder='omxh264dec'
        encoder_s.cap='video/x-h264'
    elif split_args[3]=='HEVC':
        encoder_s.encoder='omxh265enc'
        encoder_s.decoder='omxh265dec'
        encoder_s.cap='video/x-h265'

#setting encoder pipline
def setencoder_pipeline():
    if encoder_s.latency_mode=='NA':
        el=[f"{encoder_s.encoder} target-bitrate={encoder_s.target_bitrate} control-rate={encoder_s.control_rate} max-bitrate={encoder_s.max_bitrate}  num-slices={encoder_s.num_slice}  gop-mode={encoder_s.gopmode} gop-length={encoder_s.goplen} bframes={encoder_s.bframes} prefetch-buffer=TRUE ! ",
        f"{encoder_s.cap},profile={encoder_s.profile},alignment={encoder_s.alignment} ! "]
    else:
        el=[f"{encoder_s.encoder} target-bitrate={encoder_s.target_bitrate} control-rate={encoder_s.control_rate} max-bitrate={encoder_s.max_bitrate} latency-mode={encoder_s.latency_mode} num-slices={encoder_s.num_slice}  gop-mode={encoder_s.gopmode} gop-length={encoder_s.goplen} bframes={encoder_s.bframes} prefetch-buffer=TRUE ! ",
        f"{encoder_s.cap},profile={encoder_s.profile},alignment={encoder_s.alignment} ! queue ! "]

    global enc_pipeline
    enc_pipeline=''.join(el)
    #print(enc_pipeline)
    #join_pipeline()

#setting the parameters 
def set_param(split_args):
    encoder_s.target_bitrate=split_args[4]
    encoder_s.control_rate=split_args[5]
    if split_args[6]=='NA':
        encoder_s.max_bitrate=encoder_s.target_bitrate
    else:
        encoder_s.max_bitrate=split_args[6]

    encoder_s.num_slice=split_args[7]
    encoder_s.gopmode=split_args[8]
    encoder_s.goplen=split_args[9]
    
    if split_args[10]=='NA':
        encoder_s.bframes='0'
    else:
        encoder_s.bframes=split_args[10]

    if split_args[11]=='NA':
        encoder_s.latency_mode='NA'
    else:
        encoder_s.latency_mode=split_args[11]
    
    encoder_s.profile=split_args[12]
    encoder_s.alignment=split_args[13]
    setencoder_pipeline()

#setting the sink pipeline
def setsink_pipeline():
    sinkpipe=[f"fpsdisplaysink name=fpssink text-overlay=false video-sink=\"kmssink bus-id=\"a0070000.v_mix\" hold-extra-sample=TRUE fullscreen-overlay=1 sync=true\" -v"]
    global end_pipeline
    end_pipeline=''.join(sinkpipe)
    #print(end_pipeline)
    join_pipeline()

#setting decoder pipeline
def setdecoder_pipeline():
    global dec_pipeline
    decpipe=[f"{encoder_s.decoder} low-latency={decoder_s.low_latency} internal-entropy-buffers={decoder_s.entropy_buf} ! ",
             f"queue max-size-bytes=0 ! "]
    dec_pipeline=''.join(decpipe)
    setsink_pipeline()

def setdecoder(split_args):
    #print("setting the decoder")
    print(encoder_s.control_rate)
    if encoder_s.control_rate=='low-latency':
        print('YESSSSSSSSSSS')
        decoder_s.low_latency='1'
    else:
        decoder_s.low_latency='0'
    decoder_s.entropy_buf=split_args[14]
    setdecoder_pipeline()

#setting encoder
def setencoder(split_args):
    #print('setting encoder parameters')
   # encobj=encoder_s()
    # set_codec(split_args,encobj)
    # set_param(split_args,encobj)
    set_codec(split_args)
    set_param(split_args)
    

def read_data(filename):
    #write exception handling for file opening 
    fd=open(filename,"r")
    next(fd)
    for line in fd:
        line.strip()
        split_args=line.split(',')
        split_args[-1]=split_args[-1].rstrip('\n')
        #print(split_args)
        setencoder(split_args)
        setdecoder(split_args)

def main():
    #print("main function is executed")
    n=len(sys.argv)
    print(n,type(n))
    set_input_src()
    if n!=9:
        print("given iput format is wrong follow below pattern")
        print("./script -t type -l /home/path/file.lst -r 4kp60 -m iomode")
        sys.exit(0)
    
    elif sys.argv[3] != '-l':
        print("Given flag is not valid")
        print("./script -l /home/path/file.lst")
        sys.exit(0)
    else:
        path=sys.argv[4]
       #print(path,type(path))
        split_path=path.split('/')
        #print(split_path)
        filename=''.join(split_path[-1:])
        # print("filename is :",filename)
        #this read data fucntion is used to read the data
        read_data(filename)

if __name__=="__main__":
    main()