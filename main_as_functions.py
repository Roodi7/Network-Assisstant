import random
import sys
from tkinter import *
from tkinter.ttk import *
from tkhtmlview import HTMLLabel
import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
from pyvis.network import Network
from experta import *
import os
from prettytable import PrettyTable
from datetime import *

protocol = "eigrp"

#======= Making results folder =====
dt=datetime.now()
date='Project at '+str((datetime.today().strftime("%Y-%m-%d_%H-%M-%S")))
res_directory_path = 'D:/graduationf/program_results/'+date
try:
    os.mkdir(res_directory_path)
except OSError as error:
    print(error)

#======== router file open =====
router_file = open(res_directory_path+'/router_file.txt', "w")
router_file.write("enable\nconfigure terminal\n")

# ==========================
# == Expert System For Protocol
# ==========================


class protocol_engine(KnowledgeEngine):
    protocolo = "eigrp"

    @Rule(NOT(Fact(start=W())))
    def f0(self):
        ll = input("work on network protocol?")
        self.declare(Fact(start=ll))

    # ======================================

    @Rule(Fact(start='no'))
    def f1(self):
        ll = input(" ?")
        self.declare(Fact(ex_protocol=ll))
        protocolo = "eigrp"

    @Rule(Fact(start='yes'))
    def f1(self):
        self.declare(Fact(asd=input("Is your network small (less than 15 hop) ?")))

    @Rule(Fact(asd="yes"))
    def f2(self):
        ll = input("is the network expenable and need reliabilty ?")
        self.declare(Fact(reabilty=ll))

    @Rule(Fact(reabilty='no'))
    def f3(self):
        print("RIP V2")
        self.protocolo = "rip"

    @Rule(Fact(reabilty='yes'))
    def f4(self):
        print("protocol eigrp")
        self.protocolo = "eigrp"

    @Rule(Fact(asd="no"))
    def f5(self):
        ll = input("Does lower convergance time over resources consumption matter ?")
        self.declare(Fact(ex_protocol=ll))

    @Rule(Fact(ex_protocol='no'))
    def f6(self):
        print("protocol ospf")
        self.protocolo = "ospf"

    @Rule(Fact(ex_protocol='yes'))
    def f7(self):
        print("protocol eigrp")
        self.protocolo = "eigrp"


# =============== creating DB
db = sqlite3.connect(res_directory_path+"/network.db")
cr = db.cursor()

# ========Delete The previous tables
tables_from_db = cr.execute("SELECT name FROM sqlite_master WHERE type='table'")
list_of_tables_in_db = [item for t in tables_from_db for item in t]
for ff in list_of_tables_in_db:
    cr.execute('Drop table if exists ' + str(ff))
# ===========================

cr.execute("CREATE TABLE if not exists switches(id INT ,devices_in_switch INT,switch_ip VARCHAR(45),PRIMARY KEY('id'))")
cr.execute("CREATE TABLE if not exists departments2(id INT ,name VARCHAR(45),number_of_devices_in_department INT)")
cr.execute(f"CREATE TABLE if not exists each_switch(id INT ,switch_name VARCHAR(45),"
           f"number_of_devices_in_switch INT,departments_in_switch INT)")

cr.execute(
    "CREATE TABLE if not exists department_ip(department VARCHAR(45),device_ip VARCHAR(45),subnet_mask VARCHAR(45),default_gateway VARCHAR(45))")
# cr.execute("insert into department_ip(department,device_ip,subnet_mask,default_gate) values('internet','0.0.0.0')")


cr.execute("delete from switches")
cr.execute("delete  from departments2")
cr.execute("delete  from each_switch")

# =============== Drawing Network =======
g = Network(height="700px", width="1000px", directed=False, notebook=True, bgcolor="#ffffff", font_color=False, heading="",layout=True)
g.show_buttons(filter_=["physics"])

color_list = ['#4c5fb7', '#ffe227', '#81b114', '#a35fee', '#12ea4c', '#ac005d', '#ff9f68', '#a0e4f1', '#ff894c',
              '39065a', '#280f34', '#5c525c']
color_counter = 0
switch_node = 0
nodes_counter = 1

switch_node_list = []
# num_of_ent=int(input("Enter number of entries you want :"))
i=0

#==== num of devs in each dep list =====
number_of_devices_in_department = []
number_of_devices_in_department2 = []
number_of_devices_in_department3 =[]
number_of_devices_in_department4 = []
departmentslist_for_vlans=[]
dumm_list=[]
number_of_devices=0





#========================================
#========Starting The Gui Here ==========
#========================================

ro =Tk()
ro.title("Tab Widget")
ro.geometry("1250x650")
ro.state("zoomed")
tabControl = Notebook(ro)
root= Frame(tabControl)
routing_tab =Frame(tabControl)

tabControl.add(root, text='main')
tabControl.add(routing_tab, text='routing protocol')
tabControl.pack(expand=1, fill="both")
# style=Style(root)
# style.theme_use('default')
# style.layout("TFrame")
#==== main dep list =======
departmentslist = []


labels = []
dep_names_entries=[]
num_of_devices_entries=[]
path_c_list=[]
dhcp_li=[]


expens_or_cheap_list=[False]
prices_list={}


#======================


# =========== Functions ============



#=========== 24 price  =============
def switch_24_price(number_of_switches_24):
    # switches 24 port
    url_1 = "https://itprice.com/cisco/ws-c2960x-24ts-ll.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    page_1 = requests.get(url_1, headers=headers)

    # parse Pages
    soup_1 = BeautifulSoup(page_1.content, "html.parser")

    title1 = soup_1.find_all(class_="rs-price")
    string_price1 = title1[0].get_text()

    price_24_port_string = string_price1[3:7]
    # convert to integer
    price_24_port = int(price_24_port_string)
    total_24_switch_price = number_of_switches_24 * price_24_port
    return total_24_switch_price


# =========== 48 Price =============

def switch_48_price(number_of_switches_48):
    # Switches 48 port
    url_2 = "https://itprice.com/cisco/ws-c2960x-24ts-l++.html"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    page_2 = requests.get(url_2, headers=headers)

    # parse Pages
    soup_2 = BeautifulSoup(page_2.content, "html.parser")

    price_string = soup_2.find("td", text="Global Price in USD").find_next_sibling("td").text

    price_string = price_string[37:41]

    # convert to integer
    price = int(price_string)
    return (number_of_switches_48*price)


# =========== router Price =============


def router_price(router_count,expens_or_cheap):
    url_1="https://www.router-switch.com/cisco2911-hsec-k9-p-5625.html"
    url_2 = "https://www.router-switch.com/cisco2811-p-180.html"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    page_1= requests.get(url_1, headers=headers)

    page_2 = requests.get(url_2, headers=headers)

    # parse Pages
    soup_1 = BeautifulSoup(page_1.content, "html.parser")
    soup_2 = BeautifulSoup(page_2.content, "html.parser")
    expsv_router_string=soup_1.find_all(class_="listprice")
    cheap_router_string=soup_2.find_all(class_="listprice")
    exps_string = expsv_router_string[0].get_text()
    exps_string=(exps_string.split())[2]
    exps_string=exps_string[3:8]
    exps_string=exps_string.replace(",","")
    expsv_router=int(exps_string)

    cheap_string = cheap_router_string[0].get_text()
    cheap_string = (cheap_string.split())[2]
    cheap_string = cheap_string[3:8]
    cheap_string = cheap_string.replace(",", "")
    cheap_router = int(cheap_string)
    if(not expens_or_cheap):
        price=router_count*cheap_router
    else:
        price=router_count*expsv_router
    return price
# ========== Different Router ==========
# Show different routers and there prices ====


# ========== Subnetting ================
# returns a list Wich is :
# [0] ==> First ip in subnet
# [1] ==> last ip in subnet
# [2] ==> Network address
def subnet_calc(ip, mask):
    try:

        while True:
            # Take IP as input
            input_ip = ip

            # Validate the IP
            octet_ip = input_ip.split(".")
            # print octet_ip
            int_octet_ip = [int(i) for i in octet_ip]

            if (len(int_octet_ip) == 4) and \
                    (int_octet_ip[0] != 127) and \
                    (int_octet_ip[0] != 169) and \
                    (0 <= int_octet_ip[1] <= 255) and \
                    (0 <= int_octet_ip[2] <= 255) and \
                    (0 <= int_octet_ip[3] <= 255):
                break
            else:
                # print "Invalid IP, retry \n"
                print("Invalid IP, retry \n")
                break

        # Predefine possible subnet masks
        masks = [0, 128, 192, 224, 240, 248, 252, 254, 255]
        while True:

            # Take subnet mask as input
            input_subnet = mask

            # Validate the subnet mask
            octet_subnet = [int(j) for j in input_subnet.split(".")]
            # print octet_subnet
            if (len(octet_subnet) == 4) and \
                    (octet_subnet[0] == 255) and \
                    (octet_subnet[1] in masks) and \
                    (octet_subnet[2] in masks) and \
                    (octet_subnet[3] in masks) and \
                    (octet_subnet[0] >= octet_subnet[1] >= octet_subnet[2] >= octet_subnet[3]):
                break
            else:
                print("Invalid subnet mask, retry\n")
                continue

        # Converting IP and subnet to binary

        ip_in_binary = []

        # Convert each IP octet to binary
        ip_in_bin_octets = [bin(i).split("b")[1] for i in int_octet_ip]

        # make each binary octet of 8 bit length by padding zeros
        for i in range(0, len(ip_in_bin_octets)):
            if len(ip_in_bin_octets[i]) < 8:
                padded_bin = ip_in_bin_octets[i].zfill(8)
                ip_in_binary.append(padded_bin)
            else:
                ip_in_binary.append(ip_in_bin_octets[i])

        # join the binary octets
        ip_bin_mask = "".join(ip_in_binary)

        # print ip_bin_mask

        sub_in_bin = []

        # convert each subnet octet to binary
        sub_bin_octet = [bin(i).split("b")[1] for i in octet_subnet]

        # make each binary octet of 8 bit length by padding zeros
        for i in sub_bin_octet:
            if len(i) < 8:
                sub_padded = i.zfill(8)
                sub_in_bin.append(sub_padded)
            else:
                sub_in_bin.append(i)

        # print sub_in_bin
        sub_bin_mask = "".join(sub_in_bin)

        # calculating number of hosts
        no_zeros = sub_bin_mask.count("0")
        no_ones = 32 - no_zeros
        no_hosts = abs(2 ** no_zeros - 2)

        # Calculating wildcard mask
        wild_mask = []
        for i in octet_subnet:
            wild_bit = 255 - i
            wild_mask.append(wild_bit)

        wildcard = ".".join([str(i) for i in wild_mask])

        # Calculating the network and broadcast address
        network_add_bin = ip_bin_mask[:no_ones] + "0" * no_zeros
        broadcast_add_bin = ip_bin_mask[:no_ones] + "1" * no_zeros

        network_add_bin_octet = []
        broadcast_binoct = []

        [network_add_bin_octet.append(i) for i in [network_add_bin[j:j + 8]
                                                   for j in range(0, len(network_add_bin), 8)]]
        [broadcast_binoct.append(i) for i in [broadcast_add_bin[j:j + 8]
                                              for j in range(0, len(broadcast_add_bin), 8)]]

        network_add_dec_final = ".".join([str(int(i, 2)) for i in network_add_bin_octet])
        broadcast_add_dec_final = ".".join([str(int(i, 2)) for i in broadcast_binoct])

        # Calculate the host IP range
        first_ip_host = network_add_bin_octet[0:3] + [
            (bin(int(network_add_bin_octet[3], 2) + 1).split("b")[1].zfill(8))]
        first_ip = ".".join([str(int(i, 2)) for i in first_ip_host])

        last_ip_host = broadcast_binoct[0:3] + [bin(int(broadcast_binoct[3], 2) - 1).split("b")[1].zfill(8)]
        last_ip = ".".join([str(int(i, 2)) for i in last_ip_host])



    except KeyboardInterrupt:
        print("Interrupted by the User, exiting\n")
    except ValueError:
        print("Seem to have entered an incorrect value, exiting\n")
    ret_lis = [first_ip, last_ip, network_add_dec_final]
    return ret_lis


