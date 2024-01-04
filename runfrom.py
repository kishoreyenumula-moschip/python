#! /usr/bin/python3

import sys
import subprocess
import os
import xlsxwriter
import status


row=1
fps_path_global=[]

class pipeline():
    sno='0'
    num_buffers='10'
    width='1920'
    height='1080'
    format='YV12'
    framerate='30'
    def __init__(self):
        print("pipeline class is called")
#-------------------------------------------------------------------------------------------------------
# def  pipeline_status(fps_path):
#     print("GOT PATH IS:{}".format(fps_path))
    
#     # final_path=sys.argv[2]
#     fd = open(fps_path,'r')
#     sword="Execution ended after "
#     lines=fd.readlines()
#     mline=' '
    
#     for lines in fd:
#         if sword in lines:
#             mline=lines
#             break
    
#     print("main line is:{}".format(mline))
#     tl=mline.split(' ')

#     sl=tl[-1].split(':')
#     sl[-1]=sl[-1].rstrip('\n')
#     print(sl)

#     time= str(int(sl[0])*3600 + int(sl[1])*60 + float(sl[2]))
#     ms=time.split('.')
#     print(ms[0])
#     mins=int(ms[0])

#     FRAME_RATE=pipeline.framerate
#     NUM_BUFF=pipeline.num_buffers
#     Delta_For_NumBuff_60FPS=120
#     Delta_For_NumBuff_30FPS=60
#     Ending_num_Buff= mins*FRAME_RATE

#     if FRAME_RATE==60:
#         num_Buff_delta_pos=int(NUM_BUFF)+Delta_For_NumBuff_60FPS
#         num_Buff_delta_neg=int(NUM_BUFF)-Delta_For_NumBuff_60FPS
#     if FRAME_RATE==30:
#         num_Buff_delta_pos=int(NUM_BUFF)+Delta_For_NumBuff_30FPS
#         num_Buff_delta_neg=int(NUM_BUFF)-Delta_For_NumBuff_30FPS

#     print(num_Buff_delta_pos)
#     print(num_Buff_delta_neg)

#     if NUM_BUFF!='NA':
#         if Ending_num_Buff >= num_Buff_delta_pos:
#             Result='FAIL'
#         else:
#             Result='Pass'

#         if Ending_num_Buff <= num_Buff_delta_neg:
#             Result='FAIL'
#         else:
#             Result='Pass'
#     print(Result)

#--------------------------------------------------------------------------------------------
def create_logs(result,pipe):
    
    d=[f"{pipeline.sno}"]
    out_dir='logs'
    inner_dir=''.join(d)
    cur_dir=os.getcwd()

    out_dir_path=os.path.join(cur_dir,out_dir)
    inner_dir_path=os.path.join(out_dir_path,inner_dir)
    print(out_dir_path)
    print(inner_dir_path)
    
    if os.path.exists(out_dir_path):
        pass
    else:
        os.mkdir(out_dir_path)
    
    if os.path.exists(inner_dir_path):
        pass
    else:
        os.mkdir(inner_dir_path)
        
    l=[f"fps{pipeline.sno}.log"]
    # s=''.join(l)
    final_path=os.path.join(inner_dir_path,l[0])
    
    print('--------------------------------------------------------------')
    print("for log files check:{}".format(final_path))
    
    fd=open(final_path,'w+')
    fd.write("{}\n".format(pipe))
    fd = open(final_path,'+a')
    fd.write(result.stdout)
    print(result.stdout)
    global fps_path_global
    fps_path_global.append(final_path)
    #pipeline_status(final_path)


def runpipeline(pipe):
    result=subprocess.run(pipe,stdout=subprocess.PIPE,text=True,shell=True)
    #writing another function which create these logs
    create_logs(result,pipe)
    
def setpipeline(split_args):
    pipeline.sno=split_args[0]
    pipeline.num_buffers=split_args[1]
    pipeline.width=split_args[2]
    pipeline.height=split_args[3]
    pipeline.format=split_args[4]
    pipeline.framerate=split_args[5]

    l=[f"gst-launch-1.0 -v videotestsrc num-buffers={pipeline.num_buffers} ! video/x-raw,width={pipeline.width},height={pipeline.height},format={pipeline.format},framerate={pipeline.framerate}/1 ! ",
       f"fpsdisplaysink video-sink=\"autovideosink\" text-overlay=0 "]
    pipe=''.join(l)
    print(pipe)
    runpipeline(pipe)


def create_xlxs(split_args):
    print("CREATE XLXS IS CALLED")
    
    workbook = xlsxwriter.Workbook('test.xlsx')

    worksheet = workbook.add_worksheet()
    global row
    for i in range(0,len(split_args)):
        worksheet.write(row,i,split_args[i])

    row+=1
    workbook.close()

def readdata(filename):
    fd =open(filename,'r')
    next(fd)
    for line in fd:
        line.strip()
        split_args=line.split(',')
        split_args[-1]=split_args[-1].rstrip('\n')
        setpipeline(split_args)
        create_xlxs(split_args)

def main():
    #print("main function is executed")
    n=len(sys.argv)
    print(n,type(n))
    path=sys.argv[1]
    #this is to extract basename directly
    filename=os.path.basename(path)
    readdata(filename)
    # print(fps_path_global)
    for i in range(0,len(fps_path_global)):
        fps_path_global[i]=fps_path_global[i].strip()
        status.pipeline_status(fps_path_global[i],pipeline)
    
if __name__=="__main__":
    main()