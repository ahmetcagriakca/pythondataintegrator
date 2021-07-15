def cls_to_dict(cls):
    def to_dict(self):
        _dict = self.__dict__
        for attr_name in self.__dict__:
            attr = getattr(self, attr_name)
            if not callable(attr) and isinstance(attr, list):
                entities = []
                for entity in attr:
                    entities.append(entity.to_dict())
                _dict[attr_name] = entities
        return _dict

    setattr(cls, 'to_dict', to_dict)
    return cls
