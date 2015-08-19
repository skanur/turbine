from fractions import Fraction

from numpy.random.mtrand import randint

from Turbine.calc.lcm import lcm, lcm_list


def normalized_dataflow(dataflow):
    """Normalize according to a coefficient vector.

    Return
    ------
    Return the un-normalize graph.
    """
    if dataflow.is_normalized:
        return dataflow

    coef_vector = get_normalized_vector(dataflow)

    for arc in dataflow.get_arc_list():
        multiply_arc(dataflow, arc, coef_vector[arc])


def un_normalized_dataflow(dataflow, coef_vector=None):
    """Un-normalize according to a coefficient vector.

    Return
    ------
    Return the un-normalize graph.
    """
    if not dataflow.is_normalized:
        return dataflow

    if coef_vector is not None:
        if not __test_coef_vector(dataflow, coef_vector):
            raise Exception("Coefficient vector specified is not valid !")
    else:
        coef_vector = get_rdm_un_normalized_vector(dataflow)

    for arc in dataflow.get_arc_list():
        multiply_arc(dataflow, arc, coef_vector[arc])

    return coef_vector


def multiply_arc(dataflow, arc, coef):
    dataflow.set_initial_marking(arc, int(dataflow.get_initial_marking(arc) * coef))
    if dataflow.is_sdf:
        dataflow.set_prod_rate(arc, dataflow.get_prod_rate(arc)*coef)
        dataflow.set_cons_rate(arc, dataflow.get_cons_rate(arc)*coef)
    if dataflow.is_csdf:
        dataflow.set_prod_rate_list(arc, [int(x * coef) for x in dataflow.get_prod_rate_list(arc)])
        dataflow.set_cons_rate_list(arc, [int(x * coef) for x in dataflow.get_cons_rate_list(arc)])
    if dataflow.is_pcg:
        dataflow.set_ini_prod_rate_list(arc, [int(x * coef) for x in dataflow.get_ini_prod_rate_list(arc)])
        dataflow.set_ini_cons_rate_list(arc, [int(x * coef) for x in dataflow.get_ini_cons_rate_list(arc)])
        dataflow.set_threshold_list(arc, [int(x * coef) for x in dataflow.get_threshold_list(arc)])
        dataflow.set_ini_threshold_list(arc, [int(x * coef) for x in dataflow.get_ini_threshold_list(arc)])


def get_normalized_vector(dataflow):
    """Compute the normalization vector of an un-normalize graph.

    Return
    ------
    Return the the vector of coefficient for normalize the graph.
    """
    coef_list = {}

    lcm_rf = 1
    for task in dataflow.get_task_list():
        lcm_rf = lcm(lcm_rf, dataflow.get_repetition_factor(task))
    for arc in dataflow.get_arc_list():
        if dataflow.is_sdf:
            rate = dataflow.get_prod_rate(arc)
        if dataflow.is_csdf:
            rate = sum(dataflow.get_prod_rate_list(arc))
        zi = lcm_rf/dataflow.get_repetition_factor(dataflow.get_source(arc))
        # print lcm_rf, "t"+str(dataflow.get_source(arc)), dataflow.get_repetition_factor(dataflow.get_source(arc))
        # print str(arc[0])+"->"+str(arc[1]), "zi", zi, "rate", rate, "ka", Fraction(numerator=zi, denominator=rate)
        coef_list[arc] = Fraction(numerator=zi, denominator=rate)
    return coef_list


def get_normalized_vector_old(dataflow):
    """Compute the normalization vector of an un-normalize graph.

    Return
    ------
    Return the the vector of coefficient for normalize the graph.
    """
    coef = {}
    lcm_v = 1
    for arc in dataflow.get_arc_list():
        if dataflow.is_sdf:
            rate = dataflow.get_prod_rate(arc)
        if dataflow.is_csdf:
            rate = sum(dataflow.get_prod_rate_list(arc))
        rate *= dataflow.get_repetition_factor(dataflow.get_source(arc))
        lcm_v = lcm_list([lcm_v, rate])

    for arc in dataflow.get_arc_list():
        ri = dataflow.get_repetition_factor(dataflow.get_source(arc))
        if dataflow.is_sdf:
            zi = dataflow.get_prod_rate(arc)
        if dataflow.is_csdf:
            zi = sum(dataflow.get_prod_rate_list(arc))
        coef[arc] = (lcm_v / ri) / zi
    return coef


def get_rdm_un_normalized_vector(dataflow, max_num=10):
    """Compute the smallest vector for un-normalized the graph.

    ------
    Return the the vector of coefficient for un-normalize the graph.
    """
    if not dataflow.is_normalized:
        return

    coef = {}
    for arc in dataflow.get_arc_list():
        random_num = randint(1, max_num)
        coef[arc] = Fraction(numerator=random_num, denominator=dataflow.get_gcd(arc))
    return coef


def __test_coef_vector(dataflow, coef_vector):
    if len(coef_vector) != len(dataflow.get_arc_list()):
        return False

    for arc in dataflow.get_arc_list():
        coef = coef_vector[arc]
        if not __test_coef(coef, [dataflow.get_initial_marking(arc)]):
            return False

        if dataflow.is_sdf:
            if not __test_coef(coef, [dataflow.get_prod_rate(arc)]):
                return False
            if not __test_coef(coef, [dataflow.get_cons_rate(arc)]):
                return False

        if dataflow.is_csdf:
            if not __test_coef(coef, dataflow.get_prod_rate_list(arc)):
                return False
            if not __test_coef(coef, dataflow.get_cons_rate_list(arc)):
                return False

        if dataflow.is_pcg:
            if not __test_coef(coef, dataflow.get_ini_prod_rate_list(arc)):
                return False
            if not __test_coef(coef, dataflow.get_ini_cons_rate_list(arc)):
                return False
            if not __test_coef(coef, dataflow.get_threshold_list(arc)):
                return False
            if not __test_coef(coef, dataflow.get_ini_threshold_list(arc)):
                return False
        return True


def __test_coef(coef, coef_list):
    for x in coef_list:
        if x * coef != int(x * coef):
            return False
    return True
