clc;
rawTable = readmatrix("arduino_output.txt");
disp(rawTable)

D = rawTable(:, 1:3);
x = rawTable(:, 1);
y = rawTable(:, 2);
z = rawTable(:, 3);

[A,b,expmfs] = magcal(D); % Calibration coefficients

%expmfs % Display the expected magnetic field strength in uT
C = (D-b)*A; % Calibrated data

disp("///////////////////////////////////////////////////////////////////////")
disp(C)

disp(A)
disp(b)


figure(1)
plot3(x(:),y(:),z(:),"LineStyle","none","Marker","X","MarkerSize",8)

hold on
grid(gca,"on")

plot3(C(:,1),C(:,2),C(:,3),"LineStyle","none","Marker","o", "MarkerSize",8,"MarkerFaceColor","r")

axis equal
xlabel("uT")
ylabel("uT")
zlabel("uT")
legend("Uncalibrated Samples","Calibrated Samples","Location","southoutside")
title("Uncalibrated vs Calibrated" + newline + "Magnetometer Measurements")
hold off