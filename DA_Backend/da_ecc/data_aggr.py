from turtle import color
from .ECC import encrypt_ECC, decrypt_ECC
from collections import namedtuple
from operator import ge
from webbrowser import get
from matplotlib import colors, markers, pyplot as plt
import numpy as np
from .utils import get_graph
import base64
from io import BytesIO
import sys


def data_agg(data):

    # imports
    import numpy as np
    from matplotlib import pyplot as plt
    from collections import namedtuple
    from tinyec import registry
    import secrets

    # Field Dimensions - x and y maximum (in meters)
    xm = 100
    ym = 100

    charts = []
    final_data = {}

    # x and y Coordinates of the Sink
    mdef = namedtuple('sink', 'x y')
    sink = mdef(0.5*xm, 0.5*ym)

    # Number of Nodes in the field
    # n = 10
    n = int(data['node'])

    # Optimal Election Probability of a node to become cluster head
    p = 0.02

    # Energy Model (all values in Joules)
    # Initial Energy
    # Eo = 0.5
    Eo = float(data['energy'])
    # Eelec=Etx=Erx
    ETX = 50*0.000000001
    ERX = 50*0.000000001
    # Transmit Amplifier types
    Efs = 10*0.000000000001
    Emp = 0.0013*0.000000000001
    # Data Aggregation Energy
    EDA = 5*0.000000001

    # Values for Hetereogeneity
    # Percentage of nodes than are advanced
    m = 0.1
    # %\alpha
    a = 1

    # maximum number of rounds
    rmax = 1

    ################ END OF PARAMETERS ######################

    # Computation of do

    do = np.sqrt(Efs/Emp)

    # generating public and private keys
    curve = registry.get_curve('brainpoolP256r1')
    plt.figure(1)
    privKey = secrets.randbelow(curve.field.n)
    pubKey = privKey * curve.g

    # sample data for each data

    # DATA = b"hi"
    # befor encryption convert data to bytes form
    # DATA = bytes(data['data'], 'utf-8')
    data: list = data['data']
    # Creation of the random Sensor Network

    S = {x: dict({"xd": None, "yd": None, "type": None, "E": Eo,
                  "ENERGY": None, "G": None, "min_dis": None, "min_dis_cluster": None, "privKey": privKey, "pubKey": pubKey, "DATA": ""}) for x in range(0, n+1)}
    for (i, v) in enumerate(data):
        S[i]["DATA"] = v
    XR = {}
    YR = {}

    for i in range(0, n):
        print(i)
        S[i]["xd"] = np.random.rand(1, 1)[0][0]*xm
        XR[i] = S[i]["xd"]
        S[i]["yd"] = np.random.rand(1, 1)[0][0]*ym
        YR[i] = S[i]["yd"]
        S[i]["G"] = 0
        # initially there are no cluster heads only nodes
        S[i]["type"] = 'N'

        temp_rnd0 = i
        # Random Election of Normal Nodes
        if (temp_rnd0 >= m*n+1):
            S[i]["E"] = Eo
            S[i]["ENERGY"] = 0
            plt.plot(S[i]["xd"], S[i]["yd"], color="gray", marker='o')
            # plt.show()
        # end
        # Random Election of Advanced Nodes
        if (temp_rnd0 < m*n+1):
            S[i]["E"] = Eo*(1+a)
            S[i]["ENERGY"] = 1
            plt.plot(S[i]["xd"], S[i]["yd"], color="gray", marker='o')

    #     end
    # end

    S[n]["xd"] = sink.x
    S[n]["yd"] = sink.y
    plt.plot(S[n]["xd"], S[n]["yd"], 'k*', markersize=10)

    # First Iteration
    plt.figure(1)

    # counter for CHs
    countCHs = 0
    # counter for CHs per round
    rcountCHs = 0
    cluster = 1

    countCHs
    rcountCHs = rcountCHs+countCHs
    flag_first_dead = 0

    PACKETS_TO_CH = {}
    PACKETS_TO_BS = {}
    STATISTICS = {x: dict({"DEAD": None, "CLUSTERHEADS": None})
                  for x in range(0, rmax)}
    DEAD_N = {}
    DEAD = {}
    DEAD_A = {}
    CLUSTERHS = {}
    encryptionTime = []
    decryprionTime = []
    clr = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
           '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    for r in range(0, rmax, 1):
        print(r)

    #   Election Probability for Normal Nodes
        pnrm = (p / (1+a*m))
        # Election Probability for Advanced Nodes
        padv = (p/(1+a*m))

        # Operation for heterogeneous epoch
        if(np.mod(r, round(1/pnrm)) == 0):
            for i in range(0, n, 1):
                S[i]["G"] = 0
                S[i]["cl"] = 0
        #     end
        # end

        # Operations for sub-epochs
        if(np.mod(r, round(1/padv)) == 0):
            for i in range(0, n):
                if(S[i]["ENERGY"] == 1):
                    S[i]["G"] = 0
                    S[i]["cl"] = 0
        #         end
        #     end
        # end

        # Number of dead nodes
        dead = 0
        # Number of dead Advanced Nodes
        dead_a = 0
        # Number of dead Normal Nodes
        dead_n = 0

        # %counter for bit transmitted to Bases Station and to Cluster Heads
        packets_TO_BS = 0
        packets_TO_CH = 0
        # counter for bit transmitted to Bases Station and to Cluster Heads
        # per round
        PACKETS_TO_CH[r] = 0
        PACKETS_TO_BS[r] = 0
        base_station = []
        sink_node = []
        plt.figure(1)

        for i in range(0, n, 1):

            # checking if there is a dead node
            if (S[i]["E"] <= 0):
                # plt.plot(S[i]["xd"], S[i]["yd"], 'r.')
                dead = dead+1
                if(S[i]["ENERGY"] == 1):
                    dead_a = dead_a+1
                if(S[i]["ENERGY"] == 0):
                    dead_n = dead_n+1

            if S[i]["E"] > 0:
                S[i]["type"] = 'N'
                x = None
                y = None
                if (S[i]["ENERGY"] == 0):
                    # plt.plot(S[i]["xd"], S[i]["yd"], color=clr[
                    #          int(S[i]["xd"]+S[i]["yd"]) % 10], marker='o')
                    x = S[i]["xd"]
                if (S[i]["ENERGY"] == 1):
                    # plt.plot(S[i]["xd"], S[i]["yd"], '+')
                    y = S[i]["yd"]
                if x and y:
                    # print("x and y_____________", x, y)
                    plt.Line2D(x, y)

        # plt.plot(S[n+1]["xd"], S[n+1]["yd"], 'x')
        STATISTICS[r]["DEAD"] = dead
        DEAD[r] = dead
        DEAD_N[r] = dead_n
        DEAD_A[r] = dead_a

        # When the first node dies
        if (dead == 1):
            if(flag_first_dead == 0):
                first_dead = r
                flag_first_dead = 1

        if (dead >= 19 and dead <= 21):
            dead_20 = r

        if (dead >= 48 and dead <= 52):
            dead_50 = r

        countCHs = 0
        cluster = 0
        C = {x: dict({"xd": S[0]["xd"], "yd": S[0]["yd"], "distance": S[0]["min_dis"], "id": n-1, "E": S[0]["E"],
                      }) for x in range(0, n)}
        X = {}
        Y = {}
        clusetD = []
        for i in range(0, n, 1):

            if(S[i]["E"] > 0):
                temp_rand = np.random.rand()
                if ((S[i]["G"]) <= 0):
                    # Election of Cluster Heads for normal nodes
                    if((S[i]["ENERGY"] == 0 and (temp_rand <= (pnrm / (1 - pnrm * np.around(np.mod(r, round(1/pnrm)))))))):
                        countCHs = countCHs+1
                        packets_TO_BS = packets_TO_BS+1
                        PACKETS_TO_BS[r] = packets_TO_BS
                        # decrypting data at BS
                        # print("to decrypt", S[i]["DATA"])
                        # decryptedData = decrypt_ECC(S[i]["DATA"], S[i]["privKey"])
                        # d_data = decryptedData[0]
                        # decryprionTime.append(decryptedData[1])
                        # base_station.append(d_data)

                        S[i]["type"] = 'C'
                        S[i]["G"] = 100
                        C[cluster]["xd"] = S[i]["xd"]
                        C[cluster]["yd"] = S[i]["yd"]
                        plt.plot(S[i]["xd"], S[i]["yd"], 'k^')

                        distance = np.sqrt((S[i]["xd"]-(S[n]["xd"])) ** 2 +
                                           (S[i]["yd"]-(S[n]["yd"])) ** 2)
                        C[cluster]["distance"] = distance
                        C[cluster]["id"] = i
                        X[cluster] = S[i]["xd"]
                        Y[cluster] = S[i]["yd"]
                        cluster = cluster+1
                        clusetD.append((S[i]["xd"], S[i]["yd"]))
                        # print("cluser1", cluster,
                        #       S[i]["type"], S[i]["xd"], S[i]["yd"])
                        # Calculation of Energy dissipated
                        distance
                        if (distance > do):
                            S[i]["E"] = S[i]["E"] - ((ETX+EDA)*(4000) + Emp *
                                                     4000*(distance*distance*distance*distance))
                        # end
                        if (distance <= do):
                            S[i]["E"] = S[i]["E"] - ((ETX+EDA)*(4000) +
                                                     Efs*4000*(distance * distance))
                    #     end
                    # end

                    # Election of Cluster Heads for Advanced nodes
                    if((S[i]["ENERGY"] == 1 and (temp_rand <= (padv / (1 - padv * np.around(np.mod(r, round(1/padv)))))))):

                        countCHs = countCHs+1
                        packets_TO_BS = packets_TO_BS+1
                        PACKETS_TO_BS[r+1] = packets_TO_BS
                        # print("to decrypt", S[i]["DATA"])
                        # decrypting data at BS
                        # decryptedData = decrypt_ECC(S[i]["DATA"], S[i]["privKey"])
                        # d_data = decryptedData[0]
                        # decryprionTime.append(decryptedData[1])
                        # base_station.append(d_data)

                        S[i]["type"] = 'C'
                        S[i]["G"] = 100
                        C[cluster]["xd"] = S[i]["xd"]
                        C[cluster]["yd"] = S[i]["yd"]
                        plt.plot(S[i]["xd"], S[i]["yd"], 'k^')
                        clusetD.append((S[i]["xd"], S[i]["yd"]))
                        # print("cluser2", cluster,
                        #       S[i]["type"], S[i]["xd"], S[i]["yd"])
                        distance = np.sqrt(
                            (S[i]["xd"]-(S[n]["xd"])) ** 2 + (S[i]["yd"]-(S[n]["yd"])) ** 2)
                        C[cluster]["distance"] = distance
                        C[cluster]["id"] = i
                        X[cluster] = S[i]["xd"]
                        Y[cluster] = S[i]["yd"]
                        cluster = cluster+1

                        # Calculation of Energy dissipated
                        distance
                        if (distance > do):
                            S[i]["E"] = S[i]["E"] - ((ETX+EDA)*(4000) + Emp *
                                                     4000*(distance*distance*distance*distance))
                        # end
                        if (distance <= do):
                            S[i]["E"] = S[i]["E"] - \
                                ((ETX+EDA)*(4000) + Efs*4000*(distance * distance))

        #                 end
        #             end

        #         end
        #     end
        # end

        STATISTICS[r]["CLUSTERHEADS"] = cluster-1
        CLUSTERHS[r] = cluster-1

        # Election of Associated Cluster Head for Normal Nodes
        cl = []
        colorTracker = 0
        for i in range(0, n, 1):

            if (S[i]["type"] == 'N' and S[i]["E"] > 0):

                if(cluster >= 0):
                    min_dis = np.sqrt((S[i]["xd"]-S[n]["xd"]) **
                                      2 + (S[i]["yd"]-S[n]["yd"]) ** 2)
                    min_dis_cluster = 0
                    for c in range(0, cluster, 1):
                        temp = min(min_dis, np.sqrt(
                            (S[i]["xd"]-C[c]["xd"]) ** 2 + (S[i]["yd"]-C[c]["yd"]) ** 2))
                        if (temp < min_dis):
                            min_dis = temp
                            min_dis_cluster = c
                    #     end
                    # end

                    # Energy dissipated by associated Cluster Head
                    min_dis
                    if (min_dis > do):
                        S[i]["E"] = S[i]["E"] - (ETX*(4000) + Emp*4000 *
                                                 (min_dis * min_dis * min_dis * min_dis))
                    # end
                    if (min_dis <= do):
                        S[i]["E"] = S[i]["E"] - (ETX*(4000) + Efs *
                                                 4000*(min_dis * min_dis))
                    # end
                    # Energy dissipated
                    if(min_dis > 0):
                        # print("ccccc", C[min_dis_cluster]
                        #   ["id"], C[min_dis_cluster], min_dis_cluster, S[C[min_dis_cluster]["id"]]["E"])
                        S[C[min_dis_cluster]["id"]]["E"] = S[C[min_dis_cluster]
                                                             ["id"]]["E"] - ((ERX + EDA)*4000)
                        PACKETS_TO_CH[r] = n-dead-cluster+1
                        if (S[C[min_dis_cluster]["id"]]["xd"], S[C[min_dis_cluster]["id"]]["yd"]) in clusetD:
                            colorTracker = clusetD.index(
                                (S[C[min_dis_cluster]["id"]]["xd"], S[C[min_dis_cluster]["id"]]["yd"]))
                        S[C[min_dis_cluster]["id"]]["DATA"] = np.average(
                            [S[C[min_dis_cluster]["id"]]["DATA"], S[i]["DATA"]])
                        c_x = [S[i]["xd"], S[C[min_dis_cluster]["id"]]["xd"]]
                        c_y = [S[i]["yd"], S[C[min_dis_cluster]["id"]]["yd"]]
                        plt.plot(S[i]["xd"], S[i]["yd"],
                                 color=clr[int(colorTracker) % 10], marker='o')
                        # print("colorTracker", colorTracker)

                        plt.plot(c_x, c_y, color=clr[int(
                            colorTracker) % 10], alpha=0.2)
                        cl.append((S[C[min_dis_cluster]["id"]]["xd"],
                                  S[C[min_dis_cluster]["id"]]["yd"]))
                    # end

                    S[i]["min_dis"] = min_dis
                    S[i]["min_dis_cluster"] = min_dis_cluster
            colorTracker -= 1
        #         end
        #     end
        # end

        # Aggregating Cluster Head data to Sink node
        f_agg = [x["DATA"]
                 for x in S.values() if x["type"] == "C"]
        if len(f_agg) <= 0:
            f_agg = [x["DATA"]
                     for x in S.values()]
            f_agg.pop(-1)
        # print("f_agg", f_agg)
        S[n]["DATA"] = np.average(f_agg)

        for i in clusetD:
            s_x = [i[0], S[n]["xd"]]
            s_y = [i[1], S[n]["yd"]]
            plt.plot(s_x, s_y, 'k', alpha=0.5)
        # print(clusetD)

        countCHs
        # print("countCHs ", countCHs)
        # print("pkt to clusetr", cl)
        rcountCHs = rcountCHs+countCHs
    e_data = encrypt_ECC(bytes(str(S[n]["DATA"]), 'utf-8'), S[n]["pubKey"])
    sink_node.append(e_data[0])
    encryptionTime.append(e_data[1])

    # end
    print("+++++++++++++++++++ r=", r)
    # x = [i for i in range(1, r+1, 1)]
    # y = [i for i in range(1, r+1, 1)]

    # for i in range(0, r, 1):
    #     x[i] = i+1
    #     y[i] = n - STATISTICS[i+1]["DEAD"]
    # end
    d_data = decrypt_ECC(sink_node[0], privKey)
    base_station.append(d_data[0])
    decryprionTime.append(d_data[1])
    print("encrytion time", encryptionTime)
    print("decryption time", decryprionTime)
    plt.title('Sensor Network')
    plt.xlabel('Breadth in m')

    # legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label='Sensor Node',
                                  markerfacecolor='black', markersize=5)]
    legend_elements.extend([plt.Line2D([0], [0], marker='^', color='w', label='Cluser Head',
                                       markerfacecolor="Black", markersize=10)])
    legend_elements.extend([plt.Line2D([0], [0], marker='*', color='w', label='Sink Node',
                                       markerfacecolor="Black", markersize=10)])
    plt.legend(handles=legend_elements, loc='upper right', ncol=2)
    plt.ylabel('Length in m ')
    graph = get_graph()
    charts.append(graph)
    # plt.figure(2)

    # plt.plot(x, y, 'k')
    # plt.title('ALIVE NODES vs ROUNDS')
    # plt.xlabel('number of rounds')
    # plt.ylabel('number of alive nodes')
    # graph = get_graph()
    # charts.append(graph)
    # xb = np.array([x for x in range(1, 3500)])
    # dd = np.array(list(DEAD.values()))
    # plt.figure(3)
    # plt.plot(xb, dd, 'k')
    # plt.xlabel('number of rounds')
    # plt.ylabel('number of dead nodes')
    # plt.title('DEAD NODES vs ROUNDS')
    # graph = get_graph()
    # charts.append(graph)
    print(sink_node, base_station)
    final_data["sink"] = str(sink_node[0][0])
    final_data["base"] = base_station[0].decode('utf-8')
    final_data["charts"] = charts
    final_data["enc"] = encryptionTime
    final_data["dec"] = decryprionTime
    plt.close()
    del clusetD
    return final_data
