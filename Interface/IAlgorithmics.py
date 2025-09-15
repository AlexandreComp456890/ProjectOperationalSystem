from abc import ABC, abstractmethod

class IAlgorithmics(ABC):
    @abstractmethod
    def shortest_job_first(self):
        pass
    
    @abstractmethod
    def round_ribbon(self):
        '''
        :params self:
        '''
        pass
    
    @abstractmethod
    def priority(self):
        pass