Sentdex
https://www.youtube.com/watch?v=v3LJ6VvpfgI&t=225s

gotta change sc2/paths.py to your starcraft2 install location
initial 
BASEDIR = {
    "Windows": "C:/Program Files (x86)/StarCraft II",

Changed to 
  "F:/Media/Games/Blizzard/StarCraft II"

realtime false | true

to change a checked out repo to use ssh instead of http, use 
git remote set-url origin _____

OpenAI Baselines is a set of high-quality implementations of reinforcement learning 

https://stackoverflow.com/questions/42605769/openai-gym-atari-on-windows/46739299
to install atari_py (baselines dependency) on windows: 
pip install --no-index -f https://github.com/Kojoley/atari-py/releases atari_py

---
(in intellij, must set python interpreter at project level AND module level)
conda install -c anaconda absl-py

tensorflow install failed. use full url to install:
pip install https://storage.googleapis.com/tensorflow/windows/cpu/tensorflow-0.12.0rc0-cp35-cp35m-win_amd64.whl
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v8.0\bin\cudart64_80.dll
https://www.youtube.com/watch?v=RplXYjxgZbw
get cuda 

tensorflow 1.6 broke? instead install 
pip install tensorflow==1.5

regressing back to tensorflow 1.5 fixed it >.<

the float warning when importing tensor flow was fixed by reinstalling h5py
pip uninstall h5py
pip install h5py

Similar to sc2 python lib, pysc2 may require you change the default install loc for SCII
YES.
pysc2/platforms.py
os.environ.get("SC2PATH")
set it here

class SubprocVecEnv(VecEnv)  def __init__(self, nenvs, nscripts, map_name) 
envs: list of gym environments to run in subprocesses
FLAGS = flags.FLAGS

git@github.com:deepmind/pysc2.git 
  ^ is not an official google product

screw this. just get the direct repo form deepmind
git@github.com:deepmind/pysc2.git
run command:

          python -m pysc2.bin.agent --map Simple64

