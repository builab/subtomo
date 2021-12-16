#!/bin/bash
#SBATCH --ntasks=1                
#SBATCH --partition=cpu
#SBATCH --job-name=template_matching # Job name
#SBATCH --error=dtemplate_matching.err
#SBATCH --output=dtemplate_matching.out
#SBATCH --cpus-per-task=30
#SBATCH --nodes=1
#SBATCH --nodelist=c05
#SBATCH --mem-per-cpu=15GB

module load matlab
module load imod/4.11.12

matlab -nodisplay < dtemplate_matching.m

