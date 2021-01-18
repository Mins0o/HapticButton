slice = [120001,130000];
[y,Fs] = audioread("8.wav",slice);
model = armax(y(:,1),[10,7]);
