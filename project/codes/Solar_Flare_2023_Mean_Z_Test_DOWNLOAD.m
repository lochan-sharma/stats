%% SOLAR FLARES 2023 - DEVORE SECTION 9.1 TWO-SAMPLE MEAN Z-TEST
% Hypotheses (right-tailed):
%   H0: mu_rise - mu_decay = 0
%   H1: mu_rise - mu_decay > 0
%


clear; clc;
alpha = 0.05;
delta0 = 0;  % Hypothesized difference under H0

%% 1. FIND AND LOAD THE CSV FILE
scriptFullPath = mfilename('fullpath');
if isempty(scriptFullPath)
    scriptFolder = pwd;
else
    scriptFolder = fileparts(scriptFullPath);
end
fileNames = {'solar_flares_2023_clean(1).csv', ...
             'solar_flares_2023_clean.csv'};
folders = {scriptFolder, pwd};
csvFile = '';
for i = 1:numel(folders)
    for j = 1:numel(fileNames)
        candidate = fullfile(folders{i}, fileNames{j});
        if exist(candidate, 'file') == 2
            csvFile = candidate;
            break;
        end
    end
    if ~isempty(csvFile)
        break;
    end
end
if isempty(csvFile)
    [fileName, fileFolder] = uigetfile('*.csv', ...
        'Select solar_flares_2023_clean CSV file');
    if isequal(fileName, 0)
        error('No CSV file was selected.');
    end
    csvFile = fullfile(fileFolder, fileName);
end

T = readtable(csvFile);
if ~all(ismember({'rise_min', 'decay_min'}, T.Properties.VariableNames))
    error('The CSV must contain rise_min and decay_min columns.');
end
riseAll = T.rise_min;
decayAll = T.decay_min;
if ~isnumeric(riseAll) || ~isnumeric(decayAll)
    error('The rise_min and decay_min columns must contain numbers.');
end
riseAll = double(riseAll(:));
decayAll = double(decayAll(:));
valid = isfinite(riseAll) & isfinite(decayAll) & ...
        (riseAll >= 0) & (decayAll >= 0);
removed = sum(~valid);
rise = riseAll(valid);
decay = decayAll(valid);
if numel(rise) < 2 || numel(decay) < 2
    error('Need at least two valid flare observations.');
end

%% 2. DESCRIPTIVE STATISTICS
n1 = numel(rise);
n2 = numel(decay);
xbar1 = mean(rise);
xbar2 = mean(decay);
s1 = std(rise, 0);         % Sample SD: denominator n1-1
s2 = std(decay, 0);        % Sample SD: denominator n2-1
observedDifference = xbar1 - xbar2;

%% 3. DEVORE SECTION 9.1 FORMULA (NORMAL APPROXIMATION)
%   Z = [(Xbar1 - Xbar2) - delta0] / sqrt(s1^2/n1 + s2^2/n2)
% The exact Section 9.1 Z test would use KNOWN sigma1 and sigma2,
% not estimates s1 and s2. Here, s1 and s2 are used for approximation.
SE = sqrt(s1^2/n1 + s2^2/n2);
Z = (observedDifference - delta0)/SE;

% Standard normal tail probabilities using erfc (no Statistics Toolbox)
pRight = 0.5 * erfc(Z/sqrt(2));
pTwoSided = erfc(abs(Z)/sqrt(2));

% 95%% two-sided normal-approximation CI
zCritical95 = sqrt(2)*erfcinv(alpha);  % 1.95996 for alpha=0.05
ciLower = observedDifference - zCritical95*SE;
ciUpper = observedDifference + zCritical95*SE;

%% 4. PRINT EVERYTHING IN COMMAND WINDOW
fprintf('\n===========================================================\n');
fprintf('SOLAR FLARES 2023 - DEVORE SECTION 9.1 MEAN Z-TEST\n');
fprintf('===========================================================\n');
fprintf('CSV file: %s\n', csvFile);
fprintf('Valid flare rows: %d\n', n1);
fprintf('Excluded rows with invalid values: %d\n', removed);
fprintf('\nDESCRIPTIVE STATISTICS\n');
fprintf('Rise:  mean = %.6f min, median = %.3f min, SD = %.6f min\n', ...
    xbar1, median(rise), s1);
fprintf('Decay: mean = %.6f min, median = %.3f min, SD = %.6f min\n', ...
    xbar2, median(decay), s2);
fprintf('Sample sizes: n1 = %d, n2 = %d\n', n1, n2);
fprintf('Difference in sample means = %.6f min\n', observedDifference);
fprintf('\nHYPOTHESES (ONE-SIDED RIGHT-TAIL)\n');
fprintf('H0: mu_rise - mu_decay = 0\n');
fprintf('H1: mu_rise - mu_decay > 0\n');
fprintf('Significance level alpha = %.3f\n', alpha);
fprintf('\nSECTION 9.1 Z FORMULA WITH SAMPLE SD APPROXIMATION\n');
fprintf('SE = sqrt(s_rise^2/n1 + s_decay^2/n2) = %.6f min\n', SE);
fprintf('Z = ((mean rise - mean decay) - 0)/SE = %.6f\n', Z);
fprintf('One-sided (right-tail) p-value = %.8f\n', pRight);
fprintf('Two-sided p-value (for reference) = %.8f\n', pTwoSided);
fprintf('95%% two-sided normal CI for mean difference: [%.6f, %.6f] min\n', ...
    ciLower, ciUpper);
fprintf('\nDECISION FOR THE ONE-SIDED TEST\n');
if pRight < alpha
    fprintf('Reject H0 at alpha = %.2f.\n', alpha);
    fprintf('Evidence supports a greater population mean rise time.\n');
else
    fprintf('Fail to reject H0 at alpha = %.2f.\n', alpha);
    fprintf('Insufficient evidence that population mean rise time is greater.\n');
end
fprintf('===========================================================\n\n');