# =========== Subnet mask Calcuating =====
def mask_calc(dep_nums):
    x = 0
    if dep_nums == 1:
        x = 0
    if dep_nums == 2:
        x = 128
    if dep_nums == 3:
        x = 192
    if dep_nums == 4:
        x = 192
    if (dep_nums > 4 and dep_nums < 8):
        x = 224
    if (dep_nums > 7 and dep_nums < 16):
        x = 240
    if (dep_nums > 15 and dep_nums < 32):
        x = 240
    if (dep_nums > 31 and dep_nums < 64):
        x = 248
    if (dep_nums > 63 and dep_nums < 128):
        x = 252
    if (dep_nums > 127 and dep_nums < 255):
        x = 252
    return x


# =============route protocol ===========
def route_protocol(protocol):
    i = 0
    list_of_dep_ip = cr.execute(f"select device_ip from department_ip").fetchall()
    list_of_ip_for_router = [item for t in list_of_dep_ip for item in t]
    number_of_departments_ip = len(list_of_ip_for_router)
    print(list_of_ip_for_router)
    if (protocol == "eigrp"):
        router_file.write("\nexit\nexit\nenable\nconfigure terminal\n"
                          "router eigrp 1\n"
                          "network 10.10.10.10\n")

        while (i < number_of_departments_ip):
            router_file.write(
                f"network {list_of_ip_for_router[i]}\n"
            )
            i += 1
        router_file.write(f"\nno auto-summary\n")
    if (protocol == "rip"):
        router_file.write("\nexit\nexit\nenable\nconfigure terminal\n"
                          "router rip\n"
                          "version 2\n"
                          "network 10.10.10.10\n")
        while (i < number_of_departments_ip):
            router_file.write(
                f"network {list_of_ip_for_router[i]}\n"
            )
            i += 1

    if (protocol == "ospf"):
        router_file.write("\nexit\nexit\nenable\nconfigure terminal\n"
                          "router eigrp 1\n"
                          "network 10.10.10.10\n")
        while (i < number_of_departments_ip):
            router_file.write(
                f"network {list_of_ip_for_router[i]}\n"
            )
            i += 1
        router_file.write(f"\nno auto-summary\nexit\n")




# ==== DHCP protocol Config ======
def dhcp_en_fun():
    for child in dhcp_frame.winfo_children():
        child.configure(state='normal')

def dhcp_conf():
    an=str(dhcp_li[0].get())
    if(an=="yes"):
        list_of_deps = cr.execute(f"select device_ip from department_ip").fetchall()
        list_of_deps_name = cr.execute(f"select department from department_ip").fetchall()
        list_of_deps_gateway = cr.execute(f"select default_gateway from department_ip").fetchall()
        list_of_deps_subnet = cr.execute(f"select subnet_mask from department_ip").fetchall()
        list_of_ip_for_dhcp = [item for t in list_of_deps for item in t]
        list_of_name_for_dhcp = [item for t in list_of_deps_name for item in t]
        list_of_gateway_for_dhcp = [item for t in list_of_deps_gateway for item in t]
        list_of_subnet_for_dhcp = [item for t in list_of_deps_subnet for item in t]

        number_of_ips = len(list_of_ip_for_dhcp)

        i = 0
        while (i < number_of_ips):
            router_file.write(f"ip dhcp pool {list_of_name_for_dhcp[i]}\n"
                              f"network {list_of_ip_for_dhcp[i]} {list_of_subnet_for_dhcp[i]} \n"
                              f"default-router {list_of_gateway_for_dhcp[i]}\n"
                              f"exit\n")
            i += 1
    else:
        router_file.write(f"\n")




#=========== type every department with its name and number of devices
# ========== and store them in DB  =================================


def inserting_departments(number_of_departments):
    """

    :rtype: list
    """
    i = 0
    number_of_devices_in_department = []
    departmentslist = []
    finres = []
    while i < number_of_departments:
        deps = input("Enter Name of department number " + str(i + 1) + ":")
        devices_in_dep = int(input("Enter Number Of Devices in " + deps + " Department "))


        # =======insert to DB ===============
        cr.execute(
            f"insert into departments2(id,name,number_of_devices_in_department) values({i + 1},'{deps}',{devices_in_dep})")
        departmentslist.append(deps)
        number_of_devices_in_department.append(devices_in_dep)
        i += 1
    finres = [number_of_devices_in_department, departmentslist]
    return finres




#===== Create deps entry Frame =====
myframe=Frame()
def creating_entries():

    del labels[:] # remove any previous labels from if the callback was called before
    myframe=Frame(root,width=300,height=470,relief="solid")
    myframe.place(x=5,y=160)
    enter_dep_label = Label(myframe, text="Enter number of devices in deps and it's name ")
    enter_dep_label.place(x=5, y=5)

    def disable_entry():
        for child in myframe.winfo_children():
            child.configure(state='disabled')
    x=myvalue.get()
    value=int(x)
    #=====saving number of devices
    dumm_list.append(int(myvalue2.get()))
    #===== creating deps entry
    for i in range(value):
        labels.append(Label(myframe,text=" Department "+str(i)))
        labels[i].place(x=10,y=30+(30*i))
        num_of_devices = Entry(myframe,width=3)
        num_of_devices.place(x=100,y=30+(30*i))
        num_of_devices_entries.append(num_of_devices)
        dep_name = Entry(myframe, width=15)
        dep_name.place(x=130,y=30+(30*i))
        dep_names_entries.append(dep_name)
    mybutton2 = Button(root, text="Confirm the deps info", command=get_deps_info)
    mybutton2.place(x=20, y=590)
    mybutton3 = Button(root, text="Disable Frame", command=disable_entry)
    mybutton3.place(x=170, y=590)
    lbl = Label(myframe, text="Enter number of devices in deps and it's name ")

    lbl.grid_forget()

def get_deps_info():
    #== Get information from deps entry ======
    dep_name_list=''
    for child in path_frame.winfo_children():
        child.configure(state='normal')

    #======== Disable deps entry
    i=0
    for dep_name in dep_names_entries :
        departmentslist.append(str(dep_name.get()))
        departmentslist_for_vlans.append(str(dep_name.get()))
        number_of_devices_in_department.append(int(num_of_devices_entries[i].get()))

        cr.execute(
            f"insert into departments2(id,name,number_of_devices_in_department) values({i + 1},'{str(dep_name.get())}',"
            f"{int(num_of_devices_entries[i].get())})")
        i+=1

    cr.execute(
        f"CREATE TABLE if not exists departments as select * from departments2 order by number_of_devices_in_department desc")
    number_of_devices_in_department.sort()
    number_of_devices_in_department.reverse()
    i=0
    number_of_devices = int(myvalue2.get())
    for dep_num in number_of_devices_in_department:
        number_of_devices_in_department2.append(dep_num)
        number_of_devices_in_department3.append(dep_num)
        number_of_devices_in_department4.append(dep_num)
        i+=1




#======= ACL Enabling
def acl_enable_fun():
    for child in acl_frame.winfo_children():
        child.configure(state='normal')


