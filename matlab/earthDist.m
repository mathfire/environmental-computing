function dist = earthDist(ptA,ptB)

radiusEarth = 3959; %miles
% Curvature-corrected distances in miles
lngdistance = pi*(ptB(1,1) - ptA(1,1))/180.0; %Longitude
latdistance = pi*(ptB(1,2) - ptA(1,2))/180.0; %Latitude
alpha = sin(latdistance/2.0)*sin(latdistance/2.0) +... %Intermediary
    cos(pi*ptA(1,2)/180.0)*cos(pi*ptB(1,2)/180.0)*sin(lngdistance/2.0)*sin(lngdistance/2.0);
beta = 2.0*atan2(sqrt(alpha),sqrt(1-alpha)); %Intermediary
dist = radiusEarth*beta; %Cumulative sum

end