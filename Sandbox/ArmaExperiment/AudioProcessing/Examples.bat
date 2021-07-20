python subsample.py -h
::  Prints help documentation

python subsample.py
:: 1. Saves "_Wind_800_2048_0.23-1.33_8bit.tsv"

python subsample.py -s Wrap -lp original -br 16 -v
:: 2. Outputs the data and plot of "_Wrap_original_2048_0.23-1.33_16bit"
:: and saves it as .tsv

python subsample.py -s Wind -lp 600 -sr 31250 -br 16 
:: 3. Saves "_Wind_600_31250_0.23-1.33_16bit.tsv"

python subsample.py -lp 600 -sr 31250 -st 1 -l 1 -br 12 
:: 4. Saves "_Wind_600_31250_1.0-2.0_12bit.tsv"

:: .tsv file name formats
:: 1. sound type - Wind or Wrap
:: 2. lowpass Hz - 400 ~ 1000 and original
:: 3. sample rate - any integer below 44100
:: 4. start time
:: 5. followed by end time - start and end time in the audio clip
:: 6. bit resolution - the scale of the sample when it is normalized.