#======= Show Deps For ACL ==========
def show_deps_for_acl():
    dep_table = PrettyTable()
    wildcard_list = []
    w_l = ""
    list_of_deps = cr.execute(f"select device_ip from department_ip").fetchall()
    list_of_deps_name = cr.execute(f"select department from department_ip").fetchall()
    list_of_deps_gateway = cr.execute(f"select default_gateway from department_ip").fetchall()
    list_of_deps_subnet = cr.execute(f"select subnet_mask from department_ip").fetchall()
    list_of_ip = [item for t in list_of_deps for item in t]
    list_of_name = [item for t in list_of_deps_name for item in t]
    list_of_gateway = [item for t in list_of_deps_gateway for item in t]
    list_of_subnets = [item for t in list_of_deps_subnet for item in t]

    for gatway in list_of_gateway:
        gateway_list = gatway.split(".")
        w_l = (str(255 - int(gateway_list[3])))
        wildcard = "0.0.0." + str(w_l)
        wildcard_list.append(wildcard)

    dep_table.add_column("Department Name", list_of_name)
    dep_table.add_column("Department IP ", list_of_ip)
    dep_table.add_column("Departments Subnet Mask", list_of_subnets)
    dep_table.add_column("Department Gateways", wildcard_list)
    new_window=Toplevel(root)
    new_window.geometry("600x400")
    new_window.title("Departments details")
    ll=Label(new_window,text=f"{dep_table}")
    ll.place(x=5,y=5)

#======= Typing acl in Router File ======
def do_acl():
    full_acl=str(full_acl_entry.get())
    acl_num=str(acl_num_entry.get())
    acl_pd=str(pd_entry.get())
    acl_source=str(source_entry.get())
    acl_dist=str(dist_entry.get())
    port=str(portstr.get())

    ports_num = {
        "Choose from ports":"0",
        "http : 80": "80",
        "File Transfer Protocol (FTP) : 21":"21",
        "Telnet protocol: 23":"23",
        "Simple Mail Transfer Protocol (SMTP) : 25":"25",
        "Simple File Transfer Protocol (SFTP) : 115":"115"
    }
    po=ports_num.get(port)

    if full_acl == "" :
        router_file.write(f"\naccess-list {acl_num} {acl_pd} {acl_source} {acl_dist} {po}\n")
    else :
        router_file.write(f"\n{full_acl}")


# ======= ACL Def ============

def acl_make(acl_bool):
    dep_table = PrettyTable()
    acl_number = 10
    wildcard_list = []
    w_l = ""
    list_of_deps = cr.execute(f"select device_ip from department_ip").fetchall()
    list_of_deps_name = cr.execute(f"select department from department_ip").fetchall()
    list_of_deps_gateway = cr.execute(f"select default_gateway from department_ip").fetchall()
    list_of_deps_subnet = cr.execute(f"select subnet_mask from department_ip").fetchall()
    list_of_ip = [item for t in list_of_deps for item in t]
    list_of_name = [item for t in list_of_deps_name for item in t]
    list_of_gateway = [item for t in list_of_deps_gateway for item in t]
    list_of_subnets = [item for t in list_of_deps_subnet for item in t]

    for gatway in list_of_gateway:
        gateway_list = gatway.split(".")
        w_l = (str(255 - int(gateway_list[3])))
        wildcard = "0.0.0." + str(w_l)
        wildcard_list.append(wildcard)

    dep_table.add_column("Department Name", list_of_name)
    dep_table.add_column("Department IP ", list_of_ip)
    dep_table.add_column("Departments Subnet Mask",list_of_subnets)
    dep_table.add_column("Department Gateways", wildcard_list)
    while (acl_bool):
        the_acl = f"access-list {acl_number} "
        print("The Acl Format Is : access-list access-list-number {permit|deny} {host|source source-wildcard|any}.")
        print("")
        tot_or_step = input("Do you Want to type the acl command by your self (1)? \n"
                            "Or you want to do it step by step (2)?\n"
                            "choose (1) or (2) :  ")
        if (tot_or_step == "1"):
            the_acl2 = input("type your acl as the format mintioned above :\n")
            the_acl += the_acl2
        else:
            acl_pd = input("Permit or deny ? :")
            the_acl += acl_pd + " "
            acl_source = input("Type the source :")
            the_acl += acl_source + " "
            acl_dist = input("Type the dist :")
            the_acl += acl_dist + " "
            print(the_acl)
        acl_con = input("Do You Want to Add Another ACL ?")
        if (acl_con == "yes" or acl_con == "y"):
            acl_bool = True
        else:
            acl_bool = False
        acl_number += 1



#======= Clearing ACl Fields ==========

def acl_clear():
    full_acl_entry.delete(0,'end')
    acl_num_entry.delete(0,'end')
    pd_entry.delete(0,'end')
    source_entry.delete(0,'end')
    dist_entry.delete(0,'end')




