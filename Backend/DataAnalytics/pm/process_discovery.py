import os
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner


def alphaMiner(log):
    net, initial_marking, final_marking = alpha_miner.apply(log)
    return(net, initial_marking, final_marking)

def inductiveMiner(log):
    net, initial_marking, final_marking = inductive_miner.apply(log)
    return(net, initial_marking, final_marking)

def heuristicMinerTree(log):
    net, initial_marking, final_marking = heuristics_miner.apply(log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})
    return(net, initial_marking, final_marking)