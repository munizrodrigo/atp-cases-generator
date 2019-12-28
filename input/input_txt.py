from re import sub as remove_spaces


def read_input(input_file):
    input_file_rows = input_file.readlines()
    input_file_lines = []
    for (row_number, row_value) in enumerate(input_file_rows):
        row_value = row_value.strip()
        row_value = remove_spaces(" +", " ", row_value)
        if not len(row_value) == 0:
            if not row_value[0] == "#":
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
            "vrms": float(str(vrms).strip())
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
            "x": float(str(x).strip()),
            "y": float(str(y).strip())
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
            "length": float(str(length).strip()),
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
            "vrms": float(str(vrms).strip()),
            "frequency": float(str(frequency).strip()),
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
            "s": float(str(s).strip()),
            "fp": float(str(fp).strip()),
            "ra": float(str(ra).strip()),
            "rb": float(str(rb).strip()),
            "rc": float(str(rc).strip()),
            "la": float(str(la).strip()),
            "lb": float(str(lb).strip()),
            "lc": float(str(lc).strip()),
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
            "q": float(str(q).strip()),
            "ca": float(str(ca).strip()),
            "cb": float(str(cb).strip()),
            "cc": float(str(cc).strip())
        }
    return capacitor_dict


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
        pole_dict[str(code).strip()] = {
            "bus": str(bus).strip(),
            "distance": float(str(distance).strip()),
            "height": float(str(height).strip()),
            "sag": float(str(sag).strip())
        }
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
            "ri": float(str(ri).strip()),
            "ro": float(str(ro).strip()),
            "resistivity": float(str(resistivity).strip())
        }
    return cable_dict


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
            "amp": float(str(amp).strip()),
            "tfront": float(str(tfront).strip()),
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
        "surge_arrester": define_surge_arrester(input_file_lines),
        "pole": define_pole(input_file_lines),
        "cable": define_cable(input_file_lines),
        "surge": define_surge(input_file_lines)
    }
    return input_dict
