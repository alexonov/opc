from opcua import Server
import time
import random


def main():
    # create Server object
    server = Server()

    # define ip address for the server. format: 'opc.tcp://[ip_address]'
    url = 'opc.tcp://0.0.0.0:4840/freeopcua/server/'
    server.set_endpoint(url)

    # define address space
    name = 'OPCUA_SIMULATION_SERVER'
    addspace = server.register_namespace(name)

    # get root node
    root_node = server.get_objects_node()

    # define node where we wish to run parameters
    # assign to address space and name it 'Parameters'
    obj = root_node.add_object(addspace, 'Parameters')

    # We will use three parameters: temperature, pressure, time
    temp_param = obj.add_variable(addspace, 'Temperature', 0)
    pres_param = obj.add_variable(addspace, 'Pressure', 0)
    time_param = obj.add_variable(addspace, 'Time', 0)

    # make variables writable
    temp_param.set_writable()
    pres_param.set_writable()
    time_param.set_writable()

    server.start()

    print(f'server started at {url}')

    try:
        count = 0
        while True:
            time.sleep(1)
            count += 0.1
            temp_param.set_value(random.random())
            pres_param.set_value(random.randint(1, 100))
            time_param.set_value(count)
    finally:
        # close connection, remove subcsriptions, etc
        server.stop()


if __name__ == '__main__':
    main()
