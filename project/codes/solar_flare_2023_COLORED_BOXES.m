%% Solar flares 2023: side-by-side interval comparison and paired plots
% Put solar_flares_2023_clean.csv beside this script, then click Run.
clear; clc; close all;

% Find the data file beside the script (or select it manually).
scriptFile = mfilename('fullpath');
if isempty(scriptFile)
    scriptFolder = pwd;
else
    scriptFolder = fileparts(scriptFile);
end
csvFile = fullfile(scriptFolder, 'solar_flares_2023_clean.csv');
if exist(csvFile, 'file') ~= 2
    [name, folder] = uigetfile({'*.csv','CSV files (*.csv)'; '*.*','All files'}, ...
        'Select solar_flares_2023_clean.csv');
    if isequal(name,0), error('No CSV selected.'); end
    csvFile = fullfile(folder,name);
end
fprintf('Loading: %s\n',csvFile);

% This CSV has seven columns; columns 6/7 are rise_min and decay_min.
% Read using base MATLAB (no additional toolbox required).
fid = fopen(csvFile,'r');
if fid < 0, error('Cannot open CSV.'); end
header = fgetl(fid);
if ~ischar(header) || isempty(strfind(lower(header),'rise_min')) || ...
        isempty(strfind(lower(header),'decay_min'))
    fclose(fid);
    error('Select the cleaned CSV with rise_min and decay_min headers.');
end
raw = textscan(fid,'%s%s%s%s%f%f%f', 'Delimiter',',', ...
    'CollectOutput',false,'ReturnOnError',false);
fclose(fid);
riseTime = raw{6};
decayTime = raw{7};
if isempty(riseTime) || numel(riseTime)~=numel(decayTime)
    error('Could not read numeric columns 6 and 7.');
end
valid = isfinite(riseTime) & isfinite(decayTime) & riseTime>=0 & decayTime>=0;
riseTime = riseTime(valid);
decayTime = decayTime(valid);
N = numel(riseTime);
if N==0, error('No valid paired values were read.'); end

fprintf('Valid paired flares: %d\n',N);
fprintf('Rise: mean %.2f, median %.2f min\n',mean(riseTime),median(riseTime));
fprintf('Decay: mean %.2f, median %.2f min\n',mean(decayTime),median(decayTime));
fprintf('Decay > rise: %d | Rise > decay: %d | Equal: %d\n', ...
 sum(decayTime>riseTime+0.01),sum(riseTime>decayTime+0.01), ...
 sum(abs(decayTime-riseTime)<=0.01));

blue = [0.14 0.53 0.88];
orange = [1.00 0.60 0.18];

%% Figure 1: SIDE-BY-SIDE bar chart for 5-minute duration intervals
% We show 0-45 minutes for readability. Count longer values separately.
maxShown = 45;
edges = 0:5:maxShown;
riseCounts = histcounts(riseTime,edges);
decayCounts = histcounts(decayTime,edges);
labels = cell(1,numel(edges)-1);
for k=1:numel(labels)
    labels{k}=sprintf('%d-%d',edges(k),edges(k+1));
end
figure('Name','1 - Side by side durations','Color','w');
b = bar(1:numel(labels),[riseCounts(:),decayCounts(:)],'grouped');
b(1).FaceColor = blue;
b(2).FaceColor = orange;
set(gca,'XTick',1:numel(labels),'XTickLabel',labels,'FontSize',11);
xlabel('Duration interval (minutes)');
ylabel('Number of solar flares');
title('2023 Solar Flares: Rise vs Decay by Duration Interval');
legend({'Rise time','Decay time'},'Location','northeast');
grid on; box on;
fprintf('Plot 1 shows times up to 45 minutes. Rise >=45: %d; Decay >=45: %d\n', ...
    sum(riseTime>=45),sum(decayTime>=45));

%% Figure 2: box plots in DIFFERENT COLORS (blue rise, orange decay)
figure('Name','2 - Colored box plots','Color','w');
if exist('boxplot','file')==2
    % Each group gets its own color, including the median and whiskers.
    boxplot([riseTime;decayTime],[ones(N,1);2*ones(N,1)], ...
        'Labels',{'Rise','Decay'},'Colors',[blue;orange], ...
        'Widths',0.5,'Symbol','.');
    % Add a light colored fill to each box while preserving its lines.
    boxHandles = findobj(gca,'Tag','Box');
    for j=1:numel(boxHandles)
        xc = mean(get(boxHandles(j),'XData'));
        if xc < 1.5
            thisColor = blue;
        else
            thisColor = orange;
        end
        patch(get(boxHandles(j),'XData'),get(boxHandles(j),'YData'), ...
            thisColor,'FaceAlpha',0.25,'EdgeColor','none', ...
            'HandleVisibility','off');
    end
else
    % Fallback for MATLAB installations without Statistics Toolbox.
    hold on;
    groups={riseTime,decayTime};
    for k=1:2
        x=sort(groups{k}); n=numel(x);
        q1=x(max(1,ceil(.25*n)));
        med=median(x);
        q3=x(max(1,ceil(.75*n)));
        iqrVal=q3-q1;
        whiskLo=min(x(x>=q1-1.5*iqrVal));
        whiskHi=max(x(x<=q3+1.5*iqrVal));
        if k==1, thisColor=blue; else, thisColor=orange; end
        patch([k-.22 k+.22 k+.22 k-.22],[q1 q1 q3 q3], ...
            thisColor,'FaceAlpha',0.3,'EdgeColor',thisColor,'LineWidth',2);
        plot([k-.22 k+.22],[med med],'-','Color',thisColor,'LineWidth',3);
        plot([k k],[whiskLo q1],'-','Color',thisColor,'LineWidth',1.5);
        plot([k k],[q3 whiskHi],'-','Color',thisColor,'LineWidth',1.5);
        plot([k-.1 k+.1],[whiskLo whiskLo],'-','Color',thisColor);
        plot([k-.1 k+.1],[whiskHi whiskHi],'-','Color',thisColor);
    end
    xlim([0.5 2.5]); set(gca,'XTick',[1 2],'XTickLabel',{'Rise','Decay'});
end
set(gcf,'Color','w'); set(gca,'Color','w','XColor','k','YColor','k');
ylim([0 45]); grid on;
ylabel('Duration (minutes)');
title('Rise (blue) vs Decay (orange): Median and Spread (0-45 min)');

%% Figure 3: scatter with VISIBLE red equal-times line
figure('Name','3 - Paired rise and decay','Color','w');
scatter(riseTime,decayTime,14,blue,'filled'); hold on;
plot([0 45],[0 45],'--','Color',[1 0.1 0.1],'LineWidth',3.5);
xlim([0 45]); ylim([0 45]); axis square; grid on;
set(gca,'Color','w','XColor','k','YColor','k');
xlabel('Rise time (minutes)'); ylabel('Decay time (minutes)');
title('2023 Solar Flares: Rise vs Decay (zoomed to 45 min)');
legend({'Each flare','Equal rise and decay'},'Location','northwest');

fprintf('Completed all three figures.\n');