# ========================
#===== chossing path =======
def path_chossing(path,number_of_devices,number_of_devices_in_department,number_of_devices_in_department2,
                  number_of_devices_in_department3,number_of_devices_in_department4,number_of_departments):
    color_counter = 0
    switch_node = 0
    nodes_counter = 1

    switch_node_list = []

    if (path == 1):
        number_of_24_switches = 0
        number_of_48_switches = 0
        devices = number_of_devices
        router_count = 1
        switch_node = 0

        # ======== devices equal or less than 24 =========

        if (number_of_devices <= 24):
            print("All Devices In one switch We make VLAN for each department")
            number_of_24_switches += 1

            switch_24_file = open(res_directory_path+"/departments_all_in_24.txt", "w")
            switch_24_file.write("enable\nconfigure terminal\n")
            switch_24_file.write("interface range GigabitEthernet0/1-2\nswitchport mode trunk\nexit\n")
            router_file.write("interface fa0/0\nno shutdown ")

            # =======Create Table =====
            cr.execute(
                "CREATE TABLE if not exists one_24_switch(id INT,device_ip VARCHAR(45),department VARCHAR(45),vlan VARCHAR(45),default_gateway VARCHAR(45))")

            # Draw=====
            g.add_node(switch_node, value=400, title='Switch 24', label='Switch 1', color="#ee2347",
                       shape='image', image='file:///D:/graduationf/img/switch_png.png')
            nodes_counter = 1

            nodes_counter += 1
            dep_mask = mask_calc(number_of_departments)
            subnet_mask = f"255.255.255.{dep_mask}"
            switch_ip = f"192.168.1.1"
            ip_rang = subnet_calc(switch_ip, subnet_mask)
            first_ip_list = ip_rang[0].split(".")
            last_ip_list = ip_rang[1].split(".")

            last_num_in_first_ip = int(first_ip_list[3])
            last_num_in_last_ip = int(last_ip_list[3])
            network_ip = ip_rang[2]

            v = 1  # vlan * 10 *20 ....
            vv = 0  # interface counter
            vvv = 0  # counter for index of list
            vvx = 0  # while controller
            for dep in departmentslist:
                switch_24_file.write("vlan " + str(v * 10) + "\nname switch_24_vlan_" + str(v) + "\nexit\n")
                s = ""
                gateway = ""

                last_num_in_first_ip += 0
                first_ip_list[3] = str(last_num_in_first_ip)
                s = "."
                s = s.join(first_ip_list)  # ip ready to store

                # gateway store
                last_num_in_first_ip2 = last_num_in_last_ip
                gateway_list = s.split(".")
                gateway_list[3] = str(last_num_in_first_ip2)
                gateway = "."
                gateway = gateway.join(gateway_list)
                cr.execute(f"insert into department_ip(department,device_ip,subnet_mask,default_gateway)"
                           f" values('{dep}','{s}','{subnet_mask}','{gateway}')")

                s = ""

                router_file.write(
                    f"\ninterface fa0/0.{v}\nencapsulation dot1Q {v * 10}\nip address {gateway} {subnet_mask}\n")

                while (vvx < number_of_devices_in_department[vvv]):
                    # ============= setting ips for devices

                    first_ip_list[3] = str(last_num_in_first_ip)
                    s = "."
                    s = s.join(first_ip_list)  # ip ready to store

                    switch_24_file.write(
                        "interface fa0/" + str(vv + 1) + "\nswitchport mode access\nswitchport access vlan "
                        + str(v * 10) + "\nexit\n")
                    #
                    cr.execute(
                        f"insert into one_24_switch(id,device_ip,department,vlan,default_gateway) values({vv},'{s}',"
                        f"(select departments.name from departments "
                        f"where number_of_devices_in_department={number_of_devices_in_department[vvv]}),'vlan {v * 10}','{gateway}')")

                    # ============= Drawing =========

                    g.add_node(nodes_counter, value=300, title=f'Host Number {vv}', label=f'{s}',
                               color=color_list[color_counter],
                               shape='image', image='file:///D:/graduationf/img/host.png')
                    g.add_edge(switch_node, nodes_counter, title=f"interface fa0/{vv + 1}")
                    nodes_counter += 1

                    # ===========================
                    vv += 1
                    vvx += 1
                    last_num_in_first_ip += 1
                v += 1
                vvx = 0
                vvv += 1
                color_counter += 1

                # go to next sub network and start from the first number in it

                last_num_in_first_ip = last_num_in_last_ip + 3
                first_ip_list[3] = str(last_num_in_first_ip)
                s = "."
                s = s.join(first_ip_list)
                ip_rang = subnet_calc(s, subnet_mask)
                first_ip_list = ip_rang[0].split(".")
                last_ip_list = ip_rang[1].split(".")
                last_num_in_first_ip = int(first_ip_list[3])
                last_num_in_last_ip = int(last_ip_list[3])

                print(
                    f"last num in firs ip === {last_num_in_first_ip} **** last num in las ip ==={last_num_in_last_ip}")
            switch_node_list.append(switch_node)

            # =======================
            # Devices number less than 48
            # use one 48 switch
            # =======================

        # =========================================
        # ========== devices equal or less than 48
        # =========================================
        if (number_of_devices > 24 and number_of_devices <= 48):
            print("get 48 port switch \nAll Devices In one switch \n We make VLAN for each department")
            number_of_48_switches += 1
            switch_48_file = open(res_directory_path+"/departments_all_in_48.txt", "w")
            switch_48_file.write("enable\nconfigure terminal\n")
            switch_48_file.write("interface range GigabitEthernet0/1-2\nswitchport mode trunk\nexit\n")

            router_file.write("interface fa0/0\nno shutdown\nexit")

            # =======Create Table =====
            cr.execute(
                "CREATE TABLE if not exists one_48_switch(id INT,device_ip VARCHAR(45),department VARCHAR(45),"
                "vlan VARCHAR(45),default_gateway VARCHAR(45))")

            # Draw=====
            g.add_node(switch_node, value=400, title='Switch 48', label='Switch 1', color="#ee2347",
                       shape='image', image='file:///D:/graduationf/img/switch_png.png')
            nodes_counter = 1

            # =============

            # first calc mask then get first ip in first subnet and the last ip in subnet

            dep_mask = mask_calc(number_of_departments)
            subnet_mask = f"255.255.255.{dep_mask}"
            switch_ip = f"192.168.1.1"
            ip_rang = subnet_calc(switch_ip, subnet_mask)
            first_ip_list = ip_rang[0].split(".")
            last_ip_list = ip_rang[1].split(".")

            last_num_in_first_ip = int(first_ip_list[3])
            last_num_in_last_ip = int(last_ip_list[3])
            network_ip = ip_rang[2]

            # ==========

            v = 1
            vv = 0
            vvv = 0
            vvx = 0
            for dep in departmentslist:
                switch_48_file.write("vlan " + str(v * 10) + "\nname switch_24_vlan_" + str(v) + "\nexit\n")

                # store department ip
                gateway = ""

                last_num_in_first_ip -= 1
                first_ip_list[3] = str(last_num_in_first_ip)
                s = "."
                s = s.join(first_ip_list)  # ip ready to store
                # gateway store
                last_num_in_first_ip2 = last_num_in_last_ip
                gateway_list = s.split(".")
                gateway_list[3] = str(last_num_in_first_ip2)
                gateway = "."
                gateway = gateway.join(gateway_list)
                cr.execute(f"insert into department_ip(department,device_ip,subnet_mask,default_gateway) "
                           f"values('{dep}','{s}','{subnet_mask}','{gateway}')")

                s = ""

                router_file.write(
                    f"\ninterface fa0/0.{v}\nencapsulation dot1Q {v * 10}\nip address {gateway} {subnet_mask}\n")

                last_num_in_first_ip += 1
                s = ""
                while (vvx < number_of_devices_in_department[vvv]):
                    switch_48_file.write(
                        "interface fa0/" + str(vv + 1) + "\nswitchport mode access\nswitchport access vlan "
                        + str(v * 10) + "\nexit\nexit\n")
                    # =======

                    first_ip_list[3] = str(last_num_in_first_ip)
                    s = "."
                    s = s.join(first_ip_list)  # ip ready to store

                    cr.execute(
                        f"insert into one_48_switch(id,device_ip,department,vlan,default_gateway) values({vv},'{s}',"
                        f"(select departments.name from departments "
                        f"where number_of_devices_in_department={number_of_devices_in_department[vvv]}),'vlan {v * 10}','{gateway}')")

                    # ==========

                    # ============= Drawing =========

                    g.add_node(nodes_counter, value=300, title=f'Host Number {vv}', label=f'{s}',
                               color=color_list[color_counter],
                               shape='image', image='file:///D:/graduationf/img/host.png')
                    g.add_edge(switch_node, nodes_counter, title=f"interface fa0/{vv + 1}")
                    nodes_counter += 1

                    # ===========================

                    vv += 1
                    vvx += 1
                    last_num_in_first_ip += 1
                v += 1
                vvx = 0
                vvv += 1

                color_counter += 1

                # ===============

                last_num_in_first_ip = last_num_in_last_ip + 3
                first_ip_list[3] = str(last_num_in_first_ip)
                s = "."
                s = s.join(first_ip_list)
                ip_rang = subnet_calc(s, subnet_mask)
                first_ip_list = ip_rang[0].split(".")
                last_ip_list = ip_rang[1].split(".")

                last_num_in_first_ip = int(first_ip_list[3])
                last_num_in_last_ip = int(last_ip_list[3])

                # ==============
            switch_node_list.append(switch_node)

        counter_for_interfaces = 0

        # ========================================
        # ======== devices more than 48 =========
        # ========================================
        if (number_of_devices > 48):
            k = 1
            rounds = 0
            for i in number_of_devices_in_department3:
                x = 0
                k = 0
                kk = 0
                m = 0
                round24 = 0
                round48 = 0
                counter_less_than24 = 0
                counter_less_than48 = 0
                print("num 3 :")
                print(number_of_devices_in_department3)
                print("num  :")
                print(number_of_devices_in_department)
                print("i = " + str(i))

                pointer_for_department = number_of_devices_in_department2.index(i)  ## GEt Department index
                print(str(pointer_for_department) + ' pointer for department')
                number_of_devices_in_department_for_vlans = []
                department_for_vlans = []
                # ========================================
                # ========================================
                # لما يكون القسم اقل من 24
                # ========================================
                # ========================================

                if (i <= 24):
                    file24txt = res_directory_path+"/switch_24_" + str(number_of_24_switches) + ".txt"
                    # if(os.path.isfile(file24txt)):
                    #      file24txt="switch_24_"+str(number_of_24_switches)
                    file24 = open(file24txt, "w")
                    k = 24 - i
                    kk = 48 - i

                    # ====== Setting Tables =====
                    devices_in_switch24_table = f"devices_in_switch24_{rounds}"
                    switch24_table = f"switch24_{rounds}"
                    cr.execute(f"CREATE TABLE if not exists {devices_in_switch24_table}"
                               f"(id INT ,department_name VARCHAR(45),devices_number_in_department INT)")
                    # =================

                    v = 1  # vlan * 10 *20 ....
                    vv = 0  # interface counter
                    vvv = 0  # counter for index of list
                    vvx = 0  # while controller
                    print("k=" + str(k))
                    print("kkk=" + str(kk))
                    number_of_devices_in_department_for_vlans.append(number_of_devices_in_department3[0])
                    department_for_vlans.append(departmentslist[pointer_for_department])

                    file24.write("en\nconf t\ninterface range GigabitEthernet0/1-2\nswitchport mode trunk\nexit\n")

                    file24.write("vlan " + str(v * 10) + "\nname switch_24_vlan_" + str(v) + "\nexit\n")
                    print("WE will get out " + str(number_of_devices_in_department[0]))
                    dev_in_dep_in_db = cr.execute(f"select departments.number_of_devices_in_department from "
                                                  f"departments where number_of_devices_in_department={number_of_devices_in_department[0]}")
                    # number_of_devices_in_department3.pop(0)
                    while (vvx < i):  # توزيع الانترفيسات

                        file24.write(
                            "interface fa0/" + str(vv) + "\nswitchport mode access\nswitchport access vlan "
                            + str(v * 10) + "\nexit\n")
                        vv += 1
                        vvx += 1
                        counter_for_interfaces = vv
                    v += 1
                    vvx = 0

                    cr.execute(
                        f"insert into {devices_in_switch24_table}(id,department_name,devices_number_in_department) "
                        f"values({vv},(select departments.name from departments "
                        f"where number_of_devices_in_department={number_of_devices_in_department[0]}),"
                        f"'{number_of_devices_in_department[0]}')")
                    number_of_devices_in_department.pop(0)
                    print("list for loop")
                    number_of_devices_in_department2 = number_of_devices_in_department.copy()  # Copy it so the value dont lost when removing it
                    print(number_of_devices_in_department)
                    if (len(number_of_devices_in_department) == 0):
                        number_of_24_switches += 1
                    for j in number_of_devices_in_department2:
                        print("KK in loop=" + str(kk))
                        if (j <= kk and i + j > 25):

                            # يعني لما يكون قسم اللي عندي اقل من 24 بس باقي اقسام ومجموعهن اقل من 48
                            # بضيف واحد 48 بدل ما ضيف تنين 24 مثلا 20 و 10

                            switch24_table = f"switch48_{rounds}"

                            dev_in_dep_in_db = cr.execute(f"select departments.number_of_devices_in_department from "
                                                          f"departments where number_of_devices_in_department={j}")

                            m = number_of_devices_in_department.index(j)
                            m1 = number_of_devices_in_department3.index(j)
                            pointer_for_department = number_of_devices_in_department3.index(j)  ## GEt Department index
                            department_for_vlans.append(departmentslist[pointer_for_department])

                            vv = counter_for_interfaces
                            vvv = 0  # counter for index of list
                            vvx = 0  # while controller
                            file24.write("vlan " + str(v * 10) + "\nname switch_24_vlan_" + str(v) + "\nexit\n")
                            while (vvx < j):  # توزيع الانترفيسات
                                file24.write(
                                    "interface fa0/" + str(vv + 1) + "\nswitchport mode access\nswitchport access vlan "
                                    + str(v * 10) + "\nexit\n")



                                vv += 1
                                vvx += 1
                            v += 1
                            vvx = 0



                            print("we Got out " + str(m) + " " + str(
                                number_of_devices_in_department[m]) + "\nnum dev in departs")
                            cr.execute(
                                f"insert into {devices_in_switch24_table}(id,department_name,devices_number_in_department) "
                                f"values({vv},(select departments.name from departments "
                                f"where number_of_devices_in_department={number_of_devices_in_department[m]}),"
                                f"'{number_of_devices_in_department[m]}')")

                            number_of_devices_in_department.pop(m)
                            number_of_devices_in_department3.pop(m1)
                            kk = kk - j
                            counter_less_than48 += 1
                            round48 += 1
                            if (round48 > 1):
                                counter_less_than48 -= 1
                                continue

                        elif j <= k and i + j < 25:

                            # When rest devicess are les than 24 NOOO need for 48 switch

                            m = number_of_devices_in_department.index(j)
                            m1 = number_of_devices_in_department3.index(j)
                            # pointer_for_department = number_of_devices_in_department3.index(j)  ## GEt Department index
                            department_for_vlans.append(departmentslist[pointer_for_department])
                            vvv = 0  # counter for index of list
                            vvx = 0  # while controller
                            file24.write("vlan " + str(v * 10) + "\nname switch_24_vlan_" + str(v) + "\nexit\n")
                            while (vvx < j):  # توزيع الانترفيسات
                                file24.write(
                                    "\ninterface fa0/" + str(
                                        vv + 1) + "\nswitchport mode access\nswitchport access vlan "
                                    + str(v * 10) + "\nexit\n")



                                vv += 1
                                vvx += 1
                            v += 1
                            vvx = 0

                            print("we Got out2 " + str(number_of_devices_in_department2.index(j)) + "  " + str(
                                number_of_devices_in_department[m]))
                            cr.execute(
                                f"insert into {devices_in_switch24_table}(id,department_name,devices_number_in_department) "
                                f"values({vv},(select departments.name from departments "
                                f"where number_of_devices_in_department={number_of_devices_in_department[m]}),"
                                f"'{number_of_devices_in_department[m]}')")

                            number_of_devices_in_department.pop(m)
                            number_of_devices_in_department3.pop(m1)
                            counter_less_than24 += 1
                            round24 += 1
                            if (round24 > 1):
                                counter_less_than24 -= 1


                    number_of_48_switches += counter_less_than48
                    number_of_24_switches += counter_less_than24

                    print("24=" + str(number_of_24_switches))
                    print("48=" + str(number_of_48_switches))
                    # print(department_for_vlans)

                    cr.execute(
                        f"CREATE TABLE if not exists {switch24_table}(id INT ,ip VARCHAR(45),"
                        f"department_name VARCHAR(45), vlan_number VARCHAR(45),default_gateway VARCHAR(45))")

                    # ===== Storing IPs for devices in DB  & Drawing
                    # ===== Get departments and devices in it for every switch
                    db_select_devices_in_switch = cr.execute(f"select devices_number_in_department from "
                                                             f"{devices_in_switch24_table}").fetchall()
                    list_of_db_select_devices_in_switch = [item for t in db_select_devices_in_switch for item in t]
                    number_of_departments_in_switch = len(list_of_db_select_devices_in_switch)

                    # ========== set the mask and first ip ==============

                    dep_mask = mask_calc(number_of_departments_in_switch)
                    subnet_mask = f"255.255.255.{dep_mask}"
                    switch_ip = f"192.168.{rounds+1}.0"
                    ip_rang = subnet_calc(switch_ip, subnet_mask)
                    first_ip_list = ip_rang[0].split(".")
                    last_ip_list = ip_rang[1].split(".")

                    last_num_in_first_ip = int(first_ip_list[3])
                    last_num_in_last_ip = int(last_ip_list[3])
                    network_ip = ip_rang[2]
                    soso = 0
                    ip_counter = 0
                    ip_counter2 = 0
                    vlan_counter = 10
                    color_counter = 0
                    router_interface_counter = 0
                    while (soso < number_of_departments_in_switch):
                        # We are In one switch here
                        ip_counter2 = 0
                        # =====Drawing =======

                        g.add_node(switch_node, value=400, title=f'Switch_{soso}', label=f'Switch {soso}',
                                   color="#ee2347", shape='image', image='file:///D:/graduationf/img/switch_png.png')
                        # ==========

                        # ==========store department ip ====

                        last_num_in_first_ip -= 1
                        first_ip_list[3] = str(last_num_in_first_ip)
                        s = "."
                        s = s.join(first_ip_list)  # ip ready to store

                        last_num_in_first_ip += 1
                        gateway = ""
                        # gateway store
                        last_num_in_first_ip2 = last_num_in_last_ip
                        gateway_list = s.split(".")
                        gateway_list[3] = str(last_num_in_first_ip2)
                        gateway = "."
                        gateway = gateway.join(gateway_list)

                        cr.execute(f"insert into department_ip(department,device_ip,subnet_mask, default_gateway)"
                                   f" values((select departments.name from departments "
                                   f"where number_of_devices_in_department={list_of_db_select_devices_in_switch[soso]}),"
                                   f"'{s}', '{subnet_mask}', '{gateway}')")

                        s = ""


                        router_file.write(f"interface fa0/{rounds}\n"
                                          f"no shut")
                        router_file.write(
                            f"\ninterface fa0/{rounds}.{soso + 1}\nencapsulation dot1Q {vlan_counter}"
                            f"\nip address {gateway} {subnet_mask}\n")

                        while (ip_counter2 < list_of_db_select_devices_in_switch[soso]):
                            # IPs for devices ------

                            first_ip_list[3] = str(last_num_in_first_ip)
                            s = "."
                            s = s.join(first_ip_list)  # ip ready to store

                            # store the IP
                            cr.execute(
                                f"insert into {switch24_table}(id,ip,department_name,vlan_number,default_gateway) "
                                f"values({ip_counter},'{s}',(select departments.name from departments where"
                                f" number_of_devices_in_department={list_of_db_select_devices_in_switch[soso]})"
                                f",{vlan_counter},'{gateway}')")

                            # ============= Drawing =========

                            g.add_node(nodes_counter, value=300, title=f'Host Number {ip_counter}', label=f'{s}',
                                       color=color_list[color_counter], shape='image',
                                       image='file:///D:/graduationf/img/host.png')
                            g.add_edge(switch_node, nodes_counter, title=f"interface fa0/{ip_counter2}", )

                            nodes_counter += 1
                            print(f"24 Switch Node = {switch_node} ============ nodes Counter = {nodes_counter}")

                            # ===========================

                            last_num_in_first_ip += 1
                            ip_counter += 1
                            ip_counter2 += 1
                            # end While loop

                        # ================ IP--- Go to next sub network
                        last_num_in_first_ip = last_num_in_last_ip + 3
                        first_ip_list[3] = str(last_num_in_first_ip)
                        s = "."
                        s = s.join(first_ip_list)
                        ip_rang = subnet_calc(s, subnet_mask)
                        first_ip_list = ip_rang[0].split(".")
                        last_ip_list = ip_rang[1].split(".")
                        last_num_in_first_ip = int(first_ip_list[3])
                        last_num_in_last_ip = int(last_ip_list[3])

                        print(
                            f"last num in firs ip === {last_num_in_first_ip} **** last num in las ip ==={last_num_in_last_ip}")
                        # ===================
                        vlan_counter += 10
                        soso += 1
                        color_counter += 1
                        router_interface_counter += 1

                    # =======================
                    switch_node_list.append(switch_node)
                    switch_node = nodes_counter + 1
                    nodes_counter += 2

                    print("|===== End of Round " + str(rounds) + " =====|")

                # ========================================
                # ========================================
                # لما يكون القسم اقل من 48
                # ========================================
                # ========================================

                if 24 < i <= 48:
                    number_of_48_switches += 1
                    x = 48 - i
                    file48txt = res_directory_path+"/switch_48_" + str(number_of_48_switches) + ".txt"
                    file48 = open(file48txt, "w")
                    k = 24 - i
                    kk = 48 - i

                    # ====================
                    devices_in_switch48_table = f"devices_in_switch48_{rounds}"
                    switch48_table = f"switch48_{rounds}"
                    cr.execute(
                        f"CREATE TABLE if not exists {devices_in_switch48_table}(id INT ,department_name VARCHAR(45),"
                        f"devices_number_in_department INT)")

                    # =======================

                    v = 1  # vlan * 10 *20 ....
                    vv = 0  # interface counter
                    vvv = 0  # counter for index of list
                    vvx = 0  # while controller

                    number_of_devices_in_department_for_vlans.append(number_of_devices_in_department[0])
                    department_for_vlans.append(departmentslist[pointer_for_department])
                    file48.write("en\nconf t\ninterface range GigabitEthernet0/1-2\nswitchport mode trunk\nexit\n")
                    file48.write("vlan " + str(v * 10) + "\nname switch_48_vlan_" + str(v) + "\nexit\n")
                    print("WE will get out " + str(number_of_devices_in_department[0]))
                    # number_of_devices_in_department3.pop(0)
                    while (vvx < i):  # توزيع الانترفيسات
                        file48.write(
                            "interface fa0/" + str(vv + 1) + "\nswitchport mode access\nswitchport access vlan "
                            + str(v * 10) + "\nexit\n")

                        vv += 1
                        vvx += 1
                    v += 1
                    vvx = 0

                    print("WE will get out " + str(number_of_devices_in_department[0]))
                    # number_of_devices_in_department3.pop(0)
                    cr.execute(
                        f"insert into {devices_in_switch48_table}(id,department_name,devices_number_in_department) "
                        f"values({vv},(select departments.name from departments "
                        f"where number_of_devices_in_department={number_of_devices_in_department[0]}),"
                        f"'{number_of_devices_in_department[0]}')")

                    number_of_devices_in_department.pop(0)
                    print("list for loop")
                    print(number_of_devices_in_department)
                    number_of_devices_in_department2 = number_of_devices_in_department.copy()  # Copy it so the value dont lost when removing it
                    for f in number_of_devices_in_department2:
                        if (f <= x):
                            vvv = 0
                            vvx = 0
                            m = number_of_devices_in_department.index(f)
                            m1 = number_of_devices_in_department3.index(f)
                            pointer_for_department = number_of_devices_in_department3.index(f)  ## GEt Department index
                            department_for_vlans.append(departmentslist[pointer_for_department])
                            vvv = 0  # counter for index of list
                            vvx = 0  # while controller
                            file48.write("vlan " + str(v * 10) + "\nname switch_48_vlan_" + str(v)+"\nexit\n")
                            while (vvx < f):  # توزيع الانترفيسات
                                file48.write(
                                    "\ninterface fa0/" + str(
                                        vv + 1) + "\nswitchport mode access\nswitchport access vlan "
                                    + str(v * 10) + "\nexit\n")

                                vv += 1
                                vvx += 1
                            v += 1
                            vvx = 0

                            print("we Got out " + str(m) + "  " + str(
                                number_of_devices_in_department[m]) + "\nnum dev in departs")

                            cr.execute(
                                f"insert into {devices_in_switch48_table}(id,department_name,devices_number_in_department) "
                                f"values({vv},(select departments.name from departments "
                                f"where number_of_devices_in_department={number_of_devices_in_department[m]}),"
                                f"'{number_of_devices_in_department[m]}')")

                            number_of_devices_in_department.pop(m)
                            number_of_devices_in_department3.pop(m1)
                            x -= f
                            print(str(x) + "XXXX")
                    print("24=" + str(number_of_24_switches))
                    print("48=" + str(number_of_48_switches))

                    cr.execute(
                        f"CREATE TABLE if not exists {switch48_table}(id INT ,ip VARCHAR(45),"
                        f"department_name VARCHAR(45), vlan_number VARCHAR(45),default_gateway VARCHAR(45))")

                    # ===== Storing IPs for devices in DB
                    # ===== Get departments and devices in it for every switch
                    db_select_devices_in_switch = cr.execute(
                        f"select devices_number_in_department from {devices_in_switch48_table}").fetchall()
                    list_of_db_select_devices_in_switch = [item for t in db_select_devices_in_switch for item in t]
                    number_of_departments_in_switch = len(list_of_db_select_devices_in_switch)

                    # ========== set the mask and first ip ==============

                    dep_mask = mask_calc(number_of_departments_in_switch)
                    subnet_mask = f"255.255.255.{dep_mask}"
                    switch_ip = f"192.168.{rounds+1}.1"
                    ip_rang = subnet_calc(switch_ip, subnet_mask)
                    first_ip_list = ip_rang[0].split(".")
                    last_ip_list = ip_rang[1].split(".")
                    last_num_in_first_ip = int(first_ip_list[3])
                    last_num_in_last_ip = int(last_ip_list[3])
                    network_ip = ip_rang[2]
                    soso = 0
                    ip_counter = 0
                    ip_counter2 = 0
                    vlan_counter = 10
                    color_counter = 0
                    router_interface_counter = 0
                    while (soso < number_of_departments_in_switch):
                        ip_counter2 = 0

                        # =====Drawing =======

                        g.add_node(switch_node, value=400, title=f'Switch_{soso}', label=f'Switch',
                                   color="#ee2347", shape='image', image='file:///D:/graduationf/img/switch_png.png')

                        # ===============================
                        # ==========store department ip ====
                        last_num_in_first_ip -= 1
                        first_ip_list[3] = str(last_num_in_first_ip)
                        s = "."
                        s = s.join(first_ip_list)  # ip ready to store

                        last_num_in_first_ip += 1
                        gateway = ""
                        # gateway store
                        last_num_in_first_ip2 = last_num_in_last_ip
                        gateway_list = s.split(".")
                        gateway_list[3] = str(last_num_in_first_ip2)
                        gateway = "."
                        gateway = gateway.join(gateway_list)
                        cr.execute(f"insert into department_ip(department,device_ip,subnet_mask, default_gateway)"
                                   f" values((select departments.name from departments "
                                   f"where number_of_devices_in_department={list_of_db_select_devices_in_switch[soso]})"
                                   f",'{s}', '{subnet_mask}', '{gateway}')")

                        s = ""
                        router_file.write(f"interface fa0/{rounds}\n"
                                          f"no shut\nexit")
                        router_file.write(
                            f"\ninterface fa0/{rounds}.{soso + 1}\nencapsulation dot1Q {vlan_counter}"
                            f"\nip address {gateway} {subnet_mask}\n")

                        while (ip_counter2 < list_of_db_select_devices_in_switch[soso]):
                            # IPs for devices ------

                            first_ip_list[3] = str(last_num_in_first_ip)
                            s = "."
                            s = s.join(first_ip_list)  # ip ready to store

                            # store the IP
                            cr.execute(
                                f"insert into {switch48_table}(id,ip,department_name,vlan_number,default_gateway) "
                                f"values({ip_counter},'{s}',(select departments.name from departments "
                                f"where number_of_devices_in_department={list_of_db_select_devices_in_switch[soso]}),"
                                f"{vlan_counter},'{gateway}')")
                            # ============= Drawing =========

                            g.add_node(nodes_counter, value=300, title=f'Host Number {ip_counter}', label=f'{s}',
                                       color=color_list[color_counter], shape='image',
                                       image='file:///D:/graduationf/img/host.png')
                            g.add_edge(switch_node, nodes_counter, title=f"interface fa0/{ip_counter2}")
                            nodes_counter += 1
                            print(f"48 Switch Node = {switch_node} ============ nodes Counter = {nodes_counter}")

                            # ===========================

                            last_num_in_first_ip += 1
                            ip_counter += 1
                            ip_counter2 += 1
                            # end While loop

                        # ================ IP--- Go to next sub network
                        last_num_in_first_ip = last_num_in_last_ip + 3
                        first_ip_list[3] = str(last_num_in_first_ip)
                        s = "."
                        s = s.join(first_ip_list)
                        ip_rang = subnet_calc(s, subnet_mask)
                        first_ip_list = ip_rang[0].split(".")
                        last_ip_list = ip_rang[1].split(".")
                        last_num_in_first_ip = int(first_ip_list[3])
                        last_num_in_last_ip = int(last_ip_list[3])

                        print(
                            f"last num in firs ip === {last_num_in_first_ip} **** last num in las ip ==={last_num_in_last_ip}")
                        # ===================
                        vlan_counter += 10
                        soso += 1
                        color_counter += 1
                        router_interface_counter += 1

                    # =======================
                    print("|===== End of Round " + str(rounds) + " =====|")
                    switch_node_list.append(switch_node)
                    switch_node = nodes_counter + 1
                    nodes_counter += 2

                # ========================================
                # ========================================
                # لما يكون القسم اكبر من 48
                # ========================================
                # ========================================

                if (i > 48):
                    x = i-48
                    xx = 1
                    while (xx):
                        if (x <= 24):
                            number_of_24_switches += 1
                            x-=24
                            if (x <= 0):
                                xx = 0
                        if (x > 24 and x <= 48):
                            x = x - 48
                            number_of_48_switches += 1
                            if (x <= 0):
                                xx = 0
                        if (x > 48):
                            x = x - 48
                            number_of_48_switches += 1
                            if (x <= 0):
                                xx = 0
                    print(number_of_devices_in_department)
                    print("24=" + str(number_of_24_switches))
                    print("48=" + str(number_of_48_switches))
                    print("|===== End of Round " + str(rounds) + " =====|")

                rounds += 1

    # =========================================
    # =========================================
    # =======  EXTENDED PATH  =================
    # =========================================
    # =========================================

    if (path == 2):
        router_count = 2
        number_of_24_switches = 0
        number_of_48_switches = 0
        devices = number_of_devices
        networkCounter = 1
        key = 0

        switch_node = 0
        color_counter = 0
        nodes_counter = 1

        for i in number_of_devices_in_department3:
            devices_counter = 0

            # ======================================
            # == Department less than 24 device in it
            # ======================================

            if (i <= 24):
                number_of_24_switches += 1
                # ==============Store To DB
                cr.execute(f"CREATE TABLE if not exists "
                           f"switch_24_{key}(id INT,device_ip VARCHAR(45),department_name VARCHAR(45))")

                # ========== Draw=====
                g.add_node(switch_node, value=400, title='Switch 24', label=f'Switch {key}', color="#ee2347",
                           shape='image', image='file:///D:/graduationf/img/switch_png.png')
                switch_node_list.append(switch_node)
                # =============

                switch_ip = f"192.168.{networkCounter}.1"
                subnet_mask = f"255.255.255.0"
                ip_rang = subnet_calc(switch_ip, subnet_mask)
                first_ip_list = ip_rang[0].split(".")
                last_ip_list = ip_rang[1].split(".")

                last_num_in_first_ip = int(first_ip_list[3])
                last_num_in_last_ip = int(last_ip_list[3])
                network_ip = ip_rang[2]

                # ==========store department ip ====
                last_num_in_first_ip -= 1
                first_ip_list[3] = str(last_num_in_first_ip)
                s = "."
                s = s.join(first_ip_list)  # ip ready to store

                last_num_in_first_ip += 1
                gateway = ""
                # gateway store
                last_num_in_first_ip2 = last_num_in_last_ip
                gateway_list = s.split(".")
                gateway_list[3] = str(last_num_in_first_ip2)
                gateway = "."
                gateway = gateway.join(gateway_list)

                cr.execute(f"insert into department_ip(department,device_ip,subnet_mask, default_gateway)"
                           f" values((select departments.name from departments "
                           f"where number_of_devices_in_department={i}),'{s}', '{subnet_mask}', '{gateway}')")
                s = ""

                while devices_counter < i:
                    # ============= setting ips for devices

                    first_ip_list[3] = str(last_num_in_first_ip)
                    s = "."
                    s = s.join(first_ip_list)  # ip ready to store

                    cr.execute(f"insert into switch_24_{key}(id,device_ip,department_name) values({devices_counter},'{s}',"
                               f"(select departments.name from departments "
                               f"where number_of_devices_in_department={i}))")

                    # ======Drawing Hosts ========
                    print(f"nodes counter ={nodes_counter}")
                    print(f"switch counter ={switch_node}")
                    g.add_node(nodes_counter, value=300, title=f'Host Number {devices_counter}',
                               label=f'{s}', color=color_list[color_counter], shape='image',
                               image='file:///D:/graduationf/img/host.png')
                    g.add_edge(switch_node, nodes_counter)

                    nodes_counter += 1
                    devices_counter += 1
                    last_num_in_first_ip += 1

                print("==== add 24 Switch ====")



            # ===============================
            # Department >24 and less than 48
            # ===============================

            elif (i > 24 and i <= 48):
                number_of_48_switches += 1

                # ==============Stor To DB
                cr.execute(f"CREATE TABLE if not exists "
                           f"switch_48_{key}(id INT,device_ip VARCHAR(45),department_name VARCHAR(45))")

                # ========== Draw=====
                g.add_node(switch_node, value=400, title='Switch 48', label=f'Switch {key}', color="#ee2347",
                           shape='image', image='file:///D:/graduationf/img/switch_png.png')
                switch_node_list.append(switch_node)
                # =============

                switch_ip = f"192.168.{networkCounter}.1"
                subnet_mask = f"255.255.255.0"
                ip_rang = subnet_calc(switch_ip, subnet_mask)
                first_ip_list = ip_rang[0].split(".")
                last_ip_list = ip_rang[1].split(".")

                last_num_in_first_ip = int(first_ip_list[3])
                last_num_in_last_ip = int(last_ip_list[3])
                network_ip = ip_rang[2]

                # ==========store department ip ====
                last_num_in_first_ip -= 1
                first_ip_list[3] = str(last_num_in_first_ip)
                s = "."
                s = s.join(first_ip_list)  # ip ready to store
                # cr.execute(
                #     f"insert into department_ip(department,device_ip) values((select departments.name from departments "
                #     f"where number_of_devices_in_department={i}),'{s}')")

                last_num_in_first_ip += 1

                gateway = ""
                # gateway store
                last_num_in_first_ip2 = last_num_in_last_ip
                gateway_list = s.split(".")
                gateway_list[3] = str(last_num_in_first_ip2)
                gateway = "."
                gateway = gateway.join(gateway_list)

                cr.execute(f"insert into department_ip(department,device_ip,subnet_mask, default_gateway)"
                           f" values((select departments.name from departments "
                           f"where number_of_devices_in_department={i}),'{s}', '{subnet_mask}', '{gateway}')")

                s = ""

                while devices_counter < i:
                    # ============= setting ips for devices

                    first_ip_list[3] = str(last_num_in_first_ip)
                    s = "."
                    s = s.join(first_ip_list)  # ip ready to store

                    cr.execute(f"insert into switch_48_{key}(id,device_ip,department_name) values({devices_counter},'{s}',"
                               f"(select departments.name from departments "
                               f"where number_of_devices_in_department={i}))")

                    # ======Drawing Hosts ========
                    print(f"nodes counter ={nodes_counter}")
                    print(f"switch counter ={switch_node}")
                    g.add_node(nodes_counter, value=300, title=f'Host Number {devices_counter}',
                               label=f'{s}', color=color_list[color_counter], shape='image',
                               image='file:///D:/graduationf/img/host.png')
                    g.add_edge(switch_node, nodes_counter)

                    nodes_counter += 1
                    devices_counter += 1
                    last_num_in_first_ip += 1
                print("Add 48 Switch 24<>48")


            elif (i > 48):
                x = i
                xx = 1
                while (xx):
                    if (x <= 24):
                        x = x - 48
                        number_of_24_switches += 1
                        if (x <= 0):
                            xx = 0
                    if (x > 24 and x <= 48):
                        x = x - 48
                        number_of_48_switches += 1
                        if (x <= 0):
                            xx = 0
                    if (x > 48):
                        x = x - 48
                        number_of_48_switches += 1
                        if (x <= 0):
                            xx = 0
            key += 1
            color_counter += 1
            networkCounter += 1
            switch_node = nodes_counter + 1
            nodes_counter += 2
    switch_list=[]
    switches_list=[number_of_24_switches,number_of_48_switches]
    number_of_24_switches = switches_list[0]
    number_of_48_switches = switches_list[1]

    print(str(number_of_24_switches) + "*24 port switch")
    print(str(number_of_48_switches) + "*48 port switch")
    print(f"The departments {number_of_devices_in_department4}")

    # ========= Router Nodes Drawing =========
    g.add_node(1000, value=600, title=f'Router', label=f'Router',
               color='#57ee79', shape="image", image="file:///D:/graduationf/img/router_png.png")
    g.add_node(1001, value=600, title=f'Router2', label=f'Router2',
               color='#57ee79', shape="image", image='file:///D:/graduationf/img/router_png.png')
    g.add_node(1002, x=300, y=200, value=600, title=f'Router3', label=f'Router3',
               color='#57ee79', shape="image", image='file:///D:/graduationf/img/router_png.png')
    switch_node_counter = 0
    # ========= linking routers =======
    while (switch_node_counter < len(switch_node_list)):
        g.add_edge(1000, switch_node_list[switch_node_counter], width=3)
        g.add_edge(1001, switch_node_list[switch_node_counter], width=3)
        switch_node_counter += 1

    g.add_edge(1000, 1002, width=3)
    g.add_edge(1001, 1002, width=3)

    print(f" edges are {len(g.get_edges())}")
    for lolo in switch_node_list:
        print(f"each node neighbors {len(g.neighbors(lolo))}")
    g.show(res_directory_path+'/graph.html')

    # ==================================


