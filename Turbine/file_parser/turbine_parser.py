from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
# from builtins import str
from builtins import range
import io
import sys

from Turbine.graph_classe.csdf import CSDF
from Turbine.graph_classe.pcg import PCG
from Turbine.graph_classe.sdf import SDF


def write_tur(dataflow):
    output = io.StringIO()

    output.write(u"#Graph_name\n")
    output.write(dataflow.get_name() + u" " + dataflow.get_dataflow_type() + u"\n")

    output.write(u"#Number_of_tasks number_of_arcs\n")
    output.write(str(dataflow.get_task_count()) + u" " + str(dataflow.get_arc_count()) + u"\n")

    output.write(u"#TASKS\n")
    output.write(u"#Id repetition_factor phase_duration\n")
    for task in dataflow.get_task_list():
        output.write(str(task) + u" " + str(dataflow.get_repetition_factor(task)) + u" ")
        output.write(dataflow.get_duration_str(task) + u"\n")

    output.write(u"#ARCS\n")
    output.write(u"#(source,target) initial_marking production_vector consumption_vector\n")
    for arc in dataflow.get_arc_list():
        str_arc = str(arc).split(",")[0] + u"," + str(arc).split(",")[1] + u")"
        output.write(str_arc.replace(u" ", u"") + u" ")
        output.write(str(int(dataflow.get_initial_marking(arc))) + u" ")
        output.write(dataflow.get_prod_str(arc) + u" ")
        output.write(dataflow.get_cons_str(arc) + u"\n")
    r = output.getvalue()
    output.close()
    return r


def write_tur_file(dataflow, filename):
    output = write_tur(dataflow)
    open_file = sys.stdout
    if filename is not None:
        open_file = open(filename, "w")
    open_file.write(output)
    open_file.close()


def read_tur_file(filename):
    open_file = open(filename, "r")
    name, dataflow_type = __readline(open_file).replace("\n", "").split(" ")
    if dataflow_type == "SDF" or dataflow_type == "SDFG":
        dataflow = SDF(name)
    elif dataflow_type == "CSDF" or dataflow_type == "CSDFG":
        dataflow = CSDF(name)
    elif dataflow_type == "PCG":
        dataflow = PCG(name)

    task_nb, arc_nb = __readline(open_file).split(" ")
    for i in range(int(task_nb)):
        line = __readline(open_file).replace("\n", "")
        task_name, repetition_factor, str_duration = line.split(" ")
        task = dataflow.add_task(task_name)
        dataflow.set_repetition_factor(task, int(repetition_factor))
        if ";" in str_duration:
            str_ini_duration, str_duration = str_duration.split(";")
            ini_duration_list = [float(i) for i in str_ini_duration.split(",")]
            dataflow.set_ini_phase_count(task, len(ini_duration_list))
            dataflow.set_ini_phase_duration_list(task, ini_duration_list)

        duration_list = [float(i) for i in str_duration.split(",")]
        if isinstance(dataflow, SDF):
            dataflow.set_task_duration(task, duration_list[0])
        if isinstance(dataflow, CSDF):
            dataflow.set_phase_count(task, len(duration_list))
            dataflow.set_phase_duration_list(task, duration_list)

    for i in range(int(arc_nb)):
        line = __readline(open_file).replace("\n", "")
        str_arc, str_m0, str_prod, str_cons = line.split(" ")
        source = dataflow.get_task_by_name(str_arc.split(",")[0][1:])
        target = dataflow.get_task_by_name(str_arc.split(",")[1][:-1])
        m0 = int(str_m0)
        arc = dataflow.add_arc(source, target)
        dataflow.set_initial_marking(arc, m0)

        if "PCG" in dataflow_type:
            if dataflow.get_ini_phase_count(source) == 0:
                dataflow.set_ini_prod_rate_list(arc, [])
            if dataflow.get_ini_phase_count(target) == 0:
                dataflow.set_ini_cons_rate_list(arc, [])
                dataflow.set_ini_threshold_list(arc, [])

        if ";" in str_prod:
            str_prod_ini, str_prod = str_prod.split(";")
            prod_ini = [int(i) for i in str_prod_ini.split(",")]
            dataflow.set_ini_prod_rate_list(arc, prod_ini)

        prod = [int(i) for i in str_prod.split(",")]
        if isinstance(dataflow, SDF):
            dataflow.set_prod_rate(arc, prod[0])
        if isinstance(dataflow, CSDF):
            dataflow.set_prod_rate_list(arc, prod)

        if ";" in str_cons:
            str_cons_ini, str_cons = str_cons.split(";")
            str_cons_ini = str_cons_ini.split(",")
            cons_ini = []
            ini_threshold = []
            for value in str_cons_ini:
                if ":" in value:
                    value, threshold = value.split(":")
                    ini_threshold.append(int(threshold))
                else:
                    ini_threshold.append(int(value))
                cons_ini.append(int(value))

            dataflow.set_ini_cons_rate_list(arc, cons_ini)
            if isinstance(dataflow, PCG):
                dataflow.set_ini_threshold_list(arc, ini_threshold)

        str_cons = str_cons.split(",")
        cons = []
        threshold = []
        for value in str_cons:
            if ":" in value:
                value, threshold_str = value.split(":")
                threshold.append(int(threshold_str))
            else:
                threshold.append(int(value))
            cons.append(int(value))

        if isinstance(dataflow, SDF):
            dataflow.set_cons_rate(arc, cons[0])
        if isinstance(dataflow, CSDF):
            dataflow.set_cons_rate_list(arc, cons)
        if isinstance(dataflow, PCG):
            dataflow.set_threshold_list(arc, threshold)

    return dataflow


def __readline(open_file):
    line = open_file.readline()
    while "#" in line:
        line = open_file.readline()
    return line
