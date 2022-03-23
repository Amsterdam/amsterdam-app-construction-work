class IproxRecursion:
    """ A recursive algorithm to search through IPROX data
        It gets a list of target strings used as a 'stop' condition to (ex/in-)clude the tree from recursion
    """

    def filter(self, data, result, targets=None, veld=None):
        # Iprox subtrees are either lists or dictionaries
        if isinstance(data, dict):
            if data.get('Nam') in targets:
                if data.get('veld', None) is not None:
                    # We reached the leaves of the tree, we can harvest a result
                    result.append({veld: data})
                elif data.get('cluster', None) is not None:
                    # We need to dive deeper into the tree
                    result = self.filter(data['cluster'], result, targets=targets, veld=data.get('Nam'))

        elif isinstance(data, list):
            for i in range(0, len(data), 1):
                if data[i].get('Nam') in targets:
                    if data[i].get('veld', None) is not None:
                        # We reached the leaves of the tree, we can harvest a result
                        result.append({data[i].get('Nam'): data[i].get('veld')})
                    elif data[i].get('cluster', None) is not None:
                        # We need to dive deeper into the tree
                        result = self.filter(data[i], result, targets=targets, veld=data[i].get('Nam'))

        # We got the leaves and can return with the harvest
        return result