#===========


#=======Path Choosed and excute the path_chossing(path,number_of_devices,.......)

def path_comm():
    number_of_departments=int(myvalue.get())
    number_of_devices=int(myvalue2.get())

    for child in path_frame.winfo_children():
        child.configure(state='disabled')


    #==== First Try if there was an error
    # try:

    c_path = int(path_value.get())
    print("the Path Is "+str(c_path))

    path_chossing(c_path,number_of_devices, number_of_devices_in_department, number_of_devices_in_department2
                  , number_of_devices_in_department3, number_of_devices_in_department4,number_of_departments)
    # except:
    #     c_path=1
    #     path_chossing(c_path,number_of_devices, number_of_devices_in_department, number_of_devices_in_department2
    #               , number_of_devices_in_department3, number_of_devices_in_department4,number_of_departments)
#====== router_choose ======

def exp_router_choosed():
    expens_or_cheap2=True
    expens_or_cheap_list[0]=expens_or_cheap2


def cheap_router_choosed():
    expens_or_cheap2 = False
    expens_or_cheap_list[0] = expens_or_cheap2

def router_choose():
    router_window=Toplevel(root)
    router_window.geometry("1000x700")
    router_window.title("Choose Router")


    #==== Expesv Details ========
    exp_title=Label(router_window,text="CISCO2911-HSEC+/K9 Cisco 2900 Series Routers",foreground="green",font=('Sans','10','bold'))
    exp_title.place(x=60,y=10)
    cs2911_img = HTMLLabel(router_window, html="""
        <img src="img/2911.jpg">
        """)
    cs2911_img.place(x=60, y=40)
    exp_details=expsv_router_spec()[0]
    exp_label1=Label(router_window,text=exp_details)
    exp_label1.place(x=10,y=180) #140
    exp_ship=Label(router_window,text="Shipping And Price Details",foreground="green")
    exp_ship.place(x=10,y=350)
    exp_ship_s=expsv_router_spec()[1]
    exp_ship_d=Label(router_window,text=exp_ship_s)    # exp_details=expsv_router_spec()[0]
    exp_ship_d.place(x=10,y=380)
    exp_button=Button(router_window,text="Choose CISCO2911",command=exp_router_choosed)
    exp_button.place(x=140,y=630)
    cs2911_url = HTMLLabel(router_window, html="""
            <a style='font-size=5px;' href='https://www.router-switch.com/cisco2911-hsec-k9-p-5625.html'>Checkout The CISCO2911-HSEC+/K9 Page</a>
        """)

    cs2911_url.place(x=30, y=660)

    #==== Cheap Router Details ========
    cheap_title=Label(router_window,text="CISCO2811 Cisco 2811 Router 2800 Series ISR",foreground="green", font = ('Sans','10','bold'))
    cheap_title.place(x=460,y=10)
    cs2811_img = HTMLLabel(router_window, html="""
         <img src="img/2811.jpg">
         """)
    cs2811_img.place(x=460, y=30)
    cheap_details=cheap_router_spec()[0]
    cheap_label1=Label(router_window,text=cheap_details)
    cheap_label1.place(x=460,y=180)
    cheap_ship=Label(router_window,text="Shipping And Price Details",foreground="green")
    cheap_ship.place(x=460,y=350)
    cheap_ship_s=cheap_router_spec()[1]
    cheap_ship_d=Label(router_window,text=cheap_ship_s)
    cheap_ship_d.place(x=460,y=380)
    cheap_button=Button(router_window,text="Choose CISCO2811",command=cheap_router_choosed())
    cheap_button.place(x=580,y=630)
    cs2911_url = HTMLLabel(router_window, html="""
            <a href='https://www.router-switch.com/cisco2811-p-180.html'>Checkout The CISCO2811 Page</a>
        """)

    cs2911_url.place(x=500, y=660)



