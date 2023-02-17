import bluetooth
import device
import threading

thread_run = True
device_list = []


def print_dev(d: device.Device):
    print("")
    print("Device:")
    print("\tDevice Name: %s" % d.d_name)
    print("\tDevice MAC Address: %s" % d.d_mac)
    print("\tDevice Class: %s" % d.d_class)


def scan():
    print("Scanning for bluetooth devices:")
    first_run = True
    while thread_run:
        devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
        number_of_devices = len(devices)
        temp_device_list = []
        if first_run:
            print("")
            print(number_of_devices, "devices found")
        for addr, name, device_class in devices:
            count = 0
            found = False
            for d in device_list:
                if d.d_mac == addr:
                    found = True
            if not found:
                count += 1
                device_list.append(device.Device(name, addr, device_class))
                temp_device_list.append(device_list[len(device_list) - 1])
                print_dev(device_list[len(device_list) - 1])
        if not first_run and len(temp_device_list) > 0:
            print("")
            print(len(temp_device_list), "new devices found")
            for d in temp_device_list:
                print_dev(d)
        first_run = False
    if not thread_run:
        return


def bt_listen():
    print("Listening for Bluetooth Connections...")
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    port = 9876
    server_sock.bind(("", port))
    server_sock.listen(1)

    client_sock, address = server_sock.accept()
    print("Accepted connection from ", address)

    data = client_sock.recv(1024)
    print("received [%s]" % data)

    client_sock.close()
    server_sock.close()


thread_list = []
bt_thread = threading.Thread(target=lambda: scan())
thread_list.append(bt_thread)
listen_thread = threading.Thread(target=bt_listen)
thread_list.append(listen_thread)
for thread in thread_list:
    thread.start()


