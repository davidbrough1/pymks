
import os

for i in range(1, 121):
    os.system('abaqus -j 71_' + str(i) + '_fibers.inp inter')

