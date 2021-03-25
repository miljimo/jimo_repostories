import os


"""
 A class wrapper to specific defaults arguments and help to validate them base on the default types.
"""


class argument_validator:

    def __init__(self, *args, **kwargs):
        #This arguments will be used to initial the class and its called once.
        self.validator = ArgsInitialiser(*args, **kwargs)
        
        pass

    def __call__(self, operation):
        # validate a class parameters
        validator = self.validator
        if(type(operation) == object.__class__):
            class __ClsValidator(operation):

                def __init__(self, *args, **kwargs):
                    super().__init__(
                        *validator.args, **validator.kwargs)                    

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
                        return operation(*validator.args, **validator.kwargs)
            return construct_operation_wrapper


"""
  ArgsInitialiser : A class that will allow user to subscribed
    
"""


class ArgsInitialiser(object):

    def __init__(self, *args,  **kwargs):

        self.args    = args;
        self.kwargs  = kwargs;
      

    def validate(self, *args, **kwargs):
        self.args  =  args;
        
        for key in kwargs:           
            if(key in self.kwargs.keys()) is not True:
                raise ValueError(
                    "@arguments:Invalid argument {0} parameter provided.".format(key))
            if(self.kwargs[key] is not None):
                input_type = type(kwargs[key])
                expected_type = type(self.kwargs[key])
                if(input_type != expected_type):
                    raise TypeError(
                        "@arguments:Invalid argument type provided = {0}, expecting a type of {1}.".format(input_type, expected_type))
            self.kwargs[key] = kwargs[key]       
        return True



if __name__ == "__main__":


    @argument_validator(age=89, name="Obaro")
    class __Person(object):
        def __init__(self, filename:str, **kwargs):
            self.Name = kwargs['name']
            self.Age = kwargs['age']
           
    filename =  "Obaro.data"
    p = __Person(filename, name="Johnson")
    p2 = __Person(filename)
    print(p.Name)
    
