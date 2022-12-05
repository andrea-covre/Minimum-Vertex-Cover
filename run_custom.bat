cd %~dp0
@echo off
echo select graph, algorithm and repeat times
set /p g= graph: star2/power(s/p): 
set /p a= algo: LS!1/LS2(1/2): 
set /p n= repeat #:
set /p t= time: 
if %g%==s set graph=./data/star2.graph
if %g%==p set graph=./data/power.graph
if %a%==1 set algo=LS1
if %a%==2 set algo=LS2
if %a%==3 set algo=Approx
if %a%==4 set algo=BnB

set /a i=0
:loop1
python -m exec -inst %graph% -alg %algo% -time %t% -seed %Random%
set /a i=%i%+1
if %i% neq %n% goto loop1