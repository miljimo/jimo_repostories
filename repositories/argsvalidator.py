"""

"""
class ArgsValidator(object):
    '''
      @ArgValidator : this validate the argument given to make sure
      that unexpected argument is given.
    '''
    def __init__(self,name):
        self.__Name  =  name;
        self.__expected_arg_keys = list();

    @property
    def name(self):
        return self.__Name;

    @property
    def expected_argument_keys(self):
        return self.__expected_arg_keys;

    @expected_argument_keys.setter
    def expected_argument_keys(self, args):
        if(type(args) == list):
            self.__expected_arg_keys = args;

    def valid(self, **kwargs):
        for key in kwargs:
            if( key in self.expected_argument_keys) is not True:
                raise ValueError("{0} : Unknown '{1}' argument provided".format(self.name, key))
        return True;