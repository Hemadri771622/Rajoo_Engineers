import opcua
from opcua import Client
import time

# url = "opc.tcp://172.17.1.32:4840"
url = "opc.tcp://101.101.101.201:4840" #Enter Rajoo IP address
client = Client(url)

client.connect()
print("Client connected {}".format(url))

while True:
    # Note: AS4.8 have ns = 6 and AS4.12 have ns = 11
    Tag1 = client.get_node("ns=6;s =::AsGlobalPV:gVisuPara.MaxNoExt")
    # ns = 6;s =::AsGlobalPV: gVisuPara.MaxNoExt
    #ns=6;s=::AsGlobalPV:gVisuPara.TotalExtOuput
    Tag1Var1 = Tag1.get_value()
    pass
    print("MaxNoExt {}".format(Tag1Var1))
    print("Rajoo OPC variable1 {}")
    #
    Tag2 = client.get_node("ns=6;s=::AsGlobalPV:gVisuPara.TotalExtOuput")
    Tag2Var2 = Tag2.get_value()
    pass
    print("TotalExtOuput {}".format(Tag2Var2))
    print("Rajoo OPC variable2 {}")
    #
    # Tag3 = client.get_node("ns=11;s=::AsGlobalPV:INJ[0].Cal.Actpos")
    # Tag3Var3 = Tag3.get_value()
    # pass
    # print("Injection Position {}".format(Tag3Var3))
    #
    # Tag4 = client.get_node("ns=11;s=::AsGlobalPV:HEAT[0].Zone[0].Set.Temp")
    # Tag4Var4 = Tag4.get_value()
    # pass
    # print("Zone 1 Temperature {}".format(Tag4Var4))
    #
    # Tag5 = client.get_node("ns=11;s=::AsGlobalPV:HEAT[0].Zone[1].Set.Temp")
    # Tag5Var5 = Tag5.get_value()
    # pass
    # print("Zone 2 Temperature {}".format(Tag5Var5))
    #
    # Tag6 = client.get_node("ns=11;s=::AsGlobalPV:HEAT[0].Zone[2].Set.Temp")
    # Tag6Var6 = Tag6.get_value()
    # pass
    # print("Zone 3 Temperature {}".format(Tag6Var6))
    #
    # Tag7 = client.get_node("ns=11;s=::AsGlobalPV:HEAT[0].Zone[3].Set.Temp")
    # Tag7Var7 = Tag7.get_value()
    # pass
    # print("Zone 4 Temperature {}".format(Tag7Var7))

    # data['CLP Position'] = str(Tag1Var1)
    # data['EJT Position'] = str(Tag2Var2)
    # data['INJ Position'] = str(Tag3Var3)
    # data['Zone 1 Temp'] = str(Tag4Var4)
    # data['Zone 2 Temp'] = str(Tag5Var5)
    # data['Zone 3 Temp'] = str(Tag6Var6)
    # data['Zone 4 Temp'] = str(Tag7Var7)
    #
    # data_out = json.dumps(data)
    # iot_hub_client.publish(topic, data_out, 0)

    time.sleep(1)

