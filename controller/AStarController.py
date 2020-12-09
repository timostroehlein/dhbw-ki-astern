from model.Link import Link
from model.Node import Node


class AStartController:
    def __init__(self, links, nodes, start_node: Node, dest_node: Node):
        self.links = links
        self.nodes = nodes
        self.start_node = start_node
        self.dest_node = dest_node

    def start_search(self):
        # Initialization
        self.start_node.f = self.start_node.g = self.start_node.h = 0
        self.start_node.tritanium_blaster = 12
        self.start_node.energy_units = 12
        open_list = [self.start_node]   # Open list, contains the start node at the beginning
        closed_list = []                # Closed list, contains all already visited nodes

        # Iterate through all nodes until every node has been visited or the destination node has not been reached
        while open_list:
            # Get the current node
            current_node = open_list[0]

            # Finish if the current node is the destination node
            if current_node == self.dest_node:
                # Destroying the vinculum costs 5 minutes, with a tritanium-blaster 1 minute
                cost = 1 if current_node.tritanium_blaster >= 1 else 5
                current_node.g = current_node.g + cost
                current_node.f = current_node.g + current_node.h
                # Reconstruct the path
                path = self.reconstruct_path(current_node)
                print('Destination reached, cost: %d' % current_node.f)
                for p in path:
                    print(p)
                exit(0)

            # Pop current node off the open list and add it to the closed list
            open_list.pop(0)
            closed_list.append(current_node)

            # Get all links to the child nodes
            links = []
            nodes = []
            for link in self.links:
                if link.node1 == current_node:
                    links.append(link)
                    nodes.append(link.node2)
                elif link.node2 == current_node:
                    links.append(link)
                    nodes.append(link.node1)

            # Iterate through all children
            current_link: Link
            child_node: Node
            for current_link, child_node in zip(links, nodes):
                # Continue if node of the link is in the closed list
                if child_node in closed_list:
                    continue

                # Calculate the f, g and h values
                self.g(current_link, current_node, child_node)
                self.h(child_node)
                child_node.f = child_node.g + child_node.h
                child_node.parent_node = current_node

                # Check if the child node is already in the open list
                if any(child_node == open_node for open_node in open_list):
                    continue

                # Append the child node to the open list
                open_list.append(child_node)

    def g(self, link: Link, current_node: Node, child_node: Node):
        # TODO: Implement blasting a hole in a wall or ground
        # Blasting a hole in a wall with a tritanium-blaster costs 3 minutes, can be used in all directions expect up

        # No obstacle, costs 1 minute
        if link.is_open:
            child_node.g = current_node.g + 1
            child_node.regeneration_time = current_node.regeneration_time - 1
        # Costs 2 minutes
        elif link.is_door:
            child_node.g = current_node.g + 2
            child_node.regeneration_time = current_node.regeneration_time - 2
        # Destroying a drone costs 3 minutes and one energy unit
        # 5 minute regeneration time before a new drone can be fought
        elif link.is_sentinel and current_node.energy_units > 0:
            # Check whether a regeneration is set or not, if so, take a brake
            # A 1 minute Break can always be used and repeated
            if current_node.regeneration_time == 0:
                child_node.g = current_node.g + 3
                child_node.energy_units = current_node.energy_units - 1
                child_node.regeneration_time = 5
            else:
                child_node.g = current_node.g + 3 + current_node.regeneration_time
                child_node.energy_units = current_node.energy_units - 1
                child_node.regeneration_time = 5
        # Up the ladder costs 2 minutes
        # Down costs 1/2 minute
        elif link.is_ladder:
            # Check if the ladder has been went up or down
            if current_node.z <= child_node.z:
                child_node.g = current_node.g + 2
                child_node.regeneration_time = current_node.regeneration_time - 2
            else:
                child_node.g = current_node.g + 0.5
                child_node.regeneration_time = current_node.regeneration_time - 0.5

    # Estimate the cost of the cheapest path from the next node to the destination node
    def h(self, child_node: Node):
        x1, y1, z1 = child_node.x, child_node.y, child_node.z
        x2, y2, z2 = self.dest_node.x, self.dest_node.y, self.dest_node.z
        child_node.h = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

    def reconstruct_path(self, current_node: Node):
        # TODO: Calculate the path and print it
        path = [str(current_node)]
        while current_node != self.start_node:
            current_node = current_node.parent_node
            path.append(str(current_node))
        # Return reversed path
        return path[::-1]
