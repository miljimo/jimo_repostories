from repositories.argsvalidator import ArgsValidator

class ArgsInitialiser(object):

    def __init__(self, **kwargs):
        self.__input_kwargs        =  kwargs;
        self.__expected_arguments  =  dict();
        self.__validator  =  ArgsValidator("argument_validator");
            
    def initialise_default(self, **kwargs ):
        for key in kwargs:
            if(key in self.__expected_arguments) is True:
                raise ValueError("@initialing the argument {0} multi-times ".format(key))
            self.__expected_arguments[key] = kwargs[key];
            if(key in self.__validator.expected_argument_keys) is not True:
                self.__validator.expected_argument_keys.append(key);

    def populate(self):
        if(self.__valid()):
            for key in self.__input_kwargs:
                self.expected_arguments[key] = self.__input_kwargs[key];

    @property
    def expected_arguments(self):
        return self.__expected_arguments;

    def get(self, key:str):
        if(type(key) != str):
            raise TypeError("Expecting key value to be string but {0} given".format(key));
        return self.expected_arguments[key];

    def __valid(self):
        return self.__validator.valid(**self.__input_kwargs);
   
