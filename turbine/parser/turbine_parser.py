from models.graph import Graph
import StringIO
import sys

def write(dataflow, fileName):
    output = StringIO.StringIO()

    output.write("#Graph_name\n")
    output.write(str(dataflow.getName())+" "+str(dataflow.getGraphType())+"\n")
    
    output.write("#Number_of_tasks number_of_arcs\n")
    output.write(str(dataflow.getTaskCount())+" "+str(dataflow.getArcCount())+"\n")

    output.write("#TASKS\n")
    output.write("#Id repetition_factor phase_duration\n")
    for task in dataflow.getTaskList():
        output.write(str(task)+" "+str(dataflow.getRepetitionFactor(task))+" ")
        output.write(dataflow.getTaskDurationStr(task)+"\n")

    output.write("#ARCS\n")
    output.write("#(source,target) initial_marking production_vector consumption_vector\n")
    for arc in dataflow.getArcList():
        strArc = str(str(arc).split(",")[0])+","+str(str(arc).split(",")[1])+")"
        output.write(strArc.replace(" ","")+" ")
        output.write(str(dataflow.getInitialMarking(arc))+" ")
        output.write(dataflow.getProdStr(arc)+" ")
        output.write(dataflow.getConsStr(arc)+"\n")
        
    openFile = sys.stdout
    if fileName != None :
        openFile = open(fileName, "w")
    openFile.write(output.getvalue())
    output.close()
    openFile.close()

def read(fileName):
    openFile = open(fileName, "r")
    name, dataflowType = readline(openFile).replace("\n","").split(" ")
    dataflow = Graph(name)
    nbTask, nbArc = readline(openFile).split(" ")
    for i in xrange(int(nbTask)):
        line = readline(openFile).replace("\n","")
        taskName, Rt, strDur = line.split(" ")
        task = dataflow.addTask(taskName)
        dataflow.setRepetitionFactor(task, int (Rt))
        if ";" in strDur :
            strInitDur, strDur = strDur.split(";")
            initDurList = [int(i) for i in strInitDur.split(",")]
            dataflow.setPhaseCountInit(task,len(initDurList))
            dataflow.setPhaseDurationInitList(task,initDurList)

        durList = [int(float(i)) for i in strDur.split(",")]
        dataflow.setPhaseCount(task,len(durList))
        dataflow.setPhaseDurationList(task,durList)
            
    for i in xrange(int(nbArc)):
        line = readline(openFile).replace("\n","")
        strArc, strM0, strProd, strCons = line.split(" ")
        source = dataflow.getTaskByName(strArc.split(",")[0][1:])
        target = dataflow.getTaskByName(strArc.split(",")[1][:-1])
        M0 = int (strM0)
        arc = dataflow.addArc(source, target)
        dataflow.setInitialMarking(arc, M0)
        
        if ";" in strProd:
            strProdinit, strProd = strProd.split(";")
            prodInit =  [int (i) for i in strProdinit.split(",")]
            dataflow.setProdInitList(arc, prodInit)

        prod = [int (i) for i in strProd.split(",")]
        dataflow.setProdList(arc, prod)

        if ";" in strCons:
            strConsInit, strCons = strCons.split(";")
            strConsInit = strConsInit.split(",")
            consInit = []
            consInitThreshold = []
            for value in strConsInit:
                if ":" in value:
                    value, threshold = value.split(":")
                    consInitThreshold.append(int(threshold))
                else:
                    consInitThreshold.append(int(value))
                consInit.append(int(value))
            
            dataflow.setConsInitList(arc, consInit)
            if dataflowType == "PCG":
                dataflow.setConsInitThresholdList(arc, consInitThreshold)
        
        strCons = strCons.split(",")
        cons = []
        consThreshold = []
        for value in strCons:
            if ":" in value:
                value, threshold = value.split(":")
                consThreshold.append(int(threshold))
            else:
                consThreshold.append(int(value))
            cons.append(int(value))
            
        dataflow.setConsList(arc, cons)
        if "PCG" in dataflowType :
            dataflow.setConsThresholdList(arc, consThreshold)

    return dataflow

def readline(openFile):
    line = openFile.readline()
    while "#" in line:
        line = openFile.readline()
    return line

