from collections import defaultdict

class Pathfinder:
    def __init__(self, db_manager):
        self.db = db_manager
        self.adj_list = defaultdict(list)

    def refresh_graph(self):
        # Fetches all distances to build adjaceny list.
        distances = self.db.get_all_distances()

        # Clear the old graph if it exists.
        self.adj_list = defaultdict(list)
    
        for dist in distances:
            self.adj_list[dist.store_a_name].append((dist.store_b_name,dist.travel_distance_minutes))

        return self.adj_list



