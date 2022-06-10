#!C:\\Users\\user\\Anaconda3\\envs\\ui\\python

import subprocess, os, sys
from argparse import ArgumentParser

#myPath = "/home/jyw/anaconda3/envs/face/bin:/usr/sbin:/usr/bin:/sbin:/bin"
myPath = "C:\\Users\\user\\Anaconda3\\envs\\motion;"
myWdir = "D:\\program\\first-order-model\\" #first order motion
myRCmd = "C:\\Users\\user\\Anaconda3\\envs\\motion\\python demodir.py"

my_env = os.environ.copy()
my_env["PATH"] = myPath

parser = ArgumentParser()
parser.add_argument("--source_image", required=True, help="path to source image")
parser.add_argument("--driving_dir", required=True, help="path to driving folder")
parser.add_argument("--output_dir", default='output', help="path to output")

opts, others = parser.parse_known_args()

paras = f"--source_image {os.path.abspath(opts.source_image)} "
paras += f"--driving_dir {os.path.abspath(opts.driving_dir)} " 
paras += f"--output_dir {os.path.abspath(opts.output_dir)} " 
 
paras += " ".join(others)

cmdstr = f"{myRCmd} {paras}"
#cmdstr = "python -V"
print(cmdstr)
subprocess.run(cmdstr.split(), cwd=myWdir, env=my_env)
