

clc;
rawTable = readmatrix("arduino_output3.txt");


D = rawTable(:, 1:3);
x = rawTable(:, 1);


N = length(x);
Ts = 1/300;
t = 0 : Ts: (N-1)*Ts;

fN = 600; % nyquist frequency
T = N*Ts; % signal duration

spec = fft(x);
magnitude = abs(spec);

freq = 0 : 1/T : (N/2 - 1)/T;

plot(freq, magnitude(1:length(freq))), title('|X(f)|'), 
axis([0,fN, 0, 1.2*max(magnitude)]), xlabel('f (Hz)');