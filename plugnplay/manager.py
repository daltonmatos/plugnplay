class Manager(object):
    '''
    The main plugin Manager class.
    Stores all implementors of all public interfaces
    '''

    def __init__(self):
        self.iface_implementors = {}

    def add_implementor(self, interface, implementor_instance):
        self.iface_implementors.setdefault(interface, [])
        self.iface_implementors[interface].append(implementor_instance)

    def implementors(self, interface, filter_callback=None, *args, **kwargs):
        all_implementors = self.iface_implementors.get(interface, [])
        if not filter_callback:
            return all_implementors
        return self._filter(filter_callback, all_implementors, *args, **kwargs)

    def _filter(self, callback, items, *args, **kwargs):
        _r = []
        for i in items:
            if callback(i, *args, **kwargs):
                _r.append(i)
        return _r
