from re import sub as remove_spaces

from input.convert_dict_types import convert_dict_types


def read_input(input_file):
    input_file_rows = input_file.readlines()
    input_file_lines = []
    for (row_number, row_value) in enumerate(input_file_rows):
        row_value = row_value.strip()
        row_value = remove_spaces(" +", " ", row_value)
        if not len(row_value) == 0:
            if not row_value.startswith("##"):
                input_file_lines.append(row_value)
    return input_file_lines


def define_feeder(input_file_lines):
    feeder_lines = []
    is_feeder = False
    for line in input_file_lines:
        if "END" in line and is_feeder:
            break
        if "START" not in line and is_feeder:
            feeder_lines.append(line)
        if "FEEDER" in line:
            is_feeder = True
    feeder_dict = {}
    for line in feeder_lines:
        (code, vrms) = tuple(line.split(","))
        feeder_dict[str(code).strip()] = {
            "vrms": str(vrms).strip()
        }
    return feeder_dict


def define_bus(input_file_lines):
    bus_lines = []
    is_bus = False
    for line in input_file_lines:
        if "END" in line and is_bus:
            break
        if "START" not in line and is_bus:
            bus_lines.append(line)
        if "BUS" in line:
            is_bus = True
    bus_dict = {}
    for line in bus_lines:
        (bus, x, y) = tuple(line.split(","))
        bus_dict[str(bus).strip()] = {
            "x": str(x).strip(),
            "y": str(y).strip()
        }
    return bus_dict


def define_branch(input_file_lines):
    branch_lines = []
    is_branch = False
    for line in input_file_lines:
        if "END" in line and is_branch:
            break
        if "START" not in line and is_branch:
            branch_lines.append(line)
        if "BRANCH" in line:
            is_branch = True
    branch_dict = {}
    for line in branch_lines:
        (code, bus_from, bus_to, length, phase, cable, pole) = tuple(line.split(","))
        branch_dict[str(code).strip()] = {
            "from": str(bus_from).strip(),
            "to": str(bus_to).strip(),
            "length": str(length).strip(),
            "phase": str(phase).strip(),
            "cable": str(cable).strip(),
            "pole": str(pole).strip()
        }
    return branch_dict


def define_source(input_file_lines):
    source_lines = []
    is_source = False
    for line in input_file_lines:
        if "END" in line and is_source:
            break
        if "START" not in line and is_source:
            source_lines.append(line)
        if "SOURCE" in line:
            is_source = True
    source_dict = {}
    for line in source_lines:
        (code, bus, vrms, frequency, phase) = tuple(line.split(","))
        source_dict[str(code).strip()] = {
            "bus": str(bus).strip(),
            "vrms": str(vrms).strip(),
            "frequency": str(frequency).strip(),
            "phase": str(phase).strip()
        }
    return source_dict


def define_load(input_file_lines):
    load_lines = []
    is_load = False
    for line in input_file_lines:
        if "END" in line and is_load:
            break
        if "START" not in line and is_load:
            load_lines.append(line)
        if "LOAD" in line:
            is_load = True
    load_dict = {}
    for line in load_lines:
        (code, bus, phase, s, fp, ra, rb, rc, la, lb, lc) = tuple(line.split(","))
        load_dict[str(code).strip()] = {
            "bus": str(bus).strip(),
            "phase": str(phase).strip(),
            "s": str(s).strip(),
            "fp": str(fp).strip(),
            "ra": str(ra).strip(),
            "rb": str(rb).strip(),
            "rc": str(rc).strip(),
            "la": str(la).strip(),
            "lb": str(lb).strip(),
            "lc": str(lc).strip(),
        }
    return load_dict


def define_capacitor(input_file_lines):
    capacitor_lines = []
    is_capacitor = False
    for line in input_file_lines:
        if "END" in line and is_capacitor:
            break
        if "START" not in line and is_capacitor:
            capacitor_lines.append(line)
        if "CAPACITOR" in line:
            is_capacitor = True
    capacitor_dict = {}
    for line in capacitor_lines:
        (code, bus, phase, q, ca, cb, cc) = tuple(line.split(","))
        capacitor_dict[str(code).strip()] = {
            "bus": str(bus).strip(),
            "phase": str(phase).strip(),
            "q": str(q).strip(),
            "ca": str(ca).strip(),
            "cb": str(cb).strip(),
            "cc": str(cc).strip()
        }
    return capacitor_dict


