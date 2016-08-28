# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """

        # TODO
        probability = random.random()
        
        if probability < self.clearProb:
            return True
        return False
    
    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        # TODO
        diceRoll = random.random()
        givenProb = self.maxBirthProb*(1-popDensity)

        if diceRoll < givenProb:
            return SimpleVirus(self.maxBirthProb,self.clearProb)
        else:
            raise NoChildException()



class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """

        # TODO
        assert type(viruses) == list and type(maxPop) == int
        
        self.viruses = viruses
        self.maxPop = maxPop


    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """

        # TODO
        return len(self.viruses)

    def clearViruses(self):

        for virus in self.viruses:
            if virus.doesClear():
                self.viruses.remove(virus)


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        self.clearViruses()

        popDensity =  float(self.getTotalPop())/self.maxPop

        for virus in self.viruses:
            try:
                posKid = virus.reproduce(popDensity)
            except:
                continue
                
            self.viruses.append(posKid)

        return self.getTotalPop()

#
# PROBLEM 2
#
def simulationWithoutDrug(maxBirthProb = 0.1, clearProb = 0.05, maxPop = 1000, maxTimeSteps = 300):

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    
    vList = [SimpleVirus(maxBirthProb,clearProb) for i in range(100)]
    popList = [100]
    count = 0
    patient = SimplePatient(vList,maxPop)

    for i in range(maxTimeSteps):
        patient.update()
        popList.append(patient.getTotalPop())
        if (patient.getTotalPop() > maxPop) or patient.getTotalPop == 0:
            break
            

    timeList = list(range(len(popList)))

    return popList

def simGraphBuilder():
    birthProbList = [0.01,0.05,0.10,0.15,0.20]
    popListList = []

    for i in range(len(birthProbList)):
        popListList.append(simulationWithoutDrug(birthProbList[i]))
        pylab.figure()
        pylab.xlabel("Time Increments")
        pylab.ylabel("Population of Viruses w/ " + str(birthProbList[i]) + "birth prob")
        pylab.plot(list(range(len(popListList[i]))),popListList[i])
    pylab.show()

def averageSimGraphBuilder(simRun):
    popListList = []
    avgList = []
    pops = []
    for i in range(simRun):
        popListList.append(simulationWithoutDrug())

    avgList = [0 for i in range(len(popListList[0]))]
    
    for i in range(len(popListList)):
        for j in range(len(popListList[i])):
            avgList[j] = avgList[j] + popListList[i][j]
            
    for k in range(len(avgList)):
        avgList[k] = avgList[k]/simRun

    x = list(range(len(avgList)))

    pylab.xlabel("Time Increments")
    pylab.ylabel("Amount of SimpleViruses in patient at time x")
    pylab.plot(x,avgList)
    

def simpleGraph():
    y = simulationWithoutDrug(.2,.05)
    x = list(range(len(y)))

    pylab.plot(x,y)
    pylab.show()
            

