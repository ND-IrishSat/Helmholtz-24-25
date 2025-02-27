

clc;
rawTable = readtable("magFieldsOut.csv");

x = table2array(rawTable(:, "X"));
y = table2array(rawTable(:, "Y"));
z = table2array(rawTable(:, "Z"));

N = length(y);
Ts = 1/300;
t = 0 : Ts: (N-1)*Ts;

fN = 600; % nyquist frequency
T = N*Ts; % signal duration

spec = fft(y);
magnitude = abs(spec);

freq = 0 : 1/T : (N/2 - 1)/T;

plot(freq, magnitude(1:length(freq))), title('|X(f)|'), 
axis([0,fN, 0, 1.2*max(magnitude)]), xlabel('f (Hz)');