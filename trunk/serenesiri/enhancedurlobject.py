from urlobject import URLObject


class EnhancedURLObject(URLObject):

    def del_query_param(self, key):
        new_query = [(k, v) for k, v in self.query_list() if k != key]
        return self.with_query(new_query)

    def __sub__(self, query_param):
        if hasattr(query_param, '__iter__'):
            new = self
            for qp in query_param:
                new = new.del_query_param(qp)
            return new
        else:
            return self.del_query_param(query_param)