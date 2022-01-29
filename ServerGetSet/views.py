from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
import subprocess
import re
from SnmpDatabase.models import SnmpDevices #tablo

# Create your views here.

def snmpget(request):

    if request.method == 'POST':
        try:
            ip = request.POST['ip']
            type = request.POST['type']
            community = request.POST['community']

            if type == "All":

                context = {
                    "result": {"System Name": " ", "System Description": " ", "System UpTime": " ", "System Contact": " ", "System Location": " ", "System Date": " ", "System Num Users": " ", "Total Free Memory": " "},
                    "targetIP": ip
                }

                def all(type):
                    get = subprocess.check_output(f"snmpget -v 2c -c {community} {ip} {type}", shell=True).decode("utf-8")
                    return str(re.search(r"(?<=: ).+",get).group(0))

                def InterfaceInfo(value, name):
                    x = 1
                    while x <= 28:
                        try:
                            context["result"][f"Interface {name} {x}"] = all(f"1.3.6.1.2.1.2.2.1.{value}.{x}")
                        except:
                            break
                        finally:
                            x = x + 1
                
                context["result"]["System Name"] = all("1.3.6.1.2.1.1.5.0")
                context["result"]["System Description"] = all("1.3.6.1.2.1.1.1.0")
                context["result"]["System UpTime"] = all("1.3.6.1.2.1.1.3.0")
                context["result"]["System Contact"] = all("1.3.6.1.2.1.1.4.0")
                context["result"]["System Location"] = all("1.3.6.1.2.1.1.6.0")
                context["result"]["System Date"] = all("1.3.6.1.2.1.25.1.2.0")
                context["result"]["System Num Users"] = all("1.3.6.1.2.1.25.1.5.0")
                context["result"]["Total Free Memory"] = all("1.3.6.1.4.1.2021.4.11.0")
                InterfaceInfo(1,"Index")
                InterfaceInfo(2,"Description")
                InterfaceInfo(3,"Type")
                InterfaceInfo(4,"MTU")
                InterfaceInfo(5,"Speed")
                InterfaceInfo(6,"Physical Address")
                InterfaceInfo(7,"Admin Status")
                InterfaceInfo(8,"Oper Status")
                InterfaceInfo(9,"Last Change")
                
                return render(request, "pages/snmpget.html", context)
                
            else:

                context = {
                    "result": {},
                    "targetIP": ip
                }

                def SnmpGet(type):
                    get = subprocess.check_output(f"snmpget -v 2c -c {community} {ip} {type}", shell=True).decode("utf-8")
                    regular = re.search(r"(?<=: ).+",get).group(0)
                    return regular
                
                def InterfaceInfo(value, name):
                    x = 1
                    while x <= 28:
                        try:
                            context["result"][f"Interface {name} {x}"] = SnmpGet(f"1.3.6.1.2.1.2.2.1.{value}.{x}")
                        except:
                            break
                        finally:
                            x = x + 1

                if type == "1.3.6.1.2.1.1.5.0":
                    context["result"]["System Name"] = SnmpGet("1.3.6.1.2.1.1.5.0")
                if type == "1.3.6.1.2.1.1.1.0":
                    context["result"]["System Description"] = SnmpGet("1.3.6.1.2.1.1.1.0")
                if type == "1.3.6.1.2.1.1.3.0":
                    context["result"]["System UpTime"] = SnmpGet("1.3.6.1.2.1.1.3.0")
                if type == "1.3.6.1.2.1.1.4.0":
                    context["result"]["System Contact"] = SnmpGet("1.3.6.1.2.1.1.4.0")
                if type == "1.3.6.1.2.1.1.6.0":
                    context["result"]["System Location"] = SnmpGet("1.3.6.1.2.1.1.6.0")
                if type == "1.3.6.1.2.1.25.1.2.0":
                    context["result"]["System Date"] = SnmpGet("1.3.6.1.2.1.25.1.2.0")
                if type == "1.3.6.1.2.1.25.1.5.0":
                    context["result"]["System Num Users"] = SnmpGet("1.3.6.1.2.1.25.1.5.0")
                if type == "1.3.6.1.4.1.2021.4.11.0":
                    context["result"]["Total Free Memory"] = SnmpGet("1.3.6.1.4.1.2021.4.11.0")
                if type == "1.3.6.1.2.1.2.2.1.1":
                    InterfaceInfo(1,"Index")
                if type == "1.3.6.1.2.1.2.2.1.2":
                    InterfaceInfo(2,"Description")
                if type == "1.3.6.1.2.1.2.2.1.3":
                    InterfaceInfo(3,"Type")
                if type == "1.3.6.1.2.1.2.2.1.4":
                    InterfaceInfo(4,"MTU")
                if type == "1.3.6.1.2.1.2.2.1.5":
                    InterfaceInfo(5,"Speed")
                if type == "1.3.6.1.2.1.2.2.1.6":
                    InterfaceInfo(6,"Physical Address")
                if type == "1.3.6.1.2.1.2.2.1.7":
                    InterfaceInfo(7,"Admin Status")
                if type == "1.3.6.1.2.1.2.2.1.8":
                    InterfaceInfo(8,"Oper Status")
                if type == "1.3.6.1.2.1.2.2.1.9":
                    InterfaceInfo(9,"Last Change")
                

                return render(request, "pages/snmpget.html", context)
        except:
            messages.add_message(
                        request, messages.WARNING, "Bir hata oluştu.")
            return redirect('snmpget')

    else:
        return render(request, "pages/snmpget.html")

def snmpset(request):
    if request.method == 'POST':
        try:
            ip = request.POST['ip']
            type = request.POST['type']
            #community = request.POST['community']
            newvalue = request.POST['newvalue']

            set = subprocess.check_output(f"snmpset -v 2c -c public {ip} {type} s {newvalue}", shell=True).decode("utf-8")
            regular = re.search(r"(?<=: ).+",set)

            try:
                if type == "sysName.0":
                    SnmpDevices.objects.filter(Device_Ip=ip).update(System_Name=newvalue)
                if type == "sysContact.0":
                    SnmpDevices.objects.filter(Device_Ip=ip).update(System_Contact=newvalue)
                if type == "sysLocation.0":
                    SnmpDevices.objects.filter(Device_Ip=ip).update(System_Location=newvalue)
            except:
                pass

            context = {
                "result": regular.group(0),
                "targetIP": ip
            }

            return render(request, "pages/snmpset.html", context)
        except:
            messages.add_message(
                        request, messages.WARNING, "Bir hata oluştu.")
            return redirect('snmpset')
        
    else:
        return render(request, "pages/snmpset.html")
