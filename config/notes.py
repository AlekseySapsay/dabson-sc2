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

https://github.com/Blizzard/s2client-proto#map-packs

http://sc2ai.net/

Terran Bot for the Sc2 AI ladder at http://sc2ai.net/
https://github.com/Archiatrus/5minBot
^ top dog
Q learning 

gym/gym/envs/mujoco/ant.py is trippy
mujoco-py is a physics engine (need python 3 sorry dear)
PEP8 decent python style guide

import this 
The zen of python
self.build(PYLON, near=nexuses.first)

everything is rule based at the moment 

where do you want to place that nexus
fairly complex
must define (self) arg on all class methods 

TensorFlow and Deep Learning without a PhD
https://www.youtube.com/watch?v=zqWt8oI4gEw&list=PLJaEqitMr8tLwJzq1HDDvtkYjoRujG1lv&index=2

kinoni
CUDN 
cuda kernal function marked by __global__
(can be exec''d in parrallel on gpu)

write kernel in c++, rest in python 


vscode_cpp_properties.json
browse.path,"C:\\MinGW\\lib\\gcc\\mingw32\\6.3.0"
g++ -g main.cpp
launch.json 
  "miDebuggerPath": "C:\\MinGW\bin\\gdb.exe"
  "preLaunchTask": "mybuild",
  "program": "${workspaceFolder}/a.exe",


good compilers:
  g++ windows/linux
  clang mac 

compile CUDA code with nvcc
nvcc add.cu -o add_cuda
i am mental
alt + f10 for instagrab

sentdex * * * * * great channel :)

Gotta expand area + resources before going offensive 

bot_ai.py
sc2\bot_ai 
expand_now() #included method

ought to build on stratergy to not just build stalkers
self.known_enemy_units is a list

A LUA file is a source code file written in Lua, 
a light-weight programming language designed for 
extending applications. It can be compiled into 
a program using an ANSI C compiler. LUA files 
may be used to customize certain applications, 
such as the World of Warcraft and Dawn of War 
video games.

bizhawk/lua/snes for script
remember to save after training! 
  marIO/BizHawk23/Lua/SNES/DP1.state.pool 
  ..is where the trianing data is stored ;)

marI/O collects evolutions into species, 
(which a lot of genetic algos dont really do)
https://www.youtube.com/watch?v=qv6UVOQ0F44&t=255s

PULL5
http://www.dabson.co/qvalent3/

David arns atey hour
data is bootooful
https://www.youtube.com/watch?v=liJbB_0eCTo

tiniest-blockchain/blockchain.py 


sentdex 
3Blue1Brown (math animations)
youtube.com/user/shiffman
tanmay bakshi

python-sc2 
by dentosol 
(have example)

deepminds
  1.dont attack 
  2.defend our base 
  3.attack enemy buildings 
  4.attack enemy units

qlearning 
Simplest network: CNN
openCV = image processing library 
with bindings for python/java/C
ANN''s learn patterns

we use the following as training data (maybe) 
  military_weight 
  plausible_supply
  population_ratio 
  vespene_ratio 
  mineral_ratio 

NN produces something like 
[1,0,0,0]

find equiv game time for sent
For in game time you can use self.state.game_loop which is 22.4 per second﻿
Daniel forked the pysc2 package and added an on-end method 
https://github.com/daniel-kukiela/python-sc2

Convolutional Neural Nets are 
fake networks 

Convolution is the act of taking 
the original data, and creating 
feature maps from it. Pooling is 
down-sampling, most often in the 
form of "max-pooling," where we 
select a region, and then take the 
maximum value in that region, and 
that becomes the new value for the 
entire region

Pooling = downsampling 
Dropout = tossing out data (no biasing nodes in the network, makes things more robust)

'relu' is rectify Lienar
tensorboard is usefull for logging trends
[:,1] usually for the first element 

run: dxdiag to see video memory 
(not helpful)
try GPU-Z 

trying Siraj Raval''s vid again 
Algo: deep-q learner 
learnt dense representation from those pixels 

for mineral_shards game, need gflags, install via 
install python-gflags 
(MODULE NAME should be python-gflags, not just gflags)

conda install pysc2=1.2

