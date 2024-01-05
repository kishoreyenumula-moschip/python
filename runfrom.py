#! /usr/bin/python3

import sys
import subprocess
import os
import xlsxwriter
import status
import shutil
import myxlsxupdate


row=0
fps_path_global=[]
args_to_xlsx=[]
name_xlsx='samp.xlsx'
global_pipe=[]
all_result=[]

class pipeline():
    sno=''
    num_buffers='100'
    width='1920'
    height='1080'
    format='YV12'
    framerate='60'
    def __init__(self):
        pass
        #print("pipeline class is called")

def create_logs(result,pipe):
    
    d=[f"{pipeline.sno}"]
    out_dir='logs'
    inner_dir=''.join(d)
    cur_dir=os.getcwd()

    out_dir_path=os.path.join(cur_dir,out_dir)
    inner_dir_path=os.path.join(out_dir_path,inner_dir)
    
    # print(out_dir_path)
    # print(inner_dir_path)

    if pipeline.sno=='1':
        if os.path.exists(out_dir_path):
            shutil.rmtree(out_dir_path)
    
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
    
    #print('--------------------------------------------------------------')
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
    global args_to_xlsx
    args_to_xlsx.append(split_args)
    #print(args_to_xlsx)
    pipeline.sno=split_args[0]
    pipeline.num_buffers=split_args[1]
    pipeline.width=split_args[2]
    pipeline.height=split_args[3]
    if split_args[4]=='NA':
        pass
    else:
        pipeline.format=split_args[4]
    pipeline.framerate=split_args[5]

    l=[f"gst-launch-1.0 -v videotestsrc num-buffers={pipeline.num_buffers} ! video/x-raw,width={pipeline.width},height={pipeline.height},format={pipeline.format},framerate={pipeline.framerate}/1 ! ",
       f"fpsdisplaysink video-sink=\"autovideosink\" text-overlay=0 "]
    pipe=''.join(l)
   
    print("\t\t\t\t\t","************************NEXT PIPELINE***************************","\n")
    global global_pipe
    global_pipe.append(pipe)
    print(pipe)
    runpipeline(pipe)

#creating the xlxz sheet initally and updating the first row
def create_xlsx(title_line):
    
    print(type(title_line))
    print(title_line[0])
    title=title_line[0].split(',')
    title[-1]=title[-1].rstrip('\n')
    print(title)
    global name_xlsx
    workbook=xlsxwriter.Workbook(name_xlsx)
    worksheet=workbook.add_worksheet()
    global row
    for i in range(0,len(title)):
        worksheet.write(row,i,title[i])
    row+=1
    workbook.close()

def readdata(filename):
    fd =open(filename,'r')
    title_line=fd.readlines()[0:1]
    create_xlsx(title_line)
    
    fd =open(filename,'r')
    next(fd)
    for line in fd:
        line.strip()
        split_args=line.split(',')
        split_args[-1]=split_args[-1].rstrip('\n')
        setpipeline(split_args)

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
        result=status.pipeline_status(fps_path_global[i],pipeline)
        # print("RETURN STATUS IS :{}".format(result))
        global all_result
        all_result.append(result)
        print("pipeline {} is {}".format(i+1,result))
    
    global row,name_xlsx,global_pipe,args_to_xlsx
    # print("all result from main module")
    # print(all_result)
    ret= myxlsxupdate.open_and_update(name_xlsx,row,args_to_xlsx,all_result,global_pipe)
    
if __name__=="__main__":
    main()