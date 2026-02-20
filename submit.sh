#!/bin/bsub

mkdir -p ./out
mkdir -p ./log
mkdir -p ./err

for nTree in 100 500 1000 1500
do
  for depth in 2 3 4
  do
    for shrinkage in 0.01 0.02 0.05 0.1 0.15 0.2
    do
      for subsample in 0.01 0.1 0.3 0.4 0.5 0.6 0.7
      do
        for binning in 3 4 5 6 7 8 9
        do
          bsub -q s -o ./log/${nTree}_${depth}_${shrinkage}_${subsample}_${binning}.log -e ./err/${nTree}_${depth}_${shrinkage}_${subsample}_${binning}.err "./bin/GridSearch"${code} ${nTree} ${depth} ${shrinkage} ${subsample} ${binning}
        done
      done
    done
  done
done

for nTree in 2000
do
  for depth in 2 3 4
  do
    for shrinkage in 0.01 0.02 0.05 0.1 0.15 0.2
    do
      for subsample in 0.01 0.1 0.3 0.4 0.5 0.6 0.7
      do
        for binning in 3 4 5 6 7 8 9
        do
          bsub -q s -o ./log/${nTree}_${depth}_${shrinkage}_${subsample}_${binning}.log -e ./err/${nTree}_${depth}_${shrinkage}_${subsample}_${binning}.err "./bin/GridSearch"${code} ${nTree} ${depth} ${shrinkage} ${subsample} ${binning}
        done
      done
    done
  done
done
