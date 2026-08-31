% Alex Masarie
% September 7, 2016
% Main function of point-to-point distance estimator.
% Important references are:
%    Dijsktra's algorithm -
%        Bertsimas, Dimitris and Tsitsiklis, John N. Introduction to
%           Linear Optimization.  Athena Scientific, Dynamic Ideas:
%           Belmont, MA. 1997. 587 p.
%        Kirk, Joseph. DIJKSTRA Calculate Minimum Costs and Paths
%           using Dijkstra's Algorithm. See: dijkstra.m 2015
%    Google Earth -
%        Brown, Martin C. Hacking Google Maps and
%           Google Earth. Wiley Publishing Inc:Indianapolis,IN.
%           2006 373 p.
%        Google Earth software

% This function is designed to interface with a static Google maps dataset
% This is a network with fixed nodes and positive arc costs assigned by
% distance.

function [ optimal ] = main_DistCalc( rte,roads,plotTOGGLE )
% Please consult README.txt for file type information.
% INPUTS:
%       rte = (longitude,latitude,elevation) of initial point
%       plotTOGGLE = set to true(1) when we want to inspect plots
% OUTPUTS:
%       dist = cumulative distance of optimal route (curvature corrected)
%       optimalPath = connection nodes of optimal route

%logfp = fopen('C:\Users\masariat\Documents\MATLAB\LOG.txt','w');
%fprintf(logfp,'    Welcome to main_DistCalc.m');
%tic;

% If not supplied, incorporate elevation
%TODO