#========= Routers Specs ==========
def expsv_router_spec() :
    try:
        table_MN = pd.read_html('https://www.router-switch.com/cisco2911-hsec-k9-p-5625.html')
        df = table_MN[0]
        df1 = table_MN[1]
        exps_s = [df, df1]
        return exps_s
    except:
        table_MN = pd.read_html('file:///D:/graduationf/web_pages/CISCO2911.html')
        df = table_MN[0]
        df1 = table_MN[1]
        exps_s = [df, df1]
        return exps_s

def cheap_router_spec() :
    try:
        table_MN = pd.read_html('https://www.router-switch.com/cisco2811-p-180.html')
        df=table_MN[0]
        df1 = table_MN[1]
        cheap_s=[df,df1]
        return cheap_s
    except:
        table_MN = pd.read_html('file:///D:/graduationf/web_pages/CISCO2811.html')
        df = table_MN[0]
        df1 = table_MN[1]
        cheap_s = [df, df1]
        return cheap_s



#======= Final result show =====
def show_fin_res():
    fin_res_window=Toplevel(root)
    fin_res_window.title("Final Result")
    fin_res_window.geometry("500x400")
    tables_from_db = cr.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND (name like 'switch48%' OR name like 'switch24%' OR name like 'switch_%')")
    list_of_switches_in_db = [item for t in tables_from_db for item in t]
    i = 0
    switches_label = f"You need {len(list_of_switches_in_db)} switch there details are \n\n"
    dd = " , "
    number_of_24_switches = 0
    number_of_48_switches=0
    router_count=1
    coast=0
    for switch in list_of_switches_in_db:
        ports_c = 0
        deps=[]
        deps_in_switch = cr.execute(f"select distinct department_name from {switch}").fetchall()
        deps = [item for t in deps_in_switch for item in t]
        dd = dd.join(deps)
        dev_count = cr.execute(f"SELECT count(ip) from {switch}")
        if dev_count.fetchone()[0] > 24:
            ports_c = 48
            number_of_24_switches+=1
        else:
            ports_c = 24
            number_of_48_switches += 1

        # expens_or_cheap=expens_or_cheap_list[0]
        # coast=switch_24_price(number_of_24_switches)+router_price(router_count,expens_or_cheap)+((10*coast)/100)+300
        # coast=router_price(router_count,expens_or_cheap)

        switches_label += f"Switch number [{i}] : has {len(deps)} department ({dd}) & needs a {ports_c} port switch \n------------------------------\n" \
                          f"Your Coast Is {coast} $"
        dd = " , "
        i += 1

    f_res_label1=Label(fin_res_window,text=switches_label, anchor="w")
    f_res_label1.grid(sticky="w", column=0,row=0)


