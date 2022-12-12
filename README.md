Thanh Son Phung

The hash table servers run on studentxx.crc.nd.edu, where xx is in the set {05,10,11,12,13} depending on how many servers we want, and clients run on student04.crc.nd.edu. Each operation in each client runs 1000 times.

Raw data is presented here, super raw data is at the very bottom.

###RAW DATA
##N=1,K=1
#1 client:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    95.11           106.43          100.88          97.94
Latency (sec/op)        0.0105          0.0093          0.0099          0.0102

#2 clients:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    209             208             198             200
Latency (sec/op)        0.0047          0.0047          0.005           0.005

#3 clients:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    269             304             288             286
Latency (sec/op)        0.0037          0.0032          0.0034          0.0034

#4 clients:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    353             396             362             379
Latency (sec/op)        0.0028          0.0025          0.0027          0.0026

#5 clients:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    414             401             460             498
Latency (sec/op)        0.0024          0.0024          0.0021          0.0020

##N=3,K=2
#1 client:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    50              137             49              56
Latency (sec/op)        0.020           0.0072          0.0204          0.0178

#2 clients:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    110             322             107             108
Latency (sec/op)        0.0090          0.0031          0.0093          0.0092

#3 clients:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    149             310             105             144
Latency (sec/op)        0.0067          0.0032          0.0095          0.0069

#4 clients:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    198             456             143             191
Latency (sec/op)        0.0050          0.0021          0.0069          0.0052

#5 clients:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    266             543             184             247
Latency (sec/op)        0.0037          0.0018          0.0054          0.0040

##N=5,K=3
#1 client:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    31              136             26              32
Latency (sec/op)        0.0313          0.0073          0.0376          0.0303

#2 clients:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    66              237             44              66
Latency (sec/op)        0.0151          0.0042          0.0227          0.0151

#3 clients:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    100             368             70              106
Latency (sec/op)        0.0100          0.0027          0.0142          0.0094

#4 clients:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    134             445             86              131
Latency (sec/op)        0.0074          0.0022          0.0116          0.0076

#5 clients:
                        Insertion       Lookup          Scan            Removal  
Throughput (ops/sec)    176             557             115             175
Latency (sec/op)        0.0056          0.0017          0.0086          0.0057

###DISCUSSION
We can see that individual clients have roughly the same throughputs for all
 operations, as shown in the super raw data section. When there's only one
 server, the insert and removal requests are at 100 operations per second per
 client. When we increase the number of servers, these requests become much
 smaller, hitting ~30 operations per second per client at N=5. This is as 
expected as insert and removal requests are writes, and the clients take a 
long time to write sequentially to each replica server to maintain consistency. 
Also, for all server configurations, we can see that the growth in throughputs 
of all operations increases linearly as we increase the number of connected 
clients. Thus this implies that the servers spend most of the time waiting for
requests by clients, and by increasing the number of requests by increasing the
number of clients, we reduce such waiting time at the servers and increase the
system's throughputs. Another important observation to note is the throughput
of the lookup operation. While the lookup operation with only 1 server is ~400
requests per second, the throughput of lookup is ~550 ops/second when running
on 3 or 5 servers. This suggests that when we increase the number of servers,
lookup requests are served faster. The scan request usually has the lowest 
throughput as it has to ask all servers to be sure that it doesn't miss out
any keys. The insert and removal operations have roughly the same throughputs
across all server configuration, something that is expected as there's no 
significant difference between insert and remove in terms of server workload.