pysc2 not avail through conda :( 

pip install pysc2==1.2.0 
WORKED!
https://github.com/chris-chris/pysc2-examples/pull/17
The current version of pysc2 has introduced breaking changes to the SC2Env options and the format of observation objects.

git fetch origin 38226b6e5ccc7d6bd86cd4d6f894270705fb0794
https://github.com/chris-chris/pysc2-examples/pull/17/files
tensorflow 1.8.0 has requirement tensorboard<1.9.0,>=1.8.0, but you'll have tensorboard 1.9.0 which is incompatible.
pip uninstall tensorboard==1.9.0 

by 17 https://www.ctolib.com/article/comments/60285 
OpenAI’s baselines
add things.
big spike @ 79%LMI (-20% will cascade)
@Walk The World 30 What's stopping high house prices moving into consumer good prices?

switch(e.which) {
  case 37: // left
  snakeDir = 'left';
  break;

  case 38: // up
  snakeDir = 'up';
  break;

  case 39: // right
  snakeDir = 'right';
  break;

  case 40: // down
  snakeDir = 'down';
  break;

  default: return;
}
not

Is it yak shaving to want to publish an npm package to make setting up a simple game simple? 

(2.8-Math.log10(i))
its not easy being cheesy ;) xxo
let val = i % 2 == 0 ? 0 : Math.pow( 2, i + 4 );

consider putting the delimiters in your bash / git alias 
there's probably a really cool/efficient way to pass in references to the shiftCombine() function'

function moveUp() {
  // shiftCombine(gameState, 12, 8, 4, 0);
  // shiftCombine(gameState, 12, 8, 4, 0);
  // shiftCombine(gameState, 12, 8, 4, 0);
  // shiftCombine(gameState, 12, 8, 4, 0);

  mapIndexAndStack( (i,ii,j,jj) => { return i + jj * gameDim } );
}
function moveDown() {
  //0,4,8,12
  //1,5,9,13
  //2,6,10,14
  //3,7,11,15
  mapIndexAndStack( (i,ii,j,jj) => { return i + j * gameDim } );
}

function moveLeft() {
  mapIndexAndStack( (i,ii,j,jj) => { return jj + i * gameDim } );
}
function moveRight() {

  // 0,1,2,4 //moves from leftmost index to rightmost index  
  // shiftCombine(gameState, [0,1,2,3]);
  // shiftCombine(gameState, [4,5,6,7]);
  // shiftCombine(gameState, [8,9,10,11]);
  // shiftCombine(gameState, [12,13,14,15]);

  mapIndexAndStack( (i,ii,j,jj) => { return j + i * gameDim } );

}

perhaps make a transition map 
the fail condition is a bit premature perhaps..

BEWARE THE FOR..IN ITERATOR -> ITS A STRING.

  for(let i=0,j=padAmount;i<gameDim;i++) {
    let r = row[i]; // row value 
    if(!r) continue;

    zeroMap[i] = j

    if((j+1)<gameDim && ) { //initially (j+1)<squashed.length
      j++;
    }
  }

    //for(let i=squashed.length-2;i>=0;i--) {  }
  // let noSquashed = 0;
  // for( i in squashed ) {
  //   let ii = row.length - 1 - i - noSquashed;

  //   if(row[ii] === squashed[i]) {
  //     zeroMap[i+noSquashed] = ii; 
  //     continue;
  //   } else if(row[ii] === 2 * squashed[i]) {
  //     zeroMap[i+noSquashed] = ii; 
  //     noSquashed++;
  //     zeroMap[i+noSquashed] = ii; 
  //   }
  // }

  // let spaces = 0;
  // let postSpaces = padAmount - 1;
  // for(let i=0;i<gameDim;i++) {
  //   let r = row[i]; // row value 
  //   if(r!==0) {
  //     let s = squashed[i-spaces-postSpaces-1];

  //     if(r===s) {
  //       console.log('aa');
  //       zeroMap[i] = i+postSpaces;
  //     } else if( r === (2 * s) ) {
  //       console.log('bb');
  //       zeroMap[i] = i+postSpaces;
  //       i++;
  //       zeroMap[i] = i+postSpaces;
  //     } else {
  //       console.log('ccrsi ',r,s,i);
  //       console.log('squashed,i,s,i-spaces: ',squashed,i,s,i-spaces);
  //     }

  //   } else {
  //     spaces++;
  //   }
  // }

  //let spaces = padAmount - 1;

  // let lastElVal = -1;
  // for(let i=j=0;i<gameDim-1);i++) {
  //   let r = row[i]; // row value 
  //   if(!r) continue;
  //   let jj = padAmount + j;

  //   zeroMap[i] = jj;

  //   if((jj+1)<gameDim) { //initially (j+1)<squashed.length
  //     j++;
  //   }
  //   lasteElVal = squashed[j]
  // }

  //zeroMap.map( x => { return })

    // row is a list of all the pre values 
  // squashed is a non-padded version of the post values 
  // index map is the space within the gameState we're working in
  // You actually want to return the gameState indices
  // Ok, we'll use our row as the mask - squashed.length SHOULD BE <= row.length (ie not always equal)

http://scrambledeggsontoast.github.io/2014/05/09/writing-2048-elm/

no commits till >121

jamin'' Yahel and Infected Mushroom 30:00 * * * * *

