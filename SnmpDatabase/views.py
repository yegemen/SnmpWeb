from django.shortcuts import render, redirect
import subprocess
from django.contrib import messages
from .models import SnmpDevices #tablo
import re

# Create your views here.



def deviceadd(request):
    if request.method == 'POST':
        try:
            global ip, get1, get2, get3, get4, get5
            ip = request.POST['ip']
            community = request.POST['community']

            def deviceinfo(type):
                get = subprocess.check_output(f"snmpget -v 2c -c {community} {ip} {type}", shell=True).decode("utf-8")
                return str(re.search(r"(?<=: ).+",get).group(0))

            get1 = deviceinfo("1.3.6.1.2.1.1.5.0") # name
            get2 = deviceinfo("1.3.6.1.2.1.1.1.0") # description
            get3 = request.POST['community']
            get4 = deviceinfo("1.3.6.1.2.1.1.4.0")
            get5 = deviceinfo("1.3.6.1.2.1.1.6.0")

            context = {
                "result": {"System Name": f"{get1}", "System Description": f"{get2}", "System Contact": f"{get4}", "System Location": f"{get5}", "Community": f"{get3}"},
                "targetIP": ip
            }
        
            return render(request, "pages/deviceaddconf.html", context)
        except:
            messages.add_message(
                        request, messages.WARNING, "Bir hata oluştu.")
            return redirect('deviceadd')

    else:
        return render(request, "pages/deviceadd.html")

def deviceaddconf(request):
    if request.method == 'POST':
        select = request.POST['select']

        if select == 'Evet':
            current_user = request.user  # oturum açan kullanıcı bilgisi.
            SnmpDevices.objects.create(Device_Ip=ip, System_Name=get1, System_Description=get2, Community=get3, System_Contact=get4, System_Location=get5, User_id=current_user.id)  # veritabanı kayıt
            messages.add_message(
                        request, messages.WARNING, "Eklendi !")
            return redirect('deviceadd')
        else:
            messages.add_message(
                        request, messages.WARNING, "Eklenmedi.")
            return redirect('deviceadd')
    
    else:
        return render(request, "pages/deviceaddconf.html")

def devicesaved(request):
    if request.method == "POST":
        ip = request.POST['silinecek']
        SnmpDevices.objects.filter(Device_Ip=ip).delete()

        current_user = request.user
        saveddevice = SnmpDevices.objects.filter(User_id=current_user.id)
        context = {
            'saveddevice': saveddevice
        }
        return render(request, "pages/devicesaved.html", context)

    else:
        current_user = request.user
        # tabloadi.object ile objelere ulaşılır
        # giriş yapan kullanıcının tarama sonuçları
        saveddevice = SnmpDevices.objects.filter(User_id=current_user.id)
        context = {
            'saveddevice': saveddevice
        }
        return render(request, "pages/devicesaved.html", context)

