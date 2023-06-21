#!/bin/bash
# source ~/anaconda3/etc/profile.d/conda.sh &&
# conda deactivate &&
# conda deactivate &&
#shopt -s expand_aliases
python --version
#alias python='/usr/bin/python2.7'
mkdir ~/bin
PATH=~/bin:$PATH
ln -s /usr/bin/python2 ~/bin/python
python --version
cd $3
echo './run.sh '$1' --project-path '$2' --fast-orthophoto'
./run.sh $1 --project-path $2 --fast-orthophoto # exit
#source ~/anaconda3/etc/profile.d/conda.sh && conda deactivate && conda deactivate && alias python='/usr/bin/python2.7' && cd $3 && echo './run.sh '$1' --project-path '$2' --fast-orthophoto' && ./run.sh $1 --project-path $2 --fast-orthophoto # exit
#source ~/anaconda3/etc/profile.d/conda.sh && conda activate ODMEnvironment && cd $3 && echo './run.sh '$1' --project-path '$2' --fast-orthophoto' && ./run.sh $1 --project-path $2 --fast-orthophoto 
exit
exec bash
