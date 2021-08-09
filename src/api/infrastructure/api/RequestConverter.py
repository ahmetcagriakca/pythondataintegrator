import inspect
import json
from datetime import datetime

from infrastructure.utils.TypeChecker import TypeChecker
from infrastructure.json.DateTimeEncoder import DateTimeEncoder


class RequestConverter(object):
    def __init__(self):
        self.mappings = {}

    def class_mapper(self, d):
        for keys, cls in self.mappings.items():
            if keys.issuperset(d.keys()) :  # are all required arguments present?
                return cls(**d)
        else:
            # Raise exception instead of silently returning None
            raise ValueError(f'Unable to find a matching class for object: {d}')

    def complex_handler(self, Obj):
        if hasattr(Obj, '__dict__'):
            return Obj.__dict__
        else:
            raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj)))

    def register(self, cls):
        self.mappings[frozenset(tuple([attr for attr, val in cls().__dict__.items()]))] = cls
        annotations=self.get_annotations(cls())
        self.register_subclasses(annotations)
        return cls

    def ToJSON(self, obj):
        return json.dumps(dict(obj), cls=DateTimeEncoder, indent=4)

    def FromJSON(self, json_str):
        return json.loads(json_str, object_hook=self.class_mapper)

    @staticmethod
    def get_annotations(obj):
        if hasattr(obj, '__annotations__'):
            annotations = obj.__annotations__
            return annotations
        else:
            return None

    def register_subclasses(self,annotations):
        generic_type_checker = TypeChecker()
        for key in annotations:
            value = annotations[key]
            if value == int:
                pass
            elif value == str:
                pass
            elif value == bool:
                pass
            elif value == datetime:
                pass
            elif value == float:
                pass
            else:
                if generic_type_checker.is_generic(value):
                    self.register(value.__args__[0])
                    instance = value.__args__[0]()
                    nested_annotations = self.get_annotations(instance)
                    if nested_annotations is not None:
                        self.register_subclasses(nested_annotations)
                elif generic_type_checker.is_base_generic(value):
                    # TODO:Base generic class
                    print('value type should be a structure of', value.__args__[0])
                elif inspect.isclass(value):
                    self.register(value)
                    instance = value()
                    nested_annotations = self.get_annotations(instance)
                    if nested_annotations is not None:
                        self.register_subclasses(nested_annotations)
                else:
                    print('Type not know', value)