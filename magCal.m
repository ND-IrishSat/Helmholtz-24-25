clc;
rawTable = readmatrix("magnetometer_data.txt");

D = rawTable(:, 2:4);
x = rawTable(:, 2);
y = rawTable(:, 3);
z = rawTable(:, 4);

[A,b,expmfs] = magcal(D); % Calibration coefficients
expmfs % Display the expected magnetic field strength in uT
C = (D-b)*A; % Calibrated data

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