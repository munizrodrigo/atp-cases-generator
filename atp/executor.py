import os
import mmap
import struct
import pandas
import numpy

from copy import deepcopy as copy


class ATPExecutor(object):
    """
    Classe responsavel pelas execucoes do ATP, leitura das saidas e execucao de programas correlatos.
    """
    def __init__(self):
        pass

    @staticmethod
    def execute_atp(folder_path, atp_filename, execution_cmd):
        if not atp_filename[-4:] == ".atp":
            atp_filename += ".atp"
        complete_filename = os.path.join(folder_path, atp_filename)
        os.system(execution_cmd + " " + complete_filename + " >nul")

    @staticmethod
    def read_pl4(pl4_file):
        misc_data = {
            "deltat": 0.0,
            "n_var": 0,
            "pl4_size": 0,
            "steps": 0,
            "tmax": 0.0
        }

        # Open binary file for reading
        with open(pl4_file, "rb") as f:
            pl4 = mmap.mmap(fileno=f.fileno(), length=0, access=mmap.ACCESS_READ)

            # Read DELTAT
            misc_data["deltat"] = struct.unpack("<f", pl4[40:44])[0]

            # Read number of variables
            misc_data["n_var"] = int(struct.unpack("<L", pl4[48:52])[0] / 2)

            # Read PL4 used disk size
            misc_data["pl4_size"] = struct.unpack("<L", pl4[56:60])[0] - 1

            # Calculate the number of simulation steps from the PL4 file size
            misc_data["steps"] = int(
                (misc_data["pl4_size"] - 5 * 16 - misc_data["n_var"] * 16) / ((misc_data["n_var"] + 1) * 4)
            )

            # Calculate tmax from steps and deltat
            misc_data["tmax"] = (misc_data["steps"] - 1) * misc_data["deltat"]

            # Generate pandas dataframe	to store the header
            header_df = pandas.DataFrame()
            header_df["type"] = ""
            header_df["from"] = ""
            header_df["to"] = ""

            for i in range(0, misc_data["n_var"]):
                pos = 5 * 16 + i * 16
                h = struct.unpack("3x1c6s6s", pl4[pos:pos + 16])
                header_df = header_df.append({"type": int(h[0]), "from": h[1], "to": h[2]}, ignore_index=True)

            # Check for unexpected rows of zeroes
            exp_size = (5 + misc_data["n_var"]) * 16 + misc_data["steps"] * (misc_data["n_var"] + 1) * 4
            null_bytes = 0
            if misc_data["pl4_size"] > exp_size:
                null_bytes = misc_data["pl4_size"] - exp_size

            # read and store actual data, map it to a numpy read only array
            data = numpy.memmap(
                filename=pl4_file,
                dtype=numpy.float32,
                mode="r",
                shape=(misc_data["steps"], misc_data["n_var"] + 1),
                offset=(5 + misc_data["n_var"]) * 16 + null_bytes
            )

            header_df["type"] = header_df["type"].apply(lambda x: "V-node" if x == 4 else x)
            header_df["type"] = header_df["type"].apply(lambda x: "E-bran" if x == 7 else x)
            header_df["type"] = header_df["type"].apply(lambda x: "V-bran" if x == 8 else x)
            header_df["type"] = header_df["type"].apply(lambda x: "I-bran" if x == 9 else x)

            output = {
                "misc": misc_data,
                "time": data[:, 0],
                "v_node": {},
                "e_bran": {},
                "v_bran": {},
                "i_bran": {}
            }
            for index, row in header_df.iterrows():
                key_tuple = (row["from"].decode().strip(), row["to"].decode().strip())
                if row["type"] == "V-node":
                    output["v_node"][key_tuple] = data[:, index + 1]
                elif row["type"] == "E-bran":
                    output["e_bran"][key_tuple] = data[:, index + 1]
                elif row["type"] == "V-bran":
                    output["v_bran"][key_tuple] = data[:, index + 1]
                elif row["type"] == "I-bran":
                    output["i_bran"][key_tuple] = data[:, index + 1]

            return copy(output)
