import os
import sys
import configparser

class feature_enabled(object):
    def __init__(self, feature, fallback):
        self.feature = feature
        self.fallback = fallback
        self.feature_enabled = False
        config_dir = os.path.dirname(os.path.abspath(sys.argv[0])) + '/../conf/'
        self.local_config = configparser.ConfigParser()
        self.local_config.optionxform = lambda option: option  ### maintain case of keys
        self.local_config.read(config_dir+"/feature.conf")
        self.feature_switches = self.local_config['Feature_Switches']
        #read in all feature flags under specifice section of your config or shared config
        
        
    def __call__(self, original_func):
        decorator_self = self
        #print(original_func)
        
        def wrappee( *args, **kwargs):
            if not decorator_self.feature in decorator_self.feature_switches:
                decorator_self.feature_enabled = False
                #if no flag exists then set force fallback
            else:    
                decorator_self.feature_enabled=decorator_self.local_config.getboolean('Feature_Switches', decorator_self.feature)
            if decorator_self.feature_enabled:
                #if flag is there and enabled then allow feature through
                original_func(*args,**kwargs)
            else:
                decorator_self.fallback()
                #else go to fall back as defined - could have separate or shared fallbacks, dealers choice
                
        return wrappee
  
#fallback function has to be defined before you can pass it
def feature_banana_fallback():
    print("feature_banana_fallback")
    return "feature_banana_fallback"

#define features as method with decorators 
@feature_enabled("banana", feature_banana_fallback)
def feature_banana(argument1):
    print("feature_banana enabled")
    print(argument1)
    return "feature_banana"
 
  
#fallback function has to be defined before you can pass it
def feature_cranberry_fallback():
    print("feature_cranberry_fallback")
    return "feature_cranberry_fallback"
  
@feature_enabled("cranberry", feature_cranberry_fallback)
def feature_cranberry(argument1):
    print("feature cranberry enabled")
    print(argument1)
    return "feature cranberry"

#calls to features can remain in code regardless of whether they are used or not
feature_cranberry("arg1")
#illustrations also allow for passing of parameters through methods (arg2 below)
feature_banana("arg2")