% Initialize plots
if plotTOGGLE
    % Load mesh MATLAB struct (don't care about run time)
    load('C:\Users\Alex\Documents\MATLAB\ALOC8\Datasets\Omega\OUTPUT\meshes.mat');
    fig = figure('Visible','off');
    hold on;
    plot(roads.arcs(:,1),roads.arcs(:,2),'m.');
    for ii = 1:13
        plot(mesh(ii).outline(:,1),mesh(ii).outline(:,2),'k');
    end
    for pp = 1:size(rte,1)-1
        scatter(rte(pp,1),rte(pp,2),'bs'); %Initial point
        scatter(rte(pp+1,1),rte(pp+1,2),'bs'); %Terminal point
    end
    xlabel('Longitude (deg NAD83)');
    ylabel('Latitude (deg NAD83)');
    title({'Optimal Routing';'with Dijkstra Algorithm'});
    grid on;
    set(gca,'FontSize',13);
    xlim([-180.0 -60.0]);
    ylim([25 78]);
    set(fig,'Visible','on');
end

%% Local routing
%fprintf(logfp,'        Routing from location into network...\n');
% Route in straight line to closest arc point
optimal(size(rte,1)).aa = []; %Initialize storage for arc number
optimal(size(rte,1)).idx = []; %Initialize storage for points within arc
% Find nearest arc to each route point
for pp = 1:size(rte,1) %For each route point
    minTracker = inf; %Initilize minimum tracker
    for aa = 1:numel(roads.arcCellArray)-1 %For each arc in cell array
        vecE = ones(size(roads.arcCellArray{aa},1),1); %Vector of ones
        temp = ((roads.arcCellArray{aa}(:,1) - rte(pp,1).*vecE).^2 +...
            (roads.arcCellArray{aa}(:,2) - rte(pp,2).*vecE).^2).^0.5; %Compute the distance to arc points
        [ extraDist,idx ] = min(temp); %Find minimum distance
        if extraDist < minTracker %If this is a new best
            optimal(pp).aa = aa; %Flag this arc for this route point
            optimal(pp).idx = idx; %Flag this point within arc as closest
            minTracker = extraDist; %Update minimum tracker
        end
    end
end

%% Global routing
%fprintf(logfp,'        Compiling best route through network...\n');
optimal(size(rte,1)).ndPath = []; %This will store nodes along best route
optimal(size(rte,1)).cost = []; %This will store minimum distance
optimal(size(rte,1)-1).arcPath = []; %This will store arcs along best route
for pp = 1:size(rte,1)-1 %For each pair of route points (in order)
    % There will be 4 candidates for optimal paths
    minTracker = inf;
    for vv = 1:4 %Four viable candidate routes
        switch vv %Initialize depending on which combo
            case 1
                % Starting initial point to Destination initial point
                ndA = roads.E3(optimal(pp).aa,1);
                ndB = roads.E3(optimal(pp+1).aa,1);
            case 2
                % Starting initial point to Destination terminal point
                ndA = roads.E3(optimal(pp).aa,1);
                ndB = roads.E3(optimal(pp+1).aa,2);
            case 3
                % Starting terminal point to Destination initial point
                ndA = roads.E3(optimal(pp).aa,2);
                ndB = roads.E3(optimal(pp+1).aa,1);
            case 4
                % Starting terminal point to Destination terminal point
                ndA = roads.E3(optimal(pp).aa,2);
                ndB = roads.E3(optimal(pp+1).aa,2);
        end
        % Extra distance to get to nearest arc point
        extraDist = earthDist(rte(pp,:),...
            roads.arcCellArray{optimal(pp).aa}(optimal(pp).idx,:));
        % Extra distance to node
        extraDist = extraDist +...
            earthDist(roads.arcCellArray{optimal(pp).aa}(optimal(pp).idx,:),...
                roads.nds(ndA,:));
        % Extra distance to nearest arc point
        extraDist = extraDist +...
            earthDist(roads.nds(ndB,:),...
                roads.arcCellArray{optimal(pp+1).aa}(optimal(pp+1).idx,:));
        % Extra distance to route point
        extraDist = extraDist +...
            earthDist(roads.arcCellArray{optimal(pp+1).aa}(optimal(pp+1).idx,:),...
                rte(pp+1,:));
        % Query best path from ndA to ndB
        path = roads.paths(ndA,ndB);
        path = path{:}; %Unpack cell array
        for jj = 1:numel(path)-1 %For each consecutive pair of path points
            % Cumulative sum of distance along path
            extraDist = extraDist + roads.costs(path(jj),path(jj+1));
        end
        if extraDist < minTracker %If this route is shorter
            optimal(pp).ndPath = path; %Update nearest path
            optimal(pp).cost = extraDist; %Update cost for this path
            minTracker = extraDist; %Set minTracker to new min
        end
    end %End testing for best local route
    for jj = 1:numel(optimal(pp).ndPath)-1 %For each pair of path points
        bb = find( (roads.E3(:,1) == optimal(pp).ndPath(jj)) &...
            (roads.E3(:,2) == optimal(pp).ndPath(jj+1)) );
        if isempty(bb)
            bb = find( (roads.E3(:,2) == optimal(pp).ndPath(jj)) &...
                (roads.E3(:,1) == optimal(pp).ndPath(jj)) );
        else
            bb = bb(1);
            if bb > numel(roads.arcCellArray) || isempty(bb) %If this was a negative trace
                bb = find( (roads.E3(:,2) == optimal(pp).ndPath(jj)) &...
                    (roads.E3(:,1) == optimal(pp).ndPath(jj+1)) );
                bb = bb(1);
            end
        end
        optimal(pp).arcPath = [ optimal(pp).arcPath;bb ]; %Connect arc info to path
        if plotTOGGLE
            plot(roads.arcCellArray{bb}(:,1),roads.arcCellArray{bb}(:,2),'b-','LineWidth',1.15);
            scatter(roads.nds(optimal(pp).ndPath(jj),1),...
                roads.nds(optimal(pp).ndPath(jj),2),'rs');
            if jj == numel(optimal(pp).ndPath) - 1 %On last point
                scatter(roads.nds(optimal(pp).ndPath(jj+1),1),...
                    roads.nds(optimal(pp).ndPath(jj+1),2),'rs');
                annotation('textbox',...
                    [0.58,0.7,0.1,0.1],'String',...
                    sprintf('Path length = %.2f mi',optimal(pp).cost));
            end
        end
    end
end
% Report to log file we have finished
%fprintf(logfp,['    DONE, Runtime was ' num2str(toc) ' seconds']);
%fclose(logfp); %Close log file

end