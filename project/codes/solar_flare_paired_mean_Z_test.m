%% SOLAR FLARES 2023: PAIRED MEAN Z-TEST (LARGE-SAMPLE APPROXIMATION)
% Reads solar_flares_2023_clean(1).csv or solar_flares_2023_clean.csv.
% If neither is found beside this script or in the current folder,
% MATLAB asks you to select the CSV file.
%
% Each row is ONE flare, with BOTH its rise_min and decay_min measurements.
% Do not use the independent two-sample Z formula on these paired data.
%
% H0: population mean(rise - decay) = 0
% H1: population mean(rise - decay) > 0
%
% With unknown population SD, the Z result below is a LARGE-SAMPLE
% approximation. A paired t-test is also reported for comparison.

clear; clc;
format long g;
alpha = 0.05;                     % Significance level

%% 1. FIND AND LOAD THE CSV
scriptLocation = mfilename('fullpath');
if isempty(scriptLocation)
    scriptFolder = pwd;
else
    scriptFolder = fileparts(scriptLocation);
end

possibleNames = {'solar_flares_2023_clean(1).csv', ...
                 'solar_flares_2023_clean.csv'};
searchFolders = {scriptFolder, pwd};
csvFile = '';
for j = 1:numel(searchFolders)
    for k = 1:numel(possibleNames)
        candidate = fullfile(searchFolders{j}, possibleNames{k});
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
    [fileName, folderName] = uigetfile('*.csv', ...
        'Select your solar_flares_2023_clean CSV file');
    if isequal(fileName, 0)
        error('No CSV was selected. Please select your solar-flare CSV.');
    end
    csvFile = fullfile(folderName, fileName);
end

T = readtable(csvFile);
if ~all(ismember({'rise_min','decay_min'}, T.Properties.VariableNames))
    error('CSV must have columns named rise_min and decay_min.');
end

rise = T.rise_min;
decay = T.decay_min;
if ~isnumeric(rise) || ~isnumeric(decay)
    error('rise_min and decay_min must contain numeric values.');
end
rise = double(rise(:));
decay = double(decay(:));
valid = isfinite(rise) & isfinite(decay) & rise >= 0 & decay >= 0;
numberRemoved = sum(~valid);
rise = rise(valid);
decay = decay(valid);
n = numel(rise);
if n < 2
    error('Need at least 2 valid rise/decay pairs.');
end

%% 2. CALCULATE SUMMARY STATISTICS AND PAIRED DIFFERENCES
d = rise - decay;                  % Positive: rise took longer
meanRise = mean(rise);
meanDecay = mean(decay);
medianRise = median(rise);
medianDecay = median(decay);
meanD = mean(d);                   % Equal to meanRise - meanDecay
sdD = std(d, 0);                   % Sample SD: divides by n-1
seD = sdD / sqrt(n);               % Standard error of mean difference

%% 3. PAIRED MEAN Z-TEST (NORMAL APPROXIMATION)
% H0: mu_d = 0; H1: mu_d > 0
if seD == 0
    error('All paired differences are identical: cannot calculate a usual Z test.');
end
z = meanD / seD;
% Normal distribution tail probabilities without Statistics Toolbox:
pRight = 0.5 * erfc(z / sqrt(2));
pTwoSided = erfc(abs(z) / sqrt(2));
zCritical = sqrt(2) * erfinv(1 - alpha);    % 1.64485 for right tail
zCI = sqrt(2) * erfinv(1 - alpha/2);        % 1.95996 for 95%% CI
ciLower = meanD - zCI * seD;
ciUpper = meanD + zCI * seD;

%% 4. PAIRED t-TEST FOR COMPARISON (MORE STANDARD WITH UNKNOWN SD)
% Same numerical statistic, but use t distribution with n-1 df.
% betainc computes t probabilities without the Statistics Toolbox.
df = n - 1;
tStat = z;
x = df / (df + tStat^2);
tailMagnitude = 0.5 * betainc(x, df/2, 0.5);
if tStat >= 0
    pRightT = tailMagnitude;
else
    pRightT = 1 - tailMagnitude;
end
pTwoT = 2 * tailMagnitude;

