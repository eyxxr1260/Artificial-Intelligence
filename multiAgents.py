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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        def value(depth, gameState, agentIndex):#依下一個agent是什麼決定要做min or max
            #當depth為0或遊戲勝負已出，就return目前的evaluation function算出的分數(終止條件)
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            if agentIndex == 0:#當此agent是Pacman
                return maxValue(depth, gameState, agentIndex)#找到所有得到的value中的最大值
            else:#當此agent不是Pacman(即ghost)
                return minValue(depth, gameState, agentIndex)#找到所有得到的value中的最小值

        def minValue(depth, gameState, agentIndex):#return state的最小value
            #當depth為0或遊戲勝負已出，就return目前的evaluation function算出的分數(終止條件)
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            
            v = float("inf")#先將v設為無限大，可確保接下來第一個得到的v一定會小於最原始的此v(因為要找min)
            for thisAction in gameState.getLegalActions(agentIndex):#此agent的legal actions list裡的所有action都跑一遍
                if agentIndex == gameState.getNumAgents() - 1:#當此agent是最後一個agent(index是number of agents-1)，下一輪要從第一個agent(從0開始，Pacman)開始
                    v = min(v, maxValue(depth - 1, gameState.generateSuccessor(agentIndex, thisAction), 0))#更新v的值(取min)，agentIndex=0代表下個agent是Pacman
                    #gameState.generateSuccessor(agentIndex, thisAction):Returns the successor game state after this agent takes this action
                    #並將depth - 1，因為下一個agent是敵方(Pacman)，深度需要遞減1
                    #Pacman要用maxValue function
                else:#還沒到最後一個agent，ghost使用minValue
                    v = min(v, minValue(depth, gameState.generateSuccessor(agentIndex, thisAction),  agentIndex + 1))#更新v的值(取min)，agentIndex+1代表下一個要進行動作的agentIndex
                    #gameState.generateSuccessor(agentIndex, thisAction):Returns the successor game state after this agent takes this action
            return v
        
        def maxValue(depth, gameState, agentIndex):#return state的最大value
            #當depth為0(遞減為0之類的)或遊戲勝負已出，就return目前的evaluation function算出的分數(終止條件)
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            
            v = -float("inf")#先將v設為負無限大，可確保接下來第一個得到的v一定會大於最原始的此v(因為要找max)
            for thisAction in gameState.getLegalActions(agentIndex):#此agent的legal actions list裡的所有action都跑一遍
                #一個個action代進去後找出最大值當作這個state的value，這個value表示經過此agent做了此action後，可以獲得的max value，return這個最大value，用來決定當前玩家(agentIndex)採取哪個行動(thisAction)
                v = max(v, minValue(depth, gameState.generateSuccessor(agentIndex, thisAction), agentIndex + 1))
                #因為maxValue function會呼叫minValue function，而 minValue function裡本來就有判斷if agentIndex == gameState.getNumAgents() - 1來決定agent要做什麼，所以在maxValue function中不用再加上那行判斷式
            return v

        Maximum = -float("inf")#先將maximum設為負無限大，可確保第一個得到的score一定會大於maximum，就能依序比較
        a = None#最佳action一開始還沒有東西
        for thisAction in gameState.getLegalActions(0):#Pacman的legal actions list裡的所有action都跑一遍
            s = value(self.depth, gameState.generateSuccessor(0, thisAction), 1)#self.depth是限制的深度
            #gameState.generateSuccessor(0, thisAction):Returns the successor game state after a Pacman takes this action
            #agentIndex=1代表第一個不是Pacman的agent(ghost)，把這些代到value function會選擇Pacman的所有legal action所得到的所有vlaue中的最小值
            if s == max(s,Maximum):#當s大於目前的maximum，maximum=s
            #每跑到一個action就比較一次，跑完這個for迴圈會找出所有的min值中最大的那個值，那個值對應的action也就會是最佳的action，然後return最佳action
                Maximum = s
                a = thisAction
        return a
        
        
        
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
