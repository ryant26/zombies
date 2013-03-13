import random
import agentsim
from person import Person
from moveenhanced import MoveEnhanced
import callername
import re

# co-dependent imports
import zombie
import defender

class Normal(MoveEnhanced):

    def __init__(self, **keywords):

        MoveEnhanced.__init__(self, **keywords)

        # this records the information from the most recent
        # zombie alert move.  When compute_next_move() is called, 
        # this information can be processed.

        self._zombie_alert_args = None

        if agentsim.debug.get(2):
            print("Normal", self._name)

        self.set_happiness(1 - 2 * random.random())
        self.set_size(random.uniform(self.get_min_size(), self.get_max_size()))

    def get_author(self):
        return "Your names go here"

    def set_min_size(self):
        self.set_size(self.get_min_size())
    def set_max_size(self):
        self.set_size(self.get_max_size())

    def compute_next_move(self):
        # if we have a pending zombie alert, act on that first
        """
        if self._zombie_alert_args is not None:
            (x, y) = self._zombie_alert_args
            delta_x = x - self.get_xpos()
            delta_y = y - self.get_ypos()
            # clear the alert
            self._zombie_alert_args = None 
        else:
            """
        #set size medium
        self.set_size(self.get_max_size()/2)
        # find nearest zombie.
        nearest = min(
            # make pairs of (person, distance from self to person)
            [ (p, self.distances_to(p)[0] ) for p in
                zombie.Zombie.get_all_instances() if p.is_present() ]
            ,
            # and sort by distance
            key=(lambda x: x[1])
            )
        (near_p, near_d) = nearest
        (d, delta_x, delta_y, d_edge_edge) = self.distances_to(near_p)

         # Change Happiness
        delta_h = 0
        if d < 100:                 #close zombies is not good!
            delta_h = delta_h - 1
        else:                       #Far zombies are good!
             delta_h = delta_h +1 
        self.set_happiness(delta_h + self.get_happiness())

        #If we are unhappy run away!
        if self.get_happiness() <= 0:
            delta_x = delta_x + 2*(-delta_x)
            delta_y = delta_y + 2*(-delta_y)
        #if we are unhappy go to where the defenders want us to go
        #cause they know best right?
        else:
            if self._zombie_alert_args is not None:
                (x, y) = self._zombie_alert_args
                delta_x = x - self.get_xpos()
                delta_y = y - self.get_ypos()
                # clear the alert
                self._zombie_alert_args = None
        xposition = self.get_xpos()
        yposition = self.get_ypos()
        if xposition <= 10 and yposition <= 10 :
            self.set_min_size()
        return (delta_x, delta_y)

    def zombie_alert(self, x_dest, y_dest):
        # ignore any request not from a defender!
        caller_name = callername.caller_name()

        if not re.search(r"\.Defender\.", caller_name):
            raise Exception("zombie alert on {} called by non-Defender {}".format(self.get_name(), caller_name))

        if agentsim.debug.get(32):
            print("zombie_alert to ({}, {})".format( self.get_name(), x_dest, y_dest))

        # remember where the alert told us to go so that we can use this
        # information when we compute the next move
        self._zombie_alert_args = (x_dest, y_dest)
