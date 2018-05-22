import sys
import time
sys.path.insert(0, "..")


from opcua import Client


def main():
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    try:
        client.connect()

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        print("Objects node is: ", root)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())

        # get a specific node knowing its node id
        #var = client.get_node(ua.NodeId(1002, 2))
        #var = client.get_node("ns=3;i=2002")
        #print(var)
        #var.get_data_value() # get value of node as a DataValue object
        #var.get_value() # get value of node as a python builtin
        #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #var.set_value(3.9) # set node value using implicit data type

        # Now getting a variable node using its browse path
        obj = root.get_child(["0:Objects", "2:Parameters"])

        # parameters
        temp_param = root.get_child(["0:Objects", "2:Parameters", "2:Temperature"])
        pres_param = root.get_child(["0:Objects", "2:Parameters", "2:Pressure"])
        time_param = root.get_child(["0:Objects", "2:Parameters", "2:Time"])

        print("Node is: ", obj)

        while True:
            print("Temperature is: ", temp_param.get_value())
            print("Pressure is: ", pres_param.get_value())
            print("Time is: ", time_param.get_value())
            time.sleep(1)

        # Stacked myvar access
        # print("myvar is: ", root.get_children()[0].get_children()[1].get_variables()[0].get_value())

    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
