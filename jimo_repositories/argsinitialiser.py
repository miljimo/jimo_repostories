import os;

"""
class argument wrapper that allow you to validate
your inputs and set default values using functions wrappers;
"""
def argument_validator(*expected_args, **expected_kwargs):
    initialiser  =  ArgsInitialiser(*expected_args, **expected_kwargs);
    def create_initialiser_wrapper(initialiser:ArgsInitialiser):
        def operation_wrapper_caller(operation:callable):
            def construct_operation_wrapper(*args, **kwargs):
                #Validate the arguments and if its passed then always initial with the
                #right or default arguments.
                if(initialiser.validate(*args, **kwargs)):
                   return operation(*initialiser.expected_arguments[0], **initialiser.expected_arguments[1]);
            return construct_operation_wrapper;
        return operation_wrapper_caller;
    return create_initialiser_wrapper(initialiser);
      
    
    
"""
  ArgsInitialiser : A class that will allow user to subscribed
    
"""
class ArgsInitialiser(object):

    def __init__(self,*args_expected,  **kwargs__expected):
        self.__expected_arguments   =  (args_expected, kwargs__expected);
       
    def validate(self, *args, **kwargs):
        args_final  = list(self.__expected_arguments[0]);
        last_index  = 0;
        #check the number of args if they match with expected.
        if(len(args_final) > 0) and (len(args) >= len(args_final)) :          
                  
            for i in range(len(args_final)):
                if(args_final[i] is not None):
                    if(type(args[i]) != type(args_final[i])):
                        expected_type  =  type(args_final[0][i]);
                        raise TypeError("@arguments:Invalid argument type provided = {0}, expecting a type of {1}.".format(type(args[i]),expected_type));
                args_final[i] = args[i];
                last_index  =  i;
        for i in range(last_index , len(args)):
            args_final.append(args[i]);
        self.__expected_arguments =  (args_final , self.__expected_arguments[1]);                
                
        for key in kwargs:
            if(key in  self.__expected_arguments[1]) is not True:
                raise ValueError("@arguments:Invalid {0} parameter provided.".format(key));
            if( self.__expected_arguments[1][key] is not None):
                input_type     = type(kwargs[key]);
                expected_type  = type(self.__expected_arguments[1][key]);
                if(input_type != expected_type):
                    raise TypeError("@arguments:Invalid argument type provided = {0}, expecting a type of {1}.".format(input_type,expected_type));
            self.__expected_arguments[1][key] = kwargs[key];
        return True;
    
    @property
    def expected_arguments(self):
        return self.__expected_arguments;


if __name__ =="__main__":
    #Test class 
    @argument_validator(name=None, age=89)
    class __Person(object):
         def __init__(self, filename ,**kwargs):
             self.Name  =  kwargs['name'];
             self.Age   =  kwargs['age']
             print(self.Age);
             print(filename);
         
         
    args  = __Person("FileN");
    print(args.Name)
    
