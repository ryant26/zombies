import random
import agentsim
from person import Person
from moveenhanced import MoveEnhanced

# co-dependent imports
import normal
import defender

class Zombie(MoveEnhanced):

    def __init__(self, **keywords):
        MoveEnhanced.__init__(self, **keywords)
        self.set_happiness(1)

        if agentsim.debug.get(2):
            print("Zombie", self._name)

    def get_author(self):
        return "Your names go here"

    def compute_next_move(self):
        if agentsim.debug.get(128):
            pass
        
        #get small
        self.set_size(self.get_min_size())
       # find nearest zombie.
        nearest = min(
            # make pairs of (person, distance from self to person)
            [ (p, self.distances_to(p)[0] ) for p in
                normal.Normal.get_all_instances() if p.is_present() ]
            ,
            # and sort by distance
            key=(lambda x: x[1])
            )
        (near_p, near_d) = nearest
        (d, delta_x, delta_y, d_edge_edge) = self.distances_to(near_p)

        return (delta_x, delta_y)