%% 5. PRINT EVERYTHING IN THE MATLAB COMMAND WINDOW
fprintf('\n=============================================================\n');
fprintf('SOLAR FLARES: RISE TIME VS DECAY TIME\n');
fprintf('PAIRED MEAN Z-TEST (LARGE-SAMPLE NORMAL APPROXIMATION)\n');
fprintf('=============================================================\n');
fprintf('Loaded file: %s\n', csvFile);
fprintf('Number of original CSV rows: %d\n', height(T));
fprintf('Number of complete, nonnegative pairs: %d\n', n);
fprintf('Rows excluded for missing/invalid times: %d\n', numberRemoved);

fprintf('\n--- SUMMARY STATISTICS (MINUTES) ---\n');
fprintf('Mean rise time                 : %.6f\n', meanRise);
fprintf('Mean decay time                : %.6f\n', meanDecay);
fprintf('Median rise time               : %.6f\n', medianRise);
fprintf('Median decay time              : %.6f\n', medianDecay);
fprintf('Mean paired difference (rise - decay): %.6f\n', meanD);
fprintf('Check: mean rise - mean decay  : %.6f\n', meanRise-meanDecay);
fprintf('Sample SD of paired differences: %.6f\n', sdD);
fprintf('Standard error of mean difference: %.6f\n', seD);

fprintf('\n--- FIRST TEN PAIRED OBSERVATIONS ---\n');
fprintf(' Flare       Rise      Decay     Difference\n');
for k = 1:min(10,n)
    fprintf('%5d %10.2f %10.2f %12.2f\n',k,rise(k),decay(k),d(k));
end

fprintf('\n--- HYPOTHESES ---\n');
fprintf('H0: population mean(rise - decay) = 0 minutes\n');
fprintf('H1: population mean(rise - decay) > 0 minutes\n');
fprintf('One-sided right-tail test; alpha = %.3f\n', alpha);

fprintf('\n--- PAIRED MEAN Z-TEST APPROXIMATION ---\n');
fprintf('Z = mean difference / (sample SD / sqrt(n))\n');
fprintf('Z statistic                   : %.6f\n', z);
fprintf('Right-tailed p-value          : %.8f\n', pRight);
fprintf('Two-sided p-value (reference) : %.8f\n', pTwoSided);
fprintf('Right-tail critical Z         : %.6f\n', zCritical);
fprintf('95%% normal CI for mean difference: [%.6f, %.6f] minutes\n',ciLower,ciUpper);
if pRight < alpha
    fprintf('DECISION: REJECT H0 at alpha = %.2f.\n', alpha);
    fprintf('Evidence supports a POSITIVE population mean difference.\n');
else
    fprintf('DECISION: FAIL TO REJECT H0 at alpha = %.2f.\n', alpha);
    fprintf('Insufficient evidence of a POSITIVE population mean difference.\n');
end

fprintf('\n--- PAIRED t-TEST COMPARISON (SD UNKNOWN) ---\n');
fprintf('t statistic                   : %.6f\n', tStat);
fprintf('Degrees of freedom            : %d\n', df);
fprintf('Right-tailed t p-value        : %.8f\n', pRightT);
fprintf('Two-sided t p-value           : %.8f\n', pTwoT);

fprintf('\n--- DATA QUALITY NOTES ---\n');
fprintf('Maximum rise time             : %.2f minutes\n', max(rise));
fprintf('Maximum decay time            : %.2f minutes\n', max(decay));
[~, order] = sort(abs(d), 'descend');
fprintf('Largest 5 absolute paired differences (min): ');
for k = 1:min(5,n)
    fprintf('%.0f ', d(order(k)));
end
fprintf('\n');
fprintf('All valid observations were retained, including extreme values.\n');
fprintf('Very long events may strongly affect the mean and standard error.\n');
fprintf('Check dependence between flare events and influential outliers.\n');
fprintf('Population SD was not known: Z is an approximation, not exact.\n');
fprintf('The paired t-test is the conventional analysis with unknown SD.\n');
fprintf('The two-sided p-value answers a DIFFERENT hypothesis (mu_d ~= 0).\n');
fprintf('=============================================================\n\n');
