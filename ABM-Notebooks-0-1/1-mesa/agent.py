from mesa import Agent
import random
from mesa import Model

class RandomWalker(Agent):
    def __init__(self, unique_id, model : Model, pos):
        super().__init__(unique_id, model)

        self.pos = pos

    def random_move(self):
        ''' 
        This method should get the neighbouring cells (Moore's neighbourhood), select one, and move the agent to this cell.
        '''
        # Get the neighbours of the agent
        print(f"Agent {self.unique_id} at {self.pos} is moving.")
        neighbours_cells = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=1)
        # print(f"Neighbour cells space of agent {self.unique_id} at {self.pos}: {neighbours_cells}")

        # If there are no neighbours, we cannot move
        if not neighbours_cells:
            print(f"Agent {self.unique_id} at {self.pos} has no neighbours to move to.")
            return
        
        # Randomly select a neighbour to move to
        new_pos = random.choice(neighbours_cells)
        
        # Move the agent to the new position
        self.model.grid.move_agent(self, new_pos)
        self.pos = new_pos
        print(f"Agent {self.unique_id} moved to {self.pos}")
        
    
class Sheep(RandomWalker):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

    def step(self):
        '''
        This method should move the Sheep using the `random_move()` method implemented earlier, then conditionally reproduce.
        '''
        # Step 1: move the sheep randomly
        self.random_move()

        # Step 2: reproduction (probabilistic)
        if random.random() < self.model.sheep_reproduction_chance:
            # get the neighboring cells of the sheep
            neighbor_cells = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False,
                radius=1
            )

            # # Find the occupied positions among these cells
            # occupied_positions = [agent.pos for agent in self.model.grid.get_neighbors(
            #     self.pos,
            #     moore=True,
            #     include_center=False,
            #     radius=1
            # )]

            # # Remove occupied positions from all cells
            # empty_positions = [cell for cell in neighbor_cells if cell not in occupied_positions]

            # # If there are empty spaces to reproduce, randomly select one
            # if empty_positions:
            #     new_pos = random.choice(empty_positions)
            #     self.model.new_agent(Sheep, new_pos)  # model.new_agent is used to create a new Sheep agent
            #     print(f"Sheep {self.unique_id} reproduced at {new_pos}")

            new_pos = random.choice(neighbor_cells)
            self.model.new_agent(Sheep, new_pos)  # model.new_agent is used to create a new Sheep agent
            print(f"Sheep {self.unique_id} reproduced at {new_pos}")


class Wolf(RandomWalker):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

    def step(self):
        '''
        This method should move the wolf, then check for sheep on its location, 
        eat one sheep if it is available and reproduce, and finally, conditionally die.
        '''
        # Step 1: randomly move the wolf
        self.random_move()

        # Step 2: check for sheep and eat one if available
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        sheep_here = [agent for agent in cellmates if isinstance(agent, Sheep)]

        if sheep_here:
            # Step 2.1: eat one sheep
            sheep_to_eat = random.choice(sheep_here)
            self.model.remove_agent(sheep_to_eat)
            print(f"Wolf {self.unique_id} ate Sheep {sheep_to_eat.unique_id} at {self.pos}")

            # Step 2.2: reproduction
            neighbor_cells = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False,
                radius=1
            )

            # occupied_positions = [agent.pos for agent in self.model.grid.get_neighbors(
            #     self.pos,
            #     moore=True,
            #     include_center=False,
            #     radius=1
            # )]
            # empty_positions = [cell for cell in neighbor_cells if cell not in occupied_positions]

            # if empty_positions:
            #     new_pos = random.choice(empty_positions)
            #     self.model.new_agent(Wolf, new_pos)
            #     print(f"Wolf {self.unique_id} reproduced at {new_pos}")

            if neighbor_cells:
                new_pos = random.choice(neighbor_cells)
                self.model.new_agent(Wolf, new_pos)
                print(f"Wolf {self.unique_id} reproduced at {new_pos}")
            
        # Step 3: conditionally die
        if random.random() < self.model.wolf_death_chance:
            print(f"Wolf {self.unique_id} died at {self.pos}")
            self.model.remove_agent(self)
