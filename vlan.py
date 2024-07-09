vlan = int(input("Ingrese número de VLAN: "))

if 1 <= vlan <= 1005:
    print("Es una VLAN normal")
elif 1006 <= vlan <= 4094:
    print("Es una VLAN normal")
else:
    print("VLAN no válida")
