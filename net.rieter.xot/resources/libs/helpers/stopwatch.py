#===============================================================================
# LICENSE Retrospect-Framework - CC BY-NC-ND
#===============================================================================
# This work is licenced under the Creative Commons 
# Attribution-Non-Commercial-No Derivative Works 3.0 Unported License. To view a 
# copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/3.0/ 
# or send a letter to Creative Commons, 171 Second Street, Suite 300, 
# San Francisco, California 94105, USA.
#===============================================================================
import time


class StopWatch:
    """Class for time measurements and performance
    
    ATV2 is about 30 slower then the DEV PC
    """
    
    def __init__(self, name, logger):
        """Create an instance of a stopwatch with a certain logger
        
        Arguments:
        name   : string       - ID of the stopwatch.
        logger : Customlogger - Logger to write to.
        
        """
        
        if name is None or name == "" or logger is None:
            raise ValueError("Name or logger not specified")
        
        self.logger = logger
        self.name = name
        
        self.startTime = None
        self.lapTime = None
        self.stopTime = None
        
        self.set()
        return
    
    def stop(self):
        """Stops the stopwatch and prints the time elapsed."""
        
        self.stopTime = time.time()
        seconds_taken = self.stopTime - self.startTime
        
        if self.lapTime:
            delta = self.stopTime - self.lapTime
        else:
            delta = self.stopTime - self.startTime
            
        self.logger.debug("Stopwatch :: Stop (%s): %s, time elapsed: %s ms (+%s ms)",
                          self.name, self.stopTime, seconds_taken * 1000, delta * 1000)
        return
        
    def set(self):
        """Starts the stopwatch and prints the start time."""
        
        self.startTime = time.time()
        self.logger.debug("Stopwatch :: Set (%s): %s", self.name, self.startTime)
        return
        
    def lap(self, value=""):
        """Laps the stopwatch and prints the elapsed time. The stopwatch 
        does not stop.
        
        Keyword Arguments:
        value : string - Label to print with the Lap action.
        
        """
        now = time.time()
        
        if self.lapTime:
            delta = now - self.lapTime
        else:
            delta = now - self.startTime
        
        self.lapTime = now
        seconds_taken = self.lapTime - self.startTime
        self.logger.debug("Stopwatch :: Lap (%s) %s: elapsed since start: %s ms (delta +%s ms)",
                          self.name, value, seconds_taken * 1000, delta * 1000)
           
    def __str__(self):
        """String representation of this class."""
        
        return "Stopwatch: [%s]" % (self.name, )
