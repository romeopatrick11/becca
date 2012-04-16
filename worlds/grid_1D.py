
import numpy as np
from .base_world import World as BaseWorld

class World(BaseWorld):
    """ grid_1D.World
    One-dimensional grid task

    In this task, the agent steps forward and backward along a
    nine-position line. The fourth position is rewarded (+1/2) and the ninth
    position is punished (-1/2). There is also a slight punishment
    for effort expended in trying to move, i.e. taking actions.
    
    This is intended to be a simple-as-possible task for
    troubleshooting BECCA.
    
    The theoretically optimal performance without exploration is 0.5 
    reward per time step.
    In practice, the best performance the algorithm can achieve with the 
    exploration levels given is around 0.35 to 0.37 reward per time step.
    """

    def __init__(self):
                
        super(World, self).__init__()
        
        self.REPORTING_PERIOD = 10 ** 8
        self.display_state = False

        self.num_sensors = 1
        self.num_primitives = 9
        self.num_actions = 9

        self.world_state = 0
        self.simple_state = 0

    
    def step(self, action): 
        """ advances the World by one timestep.
        Accepts agent as an argument only so that it can occasionally backup
        the agent's state to disk.
        """

        if action is None:
            action = np.zeros(self.num_actions)
        
        self.timestep += 1 

        step_size = (action[0] + 
                 2 * action[1] + 
                 3 * action[2] + 
                 4 * action[3] - 
                     action[4] - 
                 2 * action[5] - 
                 3 * action[6] - 
                 4 * action[7])
                        
        # an approximation of metabolic energy
        energy    = (action[0] + 
                 2 * action[1] + 
                 3 * action[2] + 
                 4 * action[3] + 
                     action[4] + 
                 2 * action[5] + 
                 3 * action[6] + 
                 4 * action[7])

        self.world_state = self.world_state + step_size
        
        # ensures that the world state falls between 0 and 9
        self.world_state = (self.world_state - 
                            9 * np.floor_divide(self.world_state, self.num_primitives))
        self.simple_state = int(np.floor(self.world_state))
        
        # Assigns basic_feature_input elements as binary. Represents the presence
        # or absence of the current position in the bin.
        sensors = np.zeros(self.num_sensors)
        primitives = np.zeros(self.num_primitives)
        primitives[self.simple_state] = 1

        # Assigns reward based on the current state
        reward = primitives[8] * (-0.5)
        reward += primitives[3] * ( 0.5)
        
        # Punishes actions just a little.
        reward -= energy / 100

        #print action, primitives, reward        
        reward = np.max(reward, -1)
        
        self.display()
        
        return sensors, primitives, reward
    
        
    def display(self):
        """ provides an intuitive display of the current state of the World 
        to the user
        """
        if (self.display_state):
            state_image = ['.'] * self.num_primitives
            state_image[self.simple_state] = 'O'
            #print('world timestep %s    %s' % (self.timestep, ''.join(state_image)))
            print(''.join(state_image))
            
        if (self.timestep % self.REPORTING_PERIOD) == 0:
            print("world age is %s timesteps " % self.timestep)

        
        
