from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness_evaluator

def replayFitness(log, type):
    if type=="alignment":
        fitness = replay_fitness_evaluator.apply(log, net, im, fm, variant=replay_fitness_evaluator.Variants.ALIGNMENT_BASED)
        return(fitness)
    elif type=="token":
        fitness = replay_fitness_evaluator.apply(log, net, im, fm, variant=replay_fitness_evaluator.Variants.TOKEN_BASED)
        return(fitness)   

def precision(log, type):
    if type=="alignment":
        prec = precision_evaluator.apply(log, net, im, fm, variant=precision_evaluator.Variants.ALIGN_ETCONFORMANCE)
        return(prec)
    elif type=="token":
        prec = precision_evaluator.apply(log, net, im, fm, variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
        return(prec)           