###SUPER RAW DATA
##N=1,K=1
#1 client
Throughput of 1000 insertions: 95.11611216374787 ops/sec.
Latency of 1000 insertions: 0.010513465881347656 sec/op.
Throughput of 1000 lookups: 106.43975241177434 ops/sec.
Latency of 1000 lookups: 0.009394986152648926 sec/op.
Throughput of 1000 scans: 100.88800021090174 ops/sec.
Latency of 1000 scans: 0.009911981582641602 sec/op.
Throughput of 1000 removals: 97.94326119574497 ops/sec.
Latency of 1000 removals: 0.0102099928855896 sec/op.
#2 clients
Client 1:
Throughput of 1000 insertions: 105.63638044665738 ops/sec.
Latency of 1000 insertions: 0.00946643567085266 sec/op.
Throughput of 1000 lookups: 110.2289115628738 ops/sec.
Latency of 1000 lookups: 0.009072030067443847 sec/op.
Throughput of 1000 scans: 98.05889718996288 ops/sec.
Latency of 1000 scans: 0.01019795274734497 sec/op.
Throughput of 1000 removals: 100.02017666613513 ops/sec.
Latency of 1000 removals: 0.009997982740402221 sec/op.
Client 2:
Throughput of 1000 insertions: 104.72915754296038 ops/sec.
Latency of 1000 insertions: 0.009548439264297486 sec/op.
Throughput of 1000 lookups: 98.13813122414818 ops/sec.
Latency of 1000 lookups: 0.010189719200134277 sec/op.
Throughput of 1000 scans: 99.90682946123181 ops/sec.
Latency of 1000 scans: 0.010009325742721557 sec/op.
Throughput of 1000 removals: 100.29161607316577 ops/sec.
Latency of 1000 removals: 0.00997092318534851 sec/op.
#3 clients
Client 1:
Throughput of 1000 insertions: 92.62260741169183 ops/sec.
Latency of 1000 insertions: 0.010796500205993651 sec/op.
Throughput of 1000 lookups: 102.45910409452014 ops/sec.
Latency of 1000 lookups: 0.009759991645812989 sec/op.
Throughput of 1000 scans: 97.98176858243505 ops/sec.
Latency of 1000 scans: 0.01020598030090332 sec/op.
Throughput of 1000 removals: 97.83782416985468 ops/sec.
Latency of 1000 removals: 0.010220995903015137 sec/op.
Client 2:
Throughput of 1000 insertions: 94.40690650135086 ops/sec.
Latency of 1000 insertions: 0.010592445373535157 sec/op.
Throughput of 1000 lookups: 97.45658831630386 ops/sec.
Latency of 1000 lookups: 0.010260978937149048 sec/op.
Throughput of 1000 scans: 95.9141630002282 ops/sec.
Latency of 1000 scans: 0.010425988912582397 sec/op.
Throughput of 1000 removals: 97.76133674859432 ops/sec.
Latency of 1000 removals: 0.010228992700576782 sec/op.
Client 3:
Throughput of 1000 insertions: 83.63666876281579 ops/sec.
Latency of 1000 insertions: 0.011956478118896484 sec/op.
Throughput of 1000 lookups: 105.20790286357212 ops/sec.
Latency of 1000 lookups: 0.009504989385604859 sec/op.
Throughput of 1000 scans: 96.94637806938786 ops/sec.
Latency of 1000 scans: 0.010314980506896972 sec/op.
Throughput of 1000 removals: 92.73859669344313 ops/sec.
Latency of 1000 removals: 0.010782996892929077 sec/op.
#4 clients
Client 1: 
Throughput of 1000 insertions: 101.10695412354977 ops/sec.
Latency of 1000 insertions: 0.009890516519546508 sec/op.
Throughput of 1000 lookups: 99.84045014734207 ops/sec.
Latency of 1000 lookups: 0.010015980482101441 sec/op.
Throughput of 1000 scans: 103.6807022051465 ops/sec.
Latency of 1000 scans: 0.009644996404647827 sec/op.
Throughput of 1000 removals: 99.73089352594157 ops/sec.
Latency of 1000 removals: 0.010026983261108399 sec/op.
Client 2:
Throughput of 1000 insertions: 98.1983408867295 ops/sec.
Latency of 1000 insertions: 0.01018347144126892 sec/op.
Throughput of 1000 lookups: 96.62785176352976 ops/sec.
Latency of 1000 lookups: 0.0103489830493927 sec/op.
Throughput of 1000 scans: 103.15581023077509 ops/sec.
Latency of 1000 scans: 0.00969407343864441 sec/op.
Throughput of 1000 removals: 95.91495260843578 ops/sec.
Latency of 1000 removals: 0.01042590308189392 sec/op.
Client 3:
Throughput of 1000 insertions: 89.96479036752415 ops/sec.
Latency of 1000 insertions: 0.01111545968055725 sec/op.
Throughput of 1000 lookups: 98.26091489181013 ops/sec.
Latency of 1000 lookups: 0.010176986455917358 sec/op.
Throughput of 1000 scans: 99.56210565854894 ops/sec.
Latency of 1000 scans: 0.010043982028961182 sec/op.
Throughput of 1000 removals: 89.48998396103248 ops/sec.
Latency of 1000 removals: 0.011174434900283813 sec/op.
Client 4:
Throughput of 1000 insertions: 65.887087582067 ops/sec.
Latency of 1000 insertions: 0.015177480697631836 sec/op.
Throughput of 1000 lookups: 103.55616565484516 ops/sec.
Latency of 1000 lookups: 0.009656595468521118 sec/op.
Throughput of 1000 scans: 57.354637044756295 ops/sec.
Latency of 1000 scans: 0.017435381889343262 sec/op.
Throughput of 1000 removals: 96.54392949461766 ops/sec.
Latency of 1000 removals: 0.01035797905921936 sec/op.
#5 clients
Client 1:
Throughput of 1000 insertions: 109.87329389148763 ops/sec.
Latency of 1000 insertions: 0.00910139274597168 sec/op.
Throughput of 1000 lookups: 103.5734216279263 ops/sec.
Latency of 1000 lookups: 0.009654986619949341 sec/op.
Throughput of 1000 scans: 114.8767290036363 ops/sec.
Latency of 1000 scans: 0.008704983234405517 sec/op.
Throughput of 1000 removals: 111.71442769296357 ops/sec.
Latency of 1000 removals: 0.008951395273208618 sec/op.
Client 2:
Throughput of 1000 insertions: 100.29621106513193 ops/sec.
Latency of 1000 insertions: 0.009970466375350952 sec/op.
Throughput of 1000 lookups: 98.30864892384325 ops/sec.
Latency of 1000 lookups: 0.010172044992446899 sec/op.
Throughput of 1000 scans: 92.26866414799244 ops/sec.
Latency of 1000 scans: 0.010837915658950805 sec/op.
Throughput of 1000 removals: 91.16966660295687 ops/sec.
Latency of 1000 removals: 0.010968560457229614 sec/op.
Client 3:
Throughput of 1000 insertions: 83.46195306236206 ops/sec.
Latency of 1000 insertions: 0.011981507301330567 sec/op.
Throughput of 1000 lookups: 98.88276468430523 ops/sec.
Latency of 1000 lookups: 0.010112985849380493 sec/op.
Throughput of 1000 scans: 78.1837147967875 ops/sec.
Latency of 1000 scans: 0.012790387392044068 sec/op.
Throughput of 1000 removals: 101.08502596303863 ops/sec.
Latency of 1000 removals: 0.009892662048339844 sec/op.
Client 4:
Throughput of 1000 insertions: 71.45139513387895 ops/sec.
Latency of 1000 insertions: 0.013995527982711793 sec/op.
Throughput of 1000 lookups: 56.72182385339275 ops/sec.
Latency of 1000 lookups: 0.01762989854812622 sec/op.
Throughput of 1000 scans: 82.56974649578449 ops/sec.
Latency of 1000 scans: 0.012110973358154297 sec/op.
Throughput of 1000 removals: 98.61944198984844 ops/sec.
Latency of 1000 removals: 0.0101399884223938 sec/op.
Client 5:
Throughput of 1000 insertions: 51.98188251619932 ops/sec.
Latency of 1000 insertions: 0.01923747181892395 sec/op.
Throughput of 1000 lookups: 46.39726822419584 ops/sec.
Latency of 1000 lookups: 0.021552993059158324 sec/op.
Throughput of 1000 scans: 94.15327423686884 ops/sec.
Latency of 1000 scans: 0.01062097954750061 sec/op.
Throughput of 1000 removals: 97.84744002268852 ops/sec.
Latency of 1000 removals: 0.010219991445541381 sec/op.
##N=3,K=2
#1 client
Throughput of 1000 insertions: 50.62128354587662 ops/sec.
Latency of 1000 insertions: 0.019754536628723146 sec/op.
Throughput of 1000 lookups: 137.43846764790752 ops/sec.
Latency of 1000 lookups: 0.007275983333587647 sec/op.
Throughput of 1000 scans: 49.07740464544227 ops/sec.
Latency of 1000 scans: 0.020375975608825682 sec/op.
Throughput of 1000 removals: 56.69577352423582 ops/sec.
Latency of 1000 removals: 0.017637999057769777 sec/op.
#2 clients
Client 1:
Throughput of 1000 insertions: 55.553979388556876 ops/sec.
Latency of 1000 insertions: 0.018000510692596436 sec/op.
Throughput of 1000 lookups: 159.4641601761841 ops/sec.
Latency of 1000 lookups: 0.00627100157737732 sec/op.
Throughput of 1000 scans: 54.58822417178265 ops/sec.
Latency of 1000 scans: 0.018318969249725342 sec/op.
Throughput of 1000 removals: 54.740553087224995 ops/sec.
Latency of 1000 removals: 0.0182679922580719 sec/op.
Client 2:
Throughput of 1000 insertions: 55.04939623037928 ops/sec.
Latency of 1000 insertions: 0.01816550350189209 sec/op.
Throughput of 1000 lookups: 163.1880636855761 ops/sec.
Latency of 1000 lookups: 0.006127899169921875 sec/op.
Throughput of 1000 scans: 53.818439191047126 ops/sec.
Latency of 1000 scans: 0.018580992221832276 sec/op.
Throughput of 1000 removals: 54.478145956013655 ops/sec.
Latency of 1000 removals: 0.018355984449386596 sec/op.
#3 clients
Client 1:
Throughput of 1000 insertions: 52.07380958544294 ops/sec.
Latency of 1000 insertions: 0.019203511476516725 sec/op.
Throughput of 1000 lookups: 106.91781814852204 ops/sec.
Latency of 1000 lookups: 0.009352977991104126 sec/op.
Throughput of 1000 scans: 38.226338936783286 ops/sec.
Latency of 1000 scans: 0.02615997314453125 sec/op.
Throughput of 1000 removals: 50.71767012800761 ops/sec.
Latency of 1000 removals: 0.019716994047164916 sec/op.
Client 2:
Throughput of 1000 insertions: 50.455199463312994 ops/sec.
Latency of 1000 insertions: 0.019819562911987304 sec/op.
Throughput of 1000 lookups: 97.73306481446184 ops/sec.
Latency of 1000 lookups: 0.010231951713562011 sec/op.
Throughput of 1000 scans: 34.475638151319785 ops/sec.
Latency of 1000 scans: 0.029005989551544188 sec/op.
Throughput of 1000 removals: 47.74180444521158 ops/sec.
Latency of 1000 removals: 0.020946003437042237 sec/op.
Client 3:
Throughput of 1000 insertions: 47.93965244396613 ops/sec.
Latency of 1000 insertions: 0.02085955882072449 sec/op.
Throughput of 1000 lookups: 107.67789678052817 ops/sec.
Latency of 1000 lookups: 0.009286957025527955 sec/op.
Throughput of 1000 scans: 33.81465225061881 ops/sec.
Latency of 1000 scans: 0.02957297897338867 sec/op.
Throughput of 1000 removals: 47.86979883655831 ops/sec.
Latency of 1000 removals: 0.02088999795913696 sec/op.
#4 clients
Client 1:
Throughput of 1000 insertions: 50.65469772689691 ops/sec.
Latency of 1000 insertions: 0.01974150562286377 sec/op.
Throughput of 1000 lookups: 121.84721397103361 ops/sec.
Latency of 1000 lookups: 0.0082069993019104 sec/op.
Throughput of 1000 scans: 38.105388412760504 ops/sec.
Latency of 1000 scans: 0.02624300765991211 sec/op.
Throughput of 1000 removals: 49.43655546145532 ops/sec.
Latency of 1000 removals: 0.020227946519851686 sec/op.
Client 2:
Throughput of 1000 insertions: 50.829514761044 ops/sec.
Latency of 1000 insertions: 0.019673609018325804 sec/op.
Throughput of 1000 lookups: 121.3877252159367 ops/sec.
Latency of 1000 lookups: 0.008238065242767333 sec/op.
Throughput of 1000 scans: 37.833291969887604 ops/sec.
Latency of 1000 scans: 0.02643174695968628 sec/op.
Throughput of 1000 removals: 49.54626517932487 ops/sec.
Latency of 1000 removals: 0.02018315601348877 sec/op.
Client 3:
Throughput of 1000 insertions: 50.66488799172394 ops/sec.
Latency of 1000 insertions: 0.01973753499984741 sec/op.
Throughput of 1000 lookups: 108.18696179017512 ops/sec.
Latency of 1000 lookups: 0.009243257999420166 sec/op.
Throughput of 1000 scans: 35.99492135941471 ops/sec.
Latency of 1000 scans: 0.027781697034835816 sec/op.
Throughput of 1000 removals: 48.480142677098364 ops/sec.
Latency of 1000 removals: 0.020627002000808716 sec/op.
Client 4:
Throughput of 1000 insertions: 48.16833541850512 ops/sec.
Latency of 1000 insertions: 0.020760526418685914 sec/op.
Throughput of 1000 lookups: 106.7009930308492 ops/sec.
Latency of 1000 lookups: 0.009371984004974365 sec/op.
Throughput of 1000 scans: 33.55661103209398 ops/sec.
Latency of 1000 scans: 0.029800387144088746 sec/op.
Throughput of 1000 removals: 45.198617307046256 ops/sec.
Latency of 1000 removals: 0.02212457060813904 sec/op.
#5 clients
Client 1:
Throughput of 1000 insertions: 54.98611773260818 ops/sec.
Latency of 1000 insertions: 0.018186408519744873 sec/op.
Throughput of 1000 lookups: 119.93484984352982 ops/sec.
Latency of 1000 lookups: 0.008337860107421874 sec/op.
Throughput of 1000 scans: 39.21416030832175 ops/sec.
Latency of 1000 scans: 0.02550099229812622 sec/op.
Throughput of 1000 removals: 51.247907284421885 ops/sec.
Latency of 1000 removals: 0.019512991905212402 sec/op.
Client 2:
Throughput of 1000 insertions: 53.64957117925733 ops/sec.
Latency of 1000 insertions: 0.018639477968215943 sec/op.
Throughput of 1000 lookups: 114.58112624482524 ops/sec.
Latency of 1000 lookups: 0.00872744083404541 sec/op.
Throughput of 1000 scans: 37.55390685698068 ops/sec.
Latency of 1000 scans: 0.026628387928009034 sec/op.
Throughput of 1000 removals: 50.10695039592254 ops/sec.
Latency of 1000 removals: 0.019957311153411865 sec/op.
Client 3:
Throughput of 1000 insertions: 53.99717355454932 ops/sec.
Latency of 1000 insertions: 0.018519487857818602 sec/op.
Throughput of 1000 lookups: 105.17483622914708 ops/sec.
Latency of 1000 lookups: 0.009507977724075318 sec/op.
Throughput of 1000 scans: 37.64496085167445 ops/sec.
Latency of 1000 scans: 0.02656398034095764 sec/op.
Throughput of 1000 removals: 49.539318322480256 ops/sec.
Latency of 1000 removals: 0.020185986280441284 sec/op.
Client 4:
Throughput of 1000 insertions: 54.09980013804123 ops/sec.
Latency of 1000 insertions: 0.01848435664176941 sec/op.
Throughput of 1000 lookups: 102.87924750241567 ops/sec.
Latency of 1000 lookups: 0.009720133304595948 sec/op.
Throughput of 1000 scans: 37.39437245499433 ops/sec.
Latency of 1000 scans: 0.02674199175834656 sec/op.
Throughput of 1000 removals: 49.788455945633146 ops/sec.
Latency of 1000 removals: 0.02008497714996338 sec/op.
Client 5:
Throughput of 1000 insertions: 52.1957193627392 ops/sec.
Latency of 1000 insertions: 0.01915865921974182 sec/op.
Throughput of 1000 lookups: 103.7148567440371 ops/sec.
Latency of 1000 lookups: 0.009641820192337036 sec/op.
Throughput of 1000 scans: 34.946746443345205 ops/sec.
Latency of 1000 scans: 0.028614967107772827 sec/op.
Throughput of 1000 removals: 48.978810924570716 ops/sec.
Latency of 1000 removals: 0.0204169921875 sec/op.
##N=5,K=3
#1 client
Throughput of 1000 insertions: 31.911662018000495 ops/sec.
Latency of 1000 insertions: 0.03133650636672974 sec/op.
Throughput of 1000 lookups: 136.2420981087693 ops/sec.
Latency of 1000 lookups: 0.007339875221252442 sec/op.
Throughput of 1000 scans: 26.565074759843068 ops/sec.
Latency of 1000 scans: 0.037643409967422485 sec/op.
Throughput of 1000 removals: 32.97646743724952 ops/sec.
Latency of 1000 removals: 0.030324655055999756 sec/op.
#2 clients
Client 1:
Throughput of 1000 insertions: 35.35762952521357 ops/sec.
Latency of 1000 insertions: 0.02828243899345398 sec/op.
Throughput of 1000 lookups: 130.05638158765814 ops/sec.
Latency of 1000 lookups: 0.007688972949981689 sec/op.
Throughput of 1000 scans: 24.29662501993653 ops/sec.
Latency of 1000 scans: 0.04115797972679138 sec/op.
Throughput of 1000 removals: 35.6849791275444 ops/sec.
Latency of 1000 removals: 0.028022995233535766 sec/op.
Client 2:
Throughput of 1000 insertions: 31.157960121355394 ops/sec.
Latency of 1000 insertions: 0.03209452724456787 sec/op.
Throughput of 1000 lookups: 107.15872649270433 ops/sec.
Latency of 1000 lookups: 0.009331951141357422 sec/op.
Throughput of 1000 scans: 20.757646906324194 ops/sec.
Latency of 1000 scans: 0.04817501735687256 sec/op.
Throughput of 1000 removals: 31.340153853310944 ops/sec.
Latency of 1000 removals: 0.03190794801712036 sec/op.
#3 clients
Client 1:
Throughput of 1000 insertions: 36.84237298737322 ops/sec.
Latency of 1000 insertions: 0.02714265990257263 sec/op.
Throughput of 1000 lookups: 136.59671830141232 ops/sec.
Latency of 1000 lookups: 0.007320820093154907 sec/op.
Throughput of 1000 scans: 26.61912415111362 ops/sec.
Latency of 1000 scans: 0.03756697607040405 sec/op.
Throughput of 1000 removals: 38.33472847982725 ops/sec.
Latency of 1000 removals: 0.026086007118225098 sec/op.
Client 2:
Throughput of 1000 insertions: 32.027172467705526 ops/sec.
Latency of 1000 insertions: 0.03122348690032959 sec/op.
Throughput of 1000 lookups: 117.38493492870866 ops/sec.
Latency of 1000 lookups: 0.008518980741500854 sec/op.
Throughput of 1000 scans: 22.774903473635085 ops/sec.
Latency of 1000 scans: 0.043907979726791384 sec/op.
Throughput of 1000 removals: 34.81696622181407 ops/sec.
Latency of 1000 removals: 0.02872162938117981 sec/op.
Client 3:
Throughput of 1000 insertions: 32.41841826604811 ops/sec.
Latency of 1000 insertions: 0.030846662282943724 sec/op.
Throughput of 1000 lookups: 115.67344284466547 ops/sec.
Latency of 1000 lookups: 0.008645026683807374 sec/op.
Throughput of 1000 scans: 22.270317453321354 ops/sec.
Latency of 1000 scans: 0.04490281748771668 sec/op.
Throughput of 1000 removals: 34.59011654028637 ops/sec.
Latency of 1000 removals: 0.02890999221801758 sec/op.
#4 clients
Client 1:
Throughput of 1000 insertions: 34.18307237419031 ops/sec.
Latency of 1000 insertions: 0.02925424575805664 sec/op.
Throughput of 1000 lookups: 111.31775622281269 ops/sec.
Latency of 1000 lookups: 0.008983292818069458 sec/op.
Throughput of 1000 scans: 22.612673808515318 ops/sec.
Latency of 1000 scans: 0.04422298789024353 sec/op.
Throughput of 1000 removals: 33.72423324459266 ops/sec.
Latency of 1000 removals: 0.029652267932891847 sec/op.
Client 2:
Throughput of 1000 insertions: 34.08600931439564 ops/sec.
Latency of 1000 insertions: 0.029337549924850465 sec/op.
Throughput of 1000 lookups: 112.58001183963853 ops/sec.
Latency of 1000 lookups: 0.008882571458816529 sec/op.
Throughput of 1000 scans: 22.277979468702114 ops/sec.
Latency of 1000 scans: 0.04488737416267395 sec/op.
Throughput of 1000 removals: 33.95470170410538 ops/sec.
Latency of 1000 removals: 0.029451002359390258 sec/op.
Client 3:
Throughput of 1000 insertions: 33.52492202263879 ops/sec.
Latency of 1000 insertions: 0.029828555583953857 sec/op.
Throughput of 1000 lookups: 111.06210975016782 ops/sec.
Latency of 1000 lookups: 0.009003970861434937 sec/op.
Throughput of 1000 scans: 21.927429629867557 ops/sec.
Latency of 1000 scans: 0.04560498046875 sec/op.
Throughput of 1000 removals: 33.73472955607405 ops/sec.
Latency of 1000 removals: 0.029643041849136353 sec/op.
Client 4:
Throughput of 1000 insertions: 33.0471818174505 ops/sec.
Latency of 1000 insertions: 0.030259766340255737 sec/op.
Throughput of 1000 lookups: 111.0055743572948 ops/sec.
Latency of 1000 lookups: 0.009008556604385376 sec/op.
Throughput of 1000 scans: 21.449737939151873 ops/sec.
Latency of 1000 scans: 0.04662061619758606 sec/op.
Throughput of 1000 removals: 32.993842075715094 ops/sec.
Latency of 1000 removals: 0.03030868601799011 sec/op.
#5 clients
Client 1:
Throughput of 1000 insertions: 36.25220008284332 ops/sec.
Latency of 1000 insertions: 0.027584532737731933 sec/op.
Throughput of 1000 lookups: 116.0100170735892 ops/sec.
Latency of 1000 lookups: 0.008619945287704468 sec/op.
Throughput of 1000 scans: 23.278559958340946 ops/sec.
Latency of 1000 scans: 0.04295798373222351 sec/op.
Throughput of 1000 removals: 35.55415135030839 ops/sec.
Latency of 1000 removals: 0.028126110792160035 sec/op.
Client 2:
Throughput of 1000 insertions: 35.76485817268566 ops/sec.
Latency of 1000 insertions: 0.02796040725708008 sec/op.
Throughput of 1000 lookups: 110.98753594991962 ops/sec.
Latency of 1000 lookups: 0.00901002073287964 sec/op.
Throughput of 1000 scans: 23.172854896260233 ops/sec.
Latency of 1000 scans: 0.04315394043922424 sec/op.
Throughput of 1000 removals: 35.67088460605278 ops/sec.
Latency of 1000 removals: 0.028034067869186403 sec/op.
Client 3:
Throughput of 1000 insertions: 35.25669548957405 ops/sec.
Latency of 1000 insertions: 0.028363406896591187 sec/op.
Throughput of 1000 lookups: 112.74785256983033 ops/sec.
Latency of 1000 lookups: 0.008869348526000976 sec/op.
Throughput of 1000 scans: 23.24497669871069 ops/sec.
Latency of 1000 scans: 0.043020047426223756 sec/op.
Throughput of 1000 removals: 35.41362672131081 ops/sec.
Latency of 1000 removals: 0.028237717866897584 sec/op.
Client 4:
Throughput of 1000 insertions: 35.12944110027954 ops/sec.
Latency of 1000 insertions: 0.028466151714324952 sec/op.
Throughput of 1000 lookups: 110.0838182636867 ops/sec.
Latency of 1000 lookups: 0.00908398723602295 sec/op.
Throughput of 1000 scans: 23.127281306614552 ops/sec.
Latency of 1000 scans: 0.04323897767066955 sec/op.
Throughput of 1000 removals: 35.46591096548725 ops/sec.
Latency of 1000 removals: 0.028196089506149293 sec/op.
Client 5:
Throughput of 1000 insertions: 35.51210316566438 ops/sec.
Latency of 1000 insertions: 0.0281594135761261 sec/op.
Throughput of 1000 lookups: 109.51977752750727 ops/sec.
Latency of 1000 lookups: 0.009130770921707153 sec/op.
Throughput of 1000 scans: 23.21629355711244 ops/sec.
Latency of 1000 scans: 0.043073197603225706 sec/op.
Throughput of 1000 removals: 35.06927720368053 ops/sec.
Latency of 1000 removals: 0.028514987468719482 sec/op.
