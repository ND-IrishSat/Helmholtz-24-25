%% IrishSAT Helmholtz Cage B-Field Graphs
% Main Programmer: Andrew Collette 26'
% Assistance Programmer: Andres Perez 28'

% Plots B-field for 1 axis (coil pair) centered between coil pair
% Shows different B-fields given spacing tolerances
% The max acceptable length of CubeSat is where the B-field is within the
% red tolerance lines

% User-Defined Inputs
N = 100; % turns of wire
L = 2.5; % cage dimensions (length) in m
D = 0.5445*L; % spacing between coils in m (optimal=.5445*L)
I = 1; % current through coil in A
B_tolerance = 0.05;
D_tolerance = 0.05;

% Calculations
% Creates a linearly spaced vector between -2L to 2L with 10k pointers
z = linspace(-2*L, 2*L, 10000);

% This is B(z) - Equation (8)
B = B_field(N, I, L, z, D);

% Compute B(z) with tolerance 
B_high = B_field(N, I, L, z, D*(1+D_tolerance));
B_low = B_field(N, I, L, z, D*(1-D_tolerance));

% Magnetic field at the Center
B_max = B_field(N, I, L, D/2, D);

%% Plotting
% Ideal B
plot(z-D/2, B/B_max)
xlabel('z (m)')
ylabel('B-field (T)/B-field(O)')
title('Magnetic Field along the Axis')

% Wide and Thin Spacing B
hold on
plot(z-(D/2*(1+D_tolerance)), B_high/B_max, 'Color', "#77AC30")
plot(z-(D/2*(1-D_tolerance)), B_low/B_max, 'Color', "#7E2F8E")

% Horizontal and Vertical Lines
yline(B_max*(1+B_tolerance), 'r--', label="+"+B_tolerance*100+"%")
yline(B_max*(1-B_tolerance), 'r--', label="-"+B_tolerance*100+"%")
xline(0, 'b--', label="Center of Coils", LabelOrientation="horizontal")
hold off

grid on
legend('Ideal B', 'B with Wide Spacing', 'B with Thin Spacing', location = 'southwest')

%% Functions
% Auxiliar Function 
function func = aux_f(z, L)
    alp = z ./ (L / 2); % Element-wise division
    func = 1 ./ (((alp.^2) + 1) .* ((alp.^2) + 2).^(1/2)); % Element-wise operations
end

% Total Magnetic Field along the coil - Equation (8)
function B = B_field(N, I, L, z, D)
    mu0 = 4 * 3.1415 * 10^(-7); % Permeability of free space
    B = ((4 * mu0 * N * I) / (3.1415 * L)) * ((aux_f(z, L)) + aux_f(z - D, L)); % Element-wise multiplication
end

