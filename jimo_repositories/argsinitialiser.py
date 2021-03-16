import os


"""
 A class wrapper to specific defaults arguments and help to validate them base on the default types.
"""


class argument_validator:

    def __init__(self, *args, **kwargs):
        self.validator = ArgsInitialiser(*args, **kwargs)
        pass

    def __call__(self, operation):
        # validate a class parameters
        validator = self.validator
        if(type(operation) == object.__class__):
            class __ClsValidator(operation):

                def __init__(self, *args, **kwargs):
                    super().__init__(
                        *validator.expected_arguments[0], **validator.expected_arguments[1])

                def __new__(cls, *args, **kwargs):
                    if(validator.validate(*args, **kwargs)):
                        return super().__new__(cls)
                    return
            __ClsValidator.__name__ = operation.__name__
            return __ClsValidator
        else:
            if(callable(operation) is True):
                def construct_operation_wrapper(*args, **kwargs):
                    if(validator.validate(*args, **kwargs)):
                        return operation(*validator.expected_arguments[0], **validator.expected_arguments[1])
            return construct_operation_wrapper


"""
  ArgsInitialiser : A class that will allow user to subscribed
    
"""


class ArgsInitialiser(object):

    def __init__(self, *args_expected,  **kwargs__expected):
        self.__expected_arguments = (args_expected, kwargs__expected)

    def validate(self, *args, **kwargs):
        args_final = list(self.__expected_arguments[0])
        last_index = 0
        # check the number of args if they match with expected.
        if(len(args_final) > 0) and (len(args) >= len(args_final)):

            for i in range(len(args_final)):
                if(args_final[i] is not None):
                    if(type(args[i]) != type(args_final[i])):
                        expected_type = type(args_final[0][i])
                        raise TypeError(
                            "@arguments:Invalid argument type provided = {0}, expecting a type of {1}.".format(type(args[i]), expected_type))
                args_final[i] = args[i]
                last_index = i
        for i in range(last_index, len(args)):
            args_final.append(args[i])
        self.__expected_arguments = (args_final, self.__expected_arguments[1])

        for key in kwargs:
            if(key in self.__expected_arguments[1]) is not True:
                raise ValueError(
                    "@arguments:Invalid {0} parameter provided.".format(key))
            if(self.__expected_arguments[1][key] is not None):
                input_type = type(kwargs[key])
                expected_type = type(self.__expected_arguments[1][key])
                if(input_type != expected_type):
                    raise TypeError(
                        "@arguments:Invalid argument type provided = {0}, expecting a type of {1}.".format(input_type, expected_type))
            self.__expected_arguments[1][key] = kwargs[key]
        return True

    @property
    def expected_arguments(self):
        return self.__expected_arguments


if __name__ == "__main__":

    @argument_validator(name="Obaro", age=89)
    def value(**kwargs):
        print(kwargs['name'])
        print(kwargs['age'])
        return "Job"
    # Test class

    @argument_validator(name=None, age=89)
    class __Person(object):
        def __init__(self, filename, **kwargs):
            self.Name = kwargs['name']
            self.Age = kwargs['age']

    p = __Person("Obaro", age=100)
    value()