#=======Creating the deps entry
first_frame=Frame(root,width=300,height=130,relief="solid")
first_frame.place(x=5,y=10)

#=== number of devices
number_of_dev_label=Label(first_frame,text="Number Of Devices")
number_of_dev_label.place(x=5,y=10)
myvalue2=Entry(first_frame)
myvalue2.place(x=120,y=10)

#====Number of deps entry
number_of_deps_label=Label(first_frame,text="Number Of Deps")
number_of_deps_label.place(x=5,y=40)
myvalue=Entry(first_frame)
myvalue.place(x=120,y=40)

#==== Ok Button
ok_button=Button(first_frame,text="OK",command=creating_entries)
ok_button.place(x=140,y=70)




#==============================
# ====path choosing GUI=========
#==============================
path_frame = Frame(root, width=300, height=200,relief="solid")
path_frame.place(x=320, y=10)

path_label2 = Label(path_frame, text="After Inserting All The Departments Choose A Path \n \n"
                                     "1 - Low Coast Path:Choose the least \nnumber of switches \n\n"
                                     "2 - Expensive & more Extendable Path: \nUse one switch or more for each department.\n"
                                     "Then Hit Path choosed\n")
path_label2.place(x=5, y=5)
path_label = Label(path_frame, text="Type a path 1 or 2")
path_label.place(x=5, y=135)
path_value = Entry(path_frame)
path_value.place(x=120, y=135)
# ===== path choosed button
path_choosed_button = Button(path_frame, text="Choosed Path", command=path_comm)
path_choosed_button.place(x=130, y=165)


