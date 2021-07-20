try:
    from Wav2Float import wav2float
    from PCMProcessing import *
    import matplotlib.pyplot as plt
    import numpy as np
    import argparse
except Exception as e:
    print(e)
    input()

parser = argparse.ArgumentParser()

##############################
######### Settings ###########

base_directory = r"./"
# Where the audio is located

sound = "Wind"
# Available options: "Wind", "Wrap"

low_pass_hz = "original"
# Available options: "original", "400", "600", "800", "1000"

target_sample_rate = 2048
# Any integer value

start = 0.23
# Start of the audio file in seconds
target_length = 1.1
# In seconds, floating point. The unmirrored will have half the length

output_bit_resolution = 8
# bit resolution of the output. 8 will give the data in integer range of [0,255]
# 32 bit will not give proper output for most of the machines

verbose = False

parser.add_argument('-bd', '--base_dir', type = str, default = r'./', help = "Where the audio is located. \nDefault is current directory './'")
parser.add_argument('-s', '--sound', type = str, default = "Wind", help = "The name of the sound source. \nDefault is 'Wind' and available options are 'Wind' and 'Wrap'")
parser.add_argument('-lp', '--low_pass', type = str, default = '800', help = "The frequency of lowpass to select. \nThis does not mean this program will apply low pass filter. \nThe audio file should have multiple versions, with different lowpass filter applied should be labeled. This parameter only acts as a selector for those files.\nDefault is '800', and available options include 'original', '400', '600', '800', '1000'")
parser.add_argument('-sr', '--sample_rate', type = int, default = 2048, help = "This is the target sampling rate to output. It should be lower than the audio files' sampling rate (44100).\nDefault value is 2048. This must be an integer value.")
parser.add_argument('-st', '--start', type = float, default = 0.23, help = "This is the starting point of the audio clip you want to use.\nDefault is 0.23, and the start of the output sequence will be the 0.23 seconds point of the target audio clip if no other value is specified.")
parser.add_argument('-l', '--length', type = float, default = 1.1, help = "This is the length of the clip you want to use, starting from the starting point in the clip. If the duration of the clip is shorter than the given value, the output will be processed until the end of the clip.\nDefault value is 1.1 seconds. The value should be positive")
parser.add_argument('-br', '--bit_resolution', type = int, default = 8, help = "The output sequences' bit resolution can be specified here. That is, if the default value 8 is used, the data will be in integer range of [0,255].\nDefault is 8.")
parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "By adding this argument, you enable verbose. This will print out the output sequence of un-mirrored and mirrored data and also show a simple plot of the data.\nNo value is neeeded to be provided.")

args = parser.parse_args()

base_directory = args.base_dir
sound = args.sound
low_pass_hz = args.low_pass
target_sample_rate = args.sample_rate
start = args.start
target_length = args.length
output_bit_resolution = args.bit_resolution
verbose = args.verbose

##############################
##############################

if low_pass_hz == "original":
    file_name = sound + "_" + low_pass_hz + ".wav"
else:
    file_name = sound + "_" + low_pass_hz + "_filtered.wav"
file_path = base_directory + file_name
try:
    audio = (wav2float(file_path))[int(start*44100):int(44100*(start + target_length/2))]
except Exception as e:
    print(e)
    input()

# DecreaseFrequency examples
sampled_800 = DecreaseFrequency(list(audio),44100,800)
sampled_2048 = DecreaseFrequency(list(audio),44100,2048)
sampled_5000 = DecreaseFrequency(list(audio),44100,5000)
sampled_10k = DecreaseFrequency(list(audio),44100,10000)
sampled_25k = DecreaseFrequency(list(audio),44100,25000)
sampled_31k = DecreaseFrequency(list(audio),44100,31250)

sampled_target = DecreaseFrequency(list(audio),44100,target_sample_rate)

normalizing_target = sampled_target

###############################
######### normalizing #########
max_int = 2**output_bit_resolution
normalized = np.array(normalizing_target, dtype = np.longfloat)
normalized = normalized - normalized.mean()
normalized = normalized / max(abs(normalized))
normalized += 1
normalized *= 2**(output_bit_resolution-1)

# Check max clip
indices_of_clipped = normalized > (max_int-1)
normalized[indices_of_clipped] = (max_int-1)
# Check 0 clip
indices_of_clipped = normalized < 0
normalized[indices_of_clipped] = 0

output_data = normalized.astype(int)

if verbose:
    print("Normalized, unmirrored")
    print(list(output_data))
    print("Length")
    print(len(output_data))
    print()
###############################
###############################

### mirroring to avoid knocking at loop ###
output_data = list(output_data)

mirrored = output_data.copy()
mirrored.reverse()
combined = output_data+mirrored
if verbose:
    print("Normalized, mirrored")
    print(combined)
    print("Length")
    print(len(combined))
    print("Average of the data")
    print(np.average(combined))
    print()

# Save as .tsv
with open(base_directory+"_"+sound+"_"+low_pass_hz+"_"+str(target_sample_rate)+"_"+str(start)+"-"+str(start+target_length)+"_"+str(output_bit_resolution)+"bit.tsv",'w') as file:
    for i in output_data:
        file.write(str(i)+"\n")
with open(base_directory+"_"+sound+"_"+low_pass_hz+"_"+str(target_sample_rate)+"_"+str(start)+"-"+str(start+target_length)+"_"+str(output_bit_resolution)+"bit_mirrored.tsv",'w') as file:
    for i in combined:
        file.write(str(i)+"\n")
    
if verbose:
    plt.subplot(221)
    plt.plot(audio)
    plt.title("Original")
    plt.subplot(223)
    plt.plot(output_data)
    plt.title("Subsampled")
    plt.subplot(224)
    plt.plot(combined)
    plt.title("Mirrored")
    plt.show()