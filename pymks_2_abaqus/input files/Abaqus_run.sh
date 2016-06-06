#PBS -N $number
#PBS -l nodes=1:ppn=2
#PBS -l mem=8000mb
#PBS -q prometheus
#PBS -l walltime=15:00:00
#PBS -j oe
#PBS -o out.$number

cd /gpfs/pace1/project/pme/pme1/awhite40
module load abaqus/6.13
echo " Processing inp file" $number "\n"
abaqus job=$number inp=$number cpus=2 mem=8000mb mp_mode=threads interactive