def define_switch(input_file_lines):
    switch_lines = []
    is_switch = False
    for line in input_file_lines:
        if "END" in line and is_switch:
            break
        if "START" not in line and is_switch:
            switch_lines.append(line)
        if "SWITCH" in line:
            is_switch = True
    switch_dict = {}
    for line in switch_lines:
        (code, bus_from, bus_to, tclose, topen) = tuple(line.split(","))
        switch_dict[str(code).strip()] = {
            "from": str(bus_from).strip(),
            "to": str(bus_to).strip(),
            "tclose": str(tclose).strip(),
            "topen": str(topen).strip()
        }
    return switch_dict


def define_pole(input_file_lines):
    pole_lines = []
    is_pole = False
    for line in input_file_lines:
        if "END" in line and is_pole:
            break
        if "START" not in line and is_pole:
            pole_lines.append(line)
        if "POLE" in line:
            is_pole = True
    pole_dict = {}
    for line in pole_lines:
        (code, bus, distance, height, sag) = tuple(line.split(","))
        if not str(code).strip() in pole_dict:
            pole_dict[str(code).strip()] = {
                "phase": [str(bus).strip()],
                "distance": [str(distance).strip()],
                "height": [str(height).strip()],
                "sag": [str(sag).strip()]
            }
        else:
            pole_dict[str(code).strip()]["phase"].append(str(bus).strip())
            pole_dict[str(code).strip()]["distance"].append(str(distance).strip())
            pole_dict[str(code).strip()]["height"].append(str(height).strip())
            pole_dict[str(code).strip()]["sag"].append(str(sag).strip())
    return pole_dict


def define_cable(input_file_lines):
    cable_lines = []
    is_cable = False
    for line in input_file_lines:
        if "END" in line and is_cable:
            break
        if "START" not in line and is_cable:
            cable_lines.append(line)
        if "CABLE" in line:
            is_cable = True
    cable_dict = {}
    for line in cable_lines:
        (code, ri, ro, resistivity) = tuple(line.split(","))
        cable_dict[str(code).strip()] = {
            "ri": str(ri).strip(),
            "ro": str(ro).strip(),
            "resistivity": str(resistivity).strip()
        }
    return cable_dict


def define_surge_arrester(input_file_lines):
    surge_arrester_lines = []
    is_surge_arrester = False
    for line in input_file_lines:
        if "END" in line and is_surge_arrester:
            break
        if "START" not in line and is_surge_arrester:
            surge_arrester_lines.append(line)
        if "SURGE ARRESTER" in line:
            is_surge_arrester = True
    surge_arrester_dict = {}
    for line in surge_arrester_lines:
        (code, bus) = tuple(line.split(","))
        surge_arrester_dict[str(code).strip()] = {
            "bus": str(bus).strip()
        }
    return surge_arrester_dict


def define_surge(input_file_lines):
    surge_lines = []
    is_surge = False
    for line in input_file_lines:
        if "END" in line and is_surge:
            break
        if "START" not in line and is_surge:
            surge_lines.append(line)
        if "SURGE" in line and "ARRESTER" not in line:
            is_surge = True
    surge_dict = {}
    for line in surge_lines:
        (code, bus, amp, tfront, tau) = tuple(line.split(","))
        surge_dict[str(code).strip()] = {
            "bus": str(bus).strip(),
            "amp": str(amp).strip(),
            "tfront": str(tfront).strip(),
            "tau": str(tau).strip()
        }
    return surge_dict


def define_input_dict(input_file):
    input_file_lines = read_input(input_file)
    input_dict = {
        "feeder": define_feeder(input_file_lines),
        "bus": define_bus(input_file_lines),
        "branch": define_branch(input_file_lines),
        "source": define_source(input_file_lines),
        "load": define_load(input_file_lines),
        "capacitor": define_capacitor(input_file_lines),
        "switch": define_switch(input_file_lines),
        "pole": define_pole(input_file_lines),
        "cable": define_cable(input_file_lines),
        "surge_arrester": define_surge_arrester(input_file_lines),
        "surge": define_surge(input_file_lines)
    }
    input_dict = convert_dict_types(input_dict=input_dict)
    return input_dict