def collectiveget(request):
    if request.method == "POST":
        try:
            type = request.POST['type']
            ip_list = request.POST.getlist('ip')
            print(ip_list)
            current_user = request.user
            saveddevice = SnmpDevices.objects.filter(User_id=current_user.id) 

            if type == "All":
                context = {
                    'saveddevice': saveddevice,
                    "ipaddress": ip_list,
                    "result": {},
                }

                def all(ip, type):
                    community = SnmpDevices.objects.values_list('Community', flat=True).filter(Device_Ip=ip)
                    get = subprocess.check_output(f"snmpget -v 2c -c {community[0]} {ip} {type}", shell=True).decode("utf-8")
                    return str(re.search(r"(?<=: ).+",get).group(0))

                def InterfaceInfo(ip, value, name):
                    x = 1
                    while x <= 28:
                        try:
                            context["result"][f"{ip} - Interface {name} {x}"] = all(ip, f"1.3.6.1.2.1.2.2.1.{value}.{x}")
                        except:
                            break
                        finally:
                            x = x + 1
                
                for ip in ip_list:
                    context["result"][f"{ip} - System Name"] = all(ip, "1.3.6.1.2.1.1.5.0")
                    context["result"][f"{ip} - System Description"] = all(ip, "1.3.6.1.2.1.1.1.0")
                    context["result"][f"{ip} - System UpTime"] = all(ip, "1.3.6.1.2.1.1.3.0")
                    context["result"][f"{ip} - System Contact"] = all(ip, "1.3.6.1.2.1.1.4.0")
                    context["result"][f"{ip} - System Location"] = all(ip, "1.3.6.1.2.1.1.6.0")
                    context["result"][f"{ip} - System Date"] = all(ip, "1.3.6.1.2.1.25.1.2.0")
                    context["result"][f"{ip} - System Num Users"] = all(ip, "1.3.6.1.2.1.25.1.5.0")
                    context["result"][f"{ip} - Total Free Memory"] = all(ip, "1.3.6.1.4.1.2021.4.11.0")
                    InterfaceInfo(ip, 1,"Index")
                    InterfaceInfo(ip, 2,"Description")
                    InterfaceInfo(ip, 3,"Type")
                    InterfaceInfo(ip, 4,"MTU")
                    InterfaceInfo(ip, 5,"Speed")
                    InterfaceInfo(ip, 6,"Physical Address")
                    InterfaceInfo(ip, 7,"Admin Status")
                    InterfaceInfo(ip, 8,"Oper Status")
                    InterfaceInfo(ip, 9,"Last Change")

                return render(request, "pages/collectiveget.html",context)

            else:
                context = {
                        'saveddevice': saveddevice,
                        'ipaddress': ip_list,
                        "result": {},
                    }

                def SnmpGet(ip, type):
                        community = SnmpDevices.objects.values_list('Community', flat=True).filter(Device_Ip=ip)
                        get = subprocess.check_output(f"snmpget -v 2c -c {community[0]} {ip} {type}", shell=True).decode("utf-8")
                        regular = re.search(r"(?<=: ).+",get).group(0)
                        return regular
                    
                def InterfaceInfo(ip, value, name):
                        x = 1
                        while x <= 28:
                            try:
                                context["result"][f"{ip} - Interface {name} {x}"] = SnmpGet(ip, f"1.3.6.1.2.1.2.2.1.{value}.{x}")
                            except:
                                break
                            finally:
                                x = x + 1
                
                for ip in ip_list:
                    if type == "1.3.6.1.2.1.1.5.0":
                        context["result"][f"{ip} - System Name"] = SnmpGet(ip, "1.3.6.1.2.1.1.5.0")
                    if type == "1.3.6.1.2.1.1.1.0":
                        context["result"][f"{ip} - System Description"] = SnmpGet(ip, "1.3.6.1.2.1.1.1.0")
                    if type == "1.3.6.1.2.1.1.3.0":
                        context["result"][f"{ip} - System UpTime"] = SnmpGet(ip, "1.3.6.1.2.1.1.3.0")
                    if type == "1.3.6.1.2.1.1.4.0":
                        context["result"][f"{ip} - System Contact"] = SnmpGet(ip, "1.3.6.1.2.1.1.4.0")
                    if type == "1.3.6.1.2.1.1.6.0":
                        context["result"][f"{ip} - System Location"] = SnmpGet(ip, "1.3.6.1.2.1.1.6.0")
                    if type == "1.3.6.1.2.1.25.1.2.0":
                        context["result"][f"{ip} - System Date"] = SnmpGet("1.3.6.1.2.1.25.1.2.0")
                    if type == "1.3.6.1.2.1.25.1.5.0":
                        context["result"][f"{ip} - System Num Users"] = SnmpGet("1.3.6.1.2.1.25.1.5.0")
                    if type == "1.3.6.1.4.1.2021.4.11.0":
                        context["result"][f"{ip} - Total Free Memory"] = SnmpGet("1.3.6.1.4.1.2021.4.11.0")
                    if type == "1.3.6.1.2.1.2.2.1.1":
                        InterfaceInfo(ip, 1,"Index")
                    if type == "1.3.6.1.2.1.2.2.1.2":
                        InterfaceInfo(ip, 2,"Description")
                    if type == "1.3.6.1.2.1.2.2.1.3":
                        InterfaceInfo(ip, 3,"Type")
                    if type == "1.3.6.1.2.1.2.2.1.4":
                        InterfaceInfo(ip, 4,"MTU")
                    if type == "1.3.6.1.2.1.2.2.1.5":
                        InterfaceInfo(ip, 5,"Speed")
                    if type == "1.3.6.1.2.1.2.2.1.6":
                        InterfaceInfo(ip, 6,"Physical Address")
                    if type == "1.3.6.1.2.1.2.2.1.7":
                        InterfaceInfo(ip, 7,"Admin Status")
                    if type == "1.3.6.1.2.1.2.2.1.8":
                        InterfaceInfo(ip, 8,"Oper Status")
                    if type == "1.3.6.1.2.1.2.2.1.9":
                        InterfaceInfo(ip, 9,"Last Change")

                return render(request, "pages/collectiveget.html",context)
        except:
            messages.add_message(
                        request, messages.WARNING, "Bir hata oluştu.")
            return redirect('collectiveget')   

    else:
        current_user = request.user
        saveddevice = SnmpDevices.objects.filter(User_id=current_user.id)

        context = {
                'saveddevice': saveddevice
            }
        return render(request, "pages/collectiveget.html",context)

def collectiveset(request):
    if request.method == "POST":
        try:
            ip_list = request.POST.getlist('ip')
            type = request.POST['type']
            newvalue = request.POST['newvalue']
            print(ip_list)
            current_user = request.user
            saveddevice = SnmpDevices.objects.filter(User_id=current_user.id)

            context = {
                    'saveddevice': saveddevice,
                    "targetIP": [],
                    "success": f"Belirtilen IP'lerdeki Değerler Değiştirilmiştir."
                }

            for ip in ip_list:
                subprocess.check_output(f"snmpset -v 2c -c public {ip} {type} s {newvalue}", shell=True)
                context["targetIP"].append(ip)
                if type == "sysName.0":
                    SnmpDevices.objects.filter(Device_Ip=ip).update(System_Name=newvalue)
                if type == "sysContact.0":
                    SnmpDevices.objects.filter(Device_Ip=ip).update(System_Contact=newvalue)
                if type == "sysLocation.0":
                    SnmpDevices.objects.filter(Device_Ip=ip).update(System_Location=newvalue)
            

            return render(request, "pages/collectiveset.html",context)
        except:
            messages.add_message(
                        request, messages.WARNING, "Bir hata oluştu.")
            return redirect('collectiveset')

    else:
        current_user = request.user
        saveddevice = SnmpDevices.objects.filter(User_id=current_user.id)

        context = {
                'saveddevice': saveddevice
            }
        return render(request, "pages/collectiveset.html",context)
