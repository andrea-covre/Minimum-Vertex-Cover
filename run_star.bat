cd %~dp0
FOR %%s IN (10 11 12 13 14 15 16 17 18 19) DO (
    FOR %%g IN (./data/as-22july06.graph ./data/delaunay_n10.graph ./data/dummy1.graph ./data/dummy2.graph ./data/email.graph ./data/football.graph ./data/hep-th.graph ./data/jazz.graph ./data/karate.graph ./data/netscience.graph ./data/star.graph) DO (
        FOR %%a IN (LS2) DO python -m exec -inst %%g -alg %%a -time 100 -seed %%s
    )
)

