from Turbine.generation.generate import generate
from Turbine.param.parameters import Parameters


print "###### Setup the SDF generation #####"
c_param = Parameters()
c_param.set_dataflow_type("SDF")
c_param.set_solver(None)  # pass the initial marking computation phase when generate the dataflow
c_param.set_min_arcs_count(1)
c_param.set_max_arcs_count(5)
c_param.set_nb_task(100)

print "###### Generate dataflow ############"
dataflow = generate("SDF_of_test", c_param)  # Generate a SDF dataflow graph
print dataflow

print "###### Compute the initial marking ##"
dataflow.compute_initial_marking(solver_str="SC1_MIP")  # Compute the minimal initial marking
print dataflow
