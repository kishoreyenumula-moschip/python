#!/usr/bin/python3

import os,sys

def pipeline_status(p,pipeline):
    print("recived path:{}".format(p))
    fd = open(p,"r")
    sword='Execution ended after '
    mline=''
    # lines=fd.readlines()[0:1]
    # print(lines)  #reading a specific file from total file
    for lines in fd:
        if sword in lines:
            ##print('Trueeeee')
            mline=lines
            break

    #print(mline)
    tl=mline.split(' ')
    #print(tl[-1])

    sl=tl[-1].split(':')
    sl[-1]=sl[-1].rstrip('\n')
    print(sl)

    time= str(int(sl[0])*3600 + int(sl[1])*60 + float(sl[2]))
    ms=time.split('.')
    print(ms[0])
    mins=int(ms[0])

    FRAME_RATE=pipeline.framerate
    NUM_BUFF=pipeline.num_buffers
    Delta_For_NumBuff_60FPS=120
    Delta_For_NumBuff_30FPS=60
    Ending_num_Buff= mins*int(FRAME_RATE)

    if FRAME_RATE=='60':
        num_Buff_delta_pos=int(NUM_BUFF)+Delta_For_NumBuff_60FPS
        num_Buff_delta_neg=int(NUM_BUFF)-Delta_For_NumBuff_60FPS
    if FRAME_RATE=='30':
        num_Buff_delta_pos=int(NUM_BUFF)+Delta_For_NumBuff_30FPS
        num_Buff_delta_neg=int(NUM_BUFF)-Delta_For_NumBuff_30FPS

    print(num_Buff_delta_pos)
    print(num_Buff_delta_neg)

    if NUM_BUFF!='NA':
        if Ending_num_Buff >= num_Buff_delta_pos:
            Result='FAIL'
        else:
            Result='Pass'

        if Ending_num_Buff <= num_Buff_delta_neg:
            Result='Fail'
        else:
            Result='Pass'
    print(Result)







