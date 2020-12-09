import sys


class Node:
    def __init__(self, position):
        self.position = position
        self.f = sys.maxsize    # Total cost of the node: f = g + h
        self.g = sys.maxsize    # Cost of from the start node to this node
        self.h = sys.maxsize    # Estimate the cost from the current node to the destination node
        self.parent_node = None         # Parent node used for cheapest path
        self.parent_link_type = None
        self.tritanium_blaster = 0      # Used to open a wall/ ground and destroy the vinculum faster
        self.energy_units = 0           # Used to fight drones
        self._regeneration_time = 0      # 5 minutes regeneration time after fighting a drone

    @property
    def regeneration_time(self):
        return self._regeneration_time

    @regeneration_time.setter
    def regeneration_time(self, value):
        if value < 0:
            self._regeneration_time = 0
        else:
            self._regeneration_time = value

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.position == other.position

    # Sort nodes
    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        return '%s,\tf: %f,\tg: %f,\th: %f,\ttritanium_blaster: %d,\tenergy_units: %d,'\
                '\tregeneration_time: %f,\tlink_type: %s'\
                % (self.position, self.f, self.g, self.h, self.tritanium_blaster, self.energy_units,
                    self.regeneration_time, self.parent_link_type)

    def __repr__(self):
        return str(self)
