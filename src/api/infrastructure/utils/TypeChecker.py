import inspect
import typing
from abc import ABC
import builtins

def get_builtins():
    return list(filter(lambda x: not x.startswith('_'), dir(builtins)))

class ITypeChecker(ABC):
    def is_class(self, obj):
        if inspect.isclass(obj) and not self.is_primitive(obj):
            return True
        return False

    def is_primitive(self, obj):
        builtins_list =  list(filter(lambda x: not x.startswith('_'), dir(builtins)))
        return obj.__name__ in builtins_list

    def is_generic(self, class_type):
        pass

    def is_base_generic(self, class_type):
        pass


# python 3.7
if hasattr(typing, '_GenericAlias'):
    class TypeChecker(ITypeChecker):
        def is_generic(self, class_type):
            return self._is_generic(class_type)

        def is_base_generic(self, class_type):
            return self._is_base_generic(class_type)

        def _is_generic(self, cls):
            if isinstance(cls, typing._GenericAlias):
                return True
            if isinstance(cls, typing._SpecialForm):
                return cls not in {typing.Any}
            return False

        def _is_base_generic(self, cls):
            if isinstance(cls, typing._GenericAlias):
                if cls.__origin__ in {typing.Generic, typing._Protocol}:
                    return False
                if isinstance(cls, typing._VariadicGenericAlias):
                    return True
                return len(cls.__parameters__) > 0
            if isinstance(cls, typing._SpecialForm):
                return cls._name in {'ClassVar', 'Union', 'Optional'}
            return False


elif hasattr(typing, '_Union'):
    class TypeChecker(ITypeChecker):
        # python 3.6

        def is_generic(self, class_type):
            return self._is_generic(class_type)

        def is_base_generic(self, class_type):
            return self._is_base_generic(class_type)

        def _is_generic(self, cls):
            if isinstance(cls, (typing.GenericMeta, typing._Union, typing._Optional, typing._ClassVar)):
                return True
            return False

        def _is_base_generic(self, cls):
            if isinstance(cls, (typing.GenericMeta, typing._Union)):
                return cls.__args__ in {None, ()}
            if isinstance(cls, typing._Optional):
                return True
            return False
