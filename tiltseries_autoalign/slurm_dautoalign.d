#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --partition=cpu
#SBATCH --job-name=dautoalign # Job name
#SBATCH --error=dautoalign.err
#SBATCH --output=dautoalign.out
#SBATCH --cpus-per-task=12
#SBATCH --nodes=1                    # Run all processes on a single node
#SBATCH --nodelist=c02
#SBATCH --mem-per-cpu=10GB

module load matlab
module load imod/4.11.12

matlab -nodisplay < dautoalign_script.m

