%% Solar flares (2023): Two PDF plots requested by the professor
% Put this script in the same folder as solar_flares_2023_clean(2).csv.
% Run the entire script. No Statistics Toolbox is required.
clear; clc; close all;

%% 1. Find and read the CSV file
scriptPath = mfilename('fullpath');
if isempty(scriptPath)
    folder = pwd;
else
    folder = fileparts(scriptPath);
end
csvFile = fullfile(folder, 'solar_flares_2023_clean(2).csv');
if ~isfile(csvFile)
    [fileName, fileFolder] = uigetfile('*.csv', 'Select your solar flare CSV');
    if isequal(fileName,0)
        error('No CSV file was selected.');
    end
    csvFile = fullfile(fileFolder, fileName);
    folder = fileFolder;
end
T = readtable(csvFile);

%% 2. Use the paired rise and decay times, in minutes
riseTime = T.rise_min;
decayTime = T.decay_min;
valid = isfinite(riseTime) & isfinite(decayTime) & ...
        riseTime >= 0 & decayTime >= 0;
riseTime = riseTime(valid);
decayTime = decayTime(valid);
d = riseTime - decayTime;   % Difference for EACH flare

fprintf('Flares used: %d\n', numel(d));
fprintf('Mean rise time: %.2f min\n', mean(riseTime));
fprintf('Mean decay time: %.2f min\n', mean(decayTime));
fprintf('Mean difference (rise - decay): %.2f min\n', mean(d));
fprintf('Rise longer: %d; decay longer: %d; equal: %d\n', ...
    sum(d>0), sum(d<0), sum(d==0));

%% 3. FIGURE 1: PDF of paired differences (rise minus decay)
% Show the middle 98%% of values on the x axis for readability.
% IMPORTANT: ALL observations are used to calculate the PDF.
orderedD = sort(d);
n = numel(d);
leftD  = orderedD(max(1,ceil(0.01*n)));
rightD = orderedD(min(n,ceil(0.99*n)));
xD = linspace(min(leftD,0)-3, max(rightD,0)+3, 500);
pdfD = gaussianPDF(d, xD, 1.5);  % Kernel-density estimate

fig1 = figure('Color','w');
plot(xD, pdfD, 'b-', 'LineWidth', 2); hold on;
xline(0, 'k--', 'Zero difference', 'LineWidth', 1.4);
xline(mean(d), 'r-', sprintf('Mean d = %.2f min',mean(d)), ...
    'LineWidth', 1.4);
xlabel('Difference d = Rise time - Decay time (minutes)');
ylabel('Probability density (1/minute)');
title('PDF of Paired Rise-Decay Differences: Solar Flares 2023');
legend('PDF of differences','d = 0','Mean difference','Location','best');
grid on; box on;
xlim([xD(1) xD(end)]);
exportgraphics(fig1, fullfile(folder,'PDF_1_paired_difference.png'), 'Resolution',200);

%% 4. FIGURE 2: PDFs of rise times and decay times
% Same x-axis for both curves; again all observations are used.
allTimes = sort([riseTime; decayTime]);
m = numel(allTimes);
rightT = allTimes(min(m,ceil(0.99*m)));
xT = linspace(0, rightT+5, 500);
pdfRise  = gaussianPDF(riseTime, xT, 1.5);
pdfDecay = gaussianPDF(decayTime, xT, 1.5);

fig2 = figure('Color','w');
plot(xT,pdfRise,'r-','LineWidth',2); hold on;
plot(xT,pdfDecay,'b-','LineWidth',2);
xline(mean(riseTime),'r--',sprintf('Mean rise = %.2f',mean(riseTime)), ...
    'LineWidth',1.2);
xline(mean(decayTime),'b--',sprintf('Mean decay = %.2f',mean(decayTime)), ...
    'LineWidth',1.2);
xlabel('Time (minutes)');
ylabel('Probability density (1/minute)');
title('PDF Comparison of Rise and Decay Times: Solar Flares 2023');
legend('Rise-time PDF','Decay-time PDF','Mean rise','Mean decay', ...
    'Location','best');
grid on; box on;
xlim([xT(1) xT(end)]);
exportgraphics(fig2, fullfile(folder,'PDF_2_rise_vs_decay.png'), 'Resolution',200);

disp('Finished. Both PDF figures were saved in the CSV folder.');

%% Local function: Gaussian kernel PDF (no extra toolbox needed)
function density = gaussianPDF(values, xgrid, bandwidth)
    values = values(:);
    density = zeros(size(xgrid));
    for j = 1:numel(xgrid)
        z = (xgrid(j) - values) / bandwidth;
        density(j) = mean(exp(-0.5*z.^2)) / (bandwidth*sqrt(2*pi));
    end
end
