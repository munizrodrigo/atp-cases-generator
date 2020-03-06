import sys

import winreg as reg


key = reg.OpenKey(
    reg.HKEY_LOCAL_MACHINE,
    r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
    0,
    reg.KEY_ALL_ACCESS
)

try:
    value, _ = reg.QueryValueEx(key, "PATH")
except WindowsError:
    value = ""

value = list(value.split(";"))
if "" in value:
    value.remove("")

if sys.argv[1] == "-a" and not sys.argv[2] in value:
    value.append(sys.argv[2])
elif sys.argv[1] == "-r":
    var_to_remove = []
    for var in value:
        if sys.argv[2] in var:
            var_to_remove.append(var)
    for var in var_to_remove:
        value.remove(var)

value = ";".join(value)

reg.SetValueEx(key, 'PATH', 0, reg.REG_EXPAND_SZ, value)
reg.CloseKey(key)
