# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (pacman).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

        "*** YOUR CODE HERE ***"

        ## for AgentState object
        ## state.pos gives the current position
        ## state.direction gives the travel vector
        # print "newScaredTimes:", newScaredTimes
        # print "getScore():",successorGameState.getScore()


        successorGameState = currentGameState.generatePacmanSuccessor(action)
        pacman = successorGameState.getPacmanPosition()
        foodList = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()

        if action == 'Stop':
            return -float('inf')

        if successorGameState.isWin():
            return float("inf")

        score = currentGameState.getScore()
        for ghost in newGhostStates:
            distance = util.manhattanDistance(pacman,ghost.getPosition())
            if (distance < 2):
                if (ghost.scaredTimer > 0):
                    score += 9999
                else:
                    return -float('inf')

        for food in foodList.asList():
            if pacman == food:
                return float('inf')
            distance = util.manhattanDistance(pacman, food)
            score += 1.0 / (distance)

        return score



def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def maxValue(gameState, depth):

            if gameState.isWin() or gameState.isLose():
                return [self.evaluationFunction(gameState), None]

            if depth == self.depth:
                return [self.evaluationFunction(gameState), None]

            v = -float('inf')
            takeAction = None
            legalActions = gameState.getLegalActions(0)

            for action in legalActions:
                nextStateValue = minValue(gameState.generateSuccessor(0, action), 1, depth)[0]
                if (v < nextStateValue):
                    v = nextStateValue
                    takeAction = action
            return [v, takeAction]


        def minValue(gameState, agent, depth):

            if gameState.isWin() or gameState.isLose():
                return [self.evaluationFunction(gameState), None]

            v = float('inf')
            takeAction = None
            legalActions = gameState.getLegalActions(agent)

            for action in legalActions:
                if (agent == gameState.getNumAgents() - 1):
                    nextStateValue = maxValue(gameState.generateSuccessor(agent, action), depth + 1)[0]
                else:
                    nextStateValue = minValue(gameState.generateSuccessor(agent, action), agent + 1, depth)[0]
                if (v > nextStateValue):
                    v = nextStateValue
                    takeAction = action
            return [v, takeAction]

        return maxValue(gameState, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, depth, alpha, beta):

            if gameState.isWin() or gameState.isLose():
                return [self.evaluationFunction(gameState), None]

            if depth == self.depth:
                return [self.evaluationFunction(gameState), None]

            v = -float('inf')
            takeAction = None
            legalActions = gameState.getLegalActions(0)

            for action in legalActions:
                nextStateValue = minValue(gameState.generateSuccessor(0, action), 1, depth, alpha, beta)[0]
                if v < nextStateValue:
                    v = nextStateValue
                    takeAction = action

                if (v > beta):
                    return [v, takeAction]

                if alpha < v:
                    alpha = v

            return [v, takeAction]

        def minValue(gameState, agent, depth, alpha, beta):

            if gameState.isWin() or gameState.isLose():
                return [self.evaluationFunction(gameState), None]

            v = float('inf')
            takeAction = None
            legalActions = gameState.getLegalActions(agent)

            for action in legalActions:
                if (agent == gameState.getNumAgents() - 1):
                    nextStateValue = maxValue(gameState.generateSuccessor(agent, action), depth + 1, alpha, beta)[0]
                else:
                    nextStateValue = minValue(gameState.generateSuccessor(agent, action), agent + 1, depth, alpha, beta)[0]
                if v > nextStateValue:
                    v = nextStateValue
                    takeAction = action

                if (v < alpha):
                    return [v, takeAction]

                if beta > v:
                    beta = v
            return [v, takeAction]

        return maxValue(gameState, 0, (-float('inf')), float('inf'))[1]



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameState, depth):

            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return [self.evaluationFunction(gameState), None]

            v = -float('inf')
            takeAction = None
            legalActions = gameState.getLegalActions(0)

            for action in legalActions:
                nextStateValue = expValue(gameState.generateSuccessor(0, action), 1, depth)[0]
                if (v < nextStateValue):
                    v = nextStateValue
                    takeAction = action
            return [v, takeAction]

        def expValue(gameState, agent, depth):

            if gameState.isWin() or gameState.isLose():
                return (self.evaluationFunction(gameState), None)

            v = 0
            takeAction = None
            legalActions = gameState.getLegalActions(agent)
            probability = 1.0 / len(legalActions)

            for action in legalActions:
                if (agent == gameState.getNumAgents() - 1):
                    nextStateValue = maxValue(gameState.generateSuccessor(agent, action), depth + 1)[0]
                else:
                    nextStateValue = expValue(gameState.generateSuccessor(agent, action), agent + 1, depth)[0]

                v += nextStateValue * probability
                takeAction = action
            return [v, takeAction]

        return maxValue(gameState, 0)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
        This evaluation function uses linear programming with the following values:
        - food remaining
        - ghost position
        - Pacman position
        from current state to calculate the score for the state. If the ghost is in the vicinity and it
        is not scared then the score is diminished by a significant factor. If the pacman is in the
        position of a food dot the score returned is extremely high - infinity
    """
    "*** YOUR CODE HERE ***"
    #  execute using:
    #   python pacman.py -p ExpectimaxAgent -a evalFn=better -l smallClassic
    pacman = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood()
    ghosts = currentGameState.getGhostStates()

    score = currentGameState.getScore()
    for ghost in ghosts:
        distance = util.manhattanDistance(pacman, ghost.getPosition())
        if (distance < 2):
            if (ghost.scaredTimer > 0):
                score += 9999
            else:
                score -= 9999

    for food in foodList.asList():
        if pacman == food:
            return float('inf')
        distance = util.manhattanDistance(pacman, food)
        score += 1.0 / (distance)

    return score


# Abbreviation
better = betterEvaluationFunction

