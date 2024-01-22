import sys
import configparser as cfg

input_file = sys.argv[1]

config = cfg.ConfigParser()
config.read(input_file)

omega_m = config.getfloat('cosmology', 'omega_m', fallback=0.3)
omega_l = config.getfloat('cosmology', 'omega_l', fallback=0.7)

error_tolerance = config.getfloat('hyperparameters', 'error_tolerance', fallback=0.01)
depth = config.getint('hyperparameters', 'depth', fallback=3)

model = config.get('flags', 'model', fallback='local')
do_polarisation = config.getboolean('flags', 'do_polarisation', fallback=False)

output_filename = config.get('output', 'output_path')+"/"+config.get('output', 'output_name') \
    + "_"+str(omega_m)+"_"+str(omega_l)+"_"+str(error_tolerance)+"_"+str(depth)+"_"+str(model) \
    +"_"+str(do_polarisation)+".txt"

for i in range(depth):
    print(i)
    # do something clever to calculate something with error less than error_tolerance
    if(do_polarisation):
        print("do polarisation")
    else:
        print("do not polarisation")

output_data = 1.0

with open(output_filename, 'w') as f:
    f.write(str(output_data))
