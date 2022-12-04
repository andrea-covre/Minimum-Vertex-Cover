cd %~dp0
FOR %%s IN (0 1 2 3 4 5 6 7 8 9) DO (
    FOR %%g IN (./data/star2.graph ./data/power.graph) DO (
        FOR %%a IN (LS1 LS2) DO python -m exec -inst %%g -alg %%a -time 1000 -seed %%s
    )
)

