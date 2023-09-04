import os
from subprocess import check_output as cop

#Vendor ID: i[23:27]
#Name: i[33:]

class Udev(object):
    def __init__(self, perm_lvl, distro):
        self.perm_lvl = perm_lvl
        self.usb_devices = []
        self.idVendor = "idVendor" #will make sense later
        self.search()
        self.select()
        if distro == 1:
            self.save_nix()
        elif distro == 2:
            self.save_classic()

    def search(self):
        query = input("\nEnter manufactor name (type CC for CharaChorder)\nLeave blank to display all devices: ")
        if query == 'CC' or query == 'cc':
            query = "CharaChorder"
        output = str(cop(f"lsusb | grep '{query}'", shell=True)).replace("b'", "").replace("\\n", "\n")
        self.usb_devices = output.split("\n")

    def select(self):
        print("\nPlease select the correct device, from the list below:")
        for ind, i in enumerate(self.usb_devices):
            print(f'{ind}: {i[33:]}')
        self.device = self.usb_devices[int(input("\nSelect device: "))]

    def save_classic(self):
        save_path = f'/etc/udev/rules.d/60-{self.device[33:].replace(" ", "_")}.rule'
        udev_rule = f'SUBSYSTEM=="usb", ATTR{self.idVendor}=="[{self.device[23:27]}]", MODE="{self.perm_lvl}", GROUP="plugdev"'

        print(f'\nshould the following be written to {save_path} (y/n)? \n "{udev_rule}"')
        temp = input(": ")
        if temp == 'y' or temp == 'Y':
            try:
                os.system(f'echo {udev_rule} > {save_path}')
            except:
                print("an error occured whilst saving (are you sudo?)")
        elif temp == 'n' or temp == 'N':
            print("Okay, no changes made")

    def save_nix(self):
        os.system(f"echo ")


def main():
    os.system("clear")
    print("////////////////////////////////////////////////////////////")
    print("///////////////Udev Rule maker, by Lynet_101////////////////")
    print("////////////////////////////////////////////////////////////")
    
    print("\nAre you using NixOS, or another gnu/linux distro?")
    distro = int(input("1) I'm using NixOS | 2) I'm using a different Linux distro | 3) I'm not using Linux\n: "))

    if distro == 3:
        print("Only linux users!")
        return

    print("\nWhat permission level would you like to use?")
    perm_lvl = int(input("1) Read & Write permision for members of udev group (recommended)\n2) Read & Write permission for All (Not recommended)\n: "))
    if perm_lvl == 1:
        perm_lvl = "0664"
    elif perm_lvl == 2:
        perm_lvl = "0666"
    Udev(perm_lvl, distro)

if __name__ == "__main__":
    main()