#===========================
#====== DHCP Frame ==========
# ==== Create DHCP Frame ====
dhcp_frame = Frame(root, width=300, height=150,relief="solid")
dhcp_frame.place(x=320, y=230)
path_label2 = Label(dhcp_frame, text="Do You Want To Do DHCP Configuration ? \n \n")
path_label2.place(x=5, y=20)
dhcp_entry = Entry(dhcp_frame)
dhcp_entry.place(x=70, y=50)
dhcp_li.append(dhcp_entry)

# ==== DHCP OK ========
dhcp_button = Button(dhcp_frame, text="OK", command=dhcp_conf)
dhcp_button.place(x=120, y=80)



#========================
#=== ACL Frame ==========
#========================
acl_frame = Frame(root, width=550, height=600,relief="solid")
acl_frame.place(x=640, y=10)



#==== ACL ENTRIES AND LABELS ======
#==================================
acl_label = Label(acl_frame, text="Access Control List Section\n"
                                  "1- You can type the acl command fully by your self \n"
                                  "2- Or you can type it step by step\n")
acl_label.place(x=130, y=5)
acl_label2=Label(acl_frame,text="The Acl Format Is : access-list access-list-number {permit|deny} {host|source source-wildcard|any}.\n"
                                "You can get the departments details by clicking (Show Deps Details)")
acl_label2.place(x=10,y=60)

show_dep_for_acl=Button(acl_frame,text="Show Deps Details",command=show_deps_for_acl)
show_dep_for_acl.place(x=220,y=105)

full_acl_label=Label(acl_frame,text="You can type the full acl command here as the format above ")
full_acl_label.place(x=130,y=155)
full_acl_entry = Entry(acl_frame,width=85)
full_acl_entry.place(x=10, y=190)

full_acl_label=Label(acl_frame,text="You can type the acl command here step by step :")
full_acl_label.place(x=10,y=220)

acl_num = Label(acl_frame,text="ACL number")
acl_num.place(x=10,y=250)
acl_num_entry = Entry(acl_frame,width=50)
acl_num_entry.place(x=10, y=270)
acl_pd = Label(acl_frame,text="Permit or deny ? :")
acl_pd.place(x=10,y=310)
pd_entry = Entry(acl_frame,width=50)
pd_entry.place(x=10, y=330)
acl_source = Label(acl_frame,text="Type the source with its wildcard :")
acl_source.place(x=10,y=370)
source_entry = Entry(acl_frame,width=50)
source_entry.place(x=10, y=390)
acl_dist = Label(acl_frame,text="Type the dist with its wildcard :")
acl_dist.place(x=10,y=430)
dist_entry = Entry(acl_frame,width=50)
dist_entry.place(x=10, y=450)
acl_port = Label(acl_frame,text="The port (echo, eq 80 , etc..) :")
acl_port.place(x=10,y=490)
options = [
    "Choose from ports",
    "http : 80",
    "File Transfer Protocol (FTP) : 21",
    "Telnet protocol: 23",
    "Simple Mail Transfer Protocol (SMTP) : 25",
    "Simple File Transfer Protocol (SFTP) : 115",
]

# datatype of menu text
portstr = StringVar()

# initial menu text
portstr.set("Choose from ports")

# Create Dropdown menu
acl_drop = OptionMenu(acl_frame, portstr, *options)
acl_drop.place(x=10,y=510)
# port_entry = Entry(acl_frame,width=50,textvariable=clicked.get())
# port_entry.place(x=10, y=510)


access_ok_button = Button(acl_frame, text="Do The ACL",command=do_acl)
access_ok_button.place(x=120, y=540)
access_reset_button = Button(acl_frame, text="Do Another ACL",command=acl_clear)
access_reset_button.place(x=230, y=540)


#========== Button button===========

router_button = Button(root, text="Choose Routers",command=router_choose)
router_button.place(x=1220, y=10)


show_res_button = Button(root, text="Show Results",command=show_fin_res)
show_res_button.place(x=1220, y=300)

# ===============================
# ==== ACL Enable button ========
acl_button = Button(root, text="Enable ACL", command=acl_enable_fun)
acl_button.place(x=1220, y=130)


dhcp_button = Button(root, text="Enable DHCP", command=dhcp_en_fun)
dhcp_button.place(x=1220, y=190)


def show_graph():
    graph_p=res_directory_path+"/graph.html"
    os.startfile(graph_p)


show_graph_button = Button(root, text="Show Graph", command=show_graph)
show_graph_button.place(x=1220, y=250)


frame_list=[]
#===========================
def show_widgets(x,y,z):
    # This will recover the widget from toplevel
    x.pack()
    y.pack()
    z.pack()
def show_widgets2(x,y,z):
    # This will recover the widget from toplevel
    x.place(x=20,y=70)
    y.place(x=60,y=100)
    z.place(x=150,y=100)
def show_widgets3(x,y,z):
    # This will recover the widget from toplevel
    x.place(x=20,y=130)
    y.place(x=60,y=160)
    z.place(x=150,y=160)


# Button widgets
q1 = Label(routing_tab,text="Work on network protocol?")
q1.place(x=20, y=10)
q1_yes = Button(routing_tab, text="Yes",command=show_widgets2(q1_yes_q2,q1_yes_q2_yes,q1_yes_q2_no))
q1_yes.place(x=60, y=40)
q1_no = Button(routing_tab, text="No",command=route_protocol("eigrp"))
q1_no.place(x=150, y=40)

q1_yes_q2 = Label(routing_tab,text="Is your network small (less than 15 hop)?")
q1_yes_q2_yes = Button(routing_tab, text="Yes",command=lambda:show_widgets3(q1_yes_q2_yes_q3,q1_yes_q2_yes_q3_yes,q1_yes_q2_yes_q3_no))
q1_yes_q2_no = Button(routing_tab, text="No",command=lambda:show_widgets3(q1_yes_q2_no_q3,q1_yes_q2_no_q3_yes,q1_yes_q2_no_q3_no))


q1_yes_q2_yes_q3 = Label(routing_tab,text="Is the network expendable And need reliability?")
q1_yes_q2_yes_q3_yes = Button(routing_tab, text="Yes",command=route_protocol("eigrp"))
q1_yes_q2_yes_q3_no = Button(routing_tab, text="No",command=route_protocol("rip"))



q1_yes_q2_no_q3 = Label(routing_tab,text="Does lower convergance time over resources consumption matter?")
q1_yes_q2_no_q3_yes = Button(routing_tab, text="Yes",command=route_protocol("eigrp"))
q1_yes_q2_no_q3_no = Button(routing_tab, text="No",command=route_protocol("ospf"))

exp_title = Label(routing_tab, text=f"Routing Protocol will be {protocol}", foreground="green",
                  font=('Sans', '10', 'bold'))



def exp_sys_routing():
    #==============
    tabControl.select(routing_tab)

ex_sys_button = Button(root, text="Routing protocol",command=exp_sys_routing)
ex_sys_button.place(x=1220, y=70)

#======== Disabling Frames
for child in acl_frame.winfo_children():
            child.configure(state='disabled')

for child in path_frame.winfo_children():
            child.configure(state='disabled')

for child in dhcp_frame.winfo_children():
            child.configure(state='disabled')


ro.mainloop()

db.commit()
cr.close()
db.close()
#
#
# engin = protocol_engine()
# engin.reset()
# engin.run()
# protocol=engin.protocolo
# #==== Typing routing protocol =====
# route_protocol(protocol)
