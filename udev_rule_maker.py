import os
from subprocess import check_output as cop
from sys import argv as user_arguments

#Vendor ID: i[23:27]
#Name: i[33:]

#perm_lvl 1 = 0664
#perm_lvl 2 = 0666

class Program():
    def __init__(self):
        self.main()
        self.scan()
        self.select()
        self.save_classic()
    
    def main(self):
        try:
            self.manufactor = user_arguments[1]
        except:
            self.manufactor = "" 
        try:
            self.permission_lvl = str(user_arguments[2])
        except:
            self.permission_lvl = "0664"

    def scan(self):
        try:
            output = str(cop(f"lsusb | grep '{self.manufactor}'", shell=True)).replace("b'", "").replace("\\n", "\n")
        except:
            print(f"no devices found with manufactor {self.manufactor}")
            exit()
        self.usb_devices = output.split("\n")
    
    def select(self):
        for ind, device in enumerate(self.usb_devices):
            print(f'{ind}: {device[33:]}')
        
        user_select = int(input(f"Select device: "))
        selected_device = self.usb_devices[user_select]
        self.device_id = selected_device[23:27]

    def save_classic(self):
        self.idVendor = "idVendor"
        os.system(f'echo SUBSYSTEM=="usb", ATTR{self.idVendor}=="[{self.device_id}]", MODE="{self.permission_lvl}", GROUP="plugdev" >> /etc/udev/rules.d/60-usb_rules-lynet101.rules')
        print(f"Device {self.device_id} with permission {self.permission_lvl} saved")

def help():
    print("////////////////////////////////////////////////////////////")
    print("///////////////Udev Creator, by Lynet_101////////////////")
    print("////////////////////////////////////////////////////////////")

    print("Usage: udev_creator [manufactor] [permission_lvl]")
    print("Example: udev_creator CharaChorder 0666")
    print("If manufactor is not given, all devices will be scanned")
    print("If permission_lvl is not given, 0664 will be used")

if __name__ == "__main__":
    try:
        if user_arguments[1] == "help":
            help()
        else:
            Program()
    except:
        Program()
        