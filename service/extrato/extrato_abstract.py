from abc import ABC, abstractmethod

class ExtratoAbstract(ABC):
    
    @abstractmethod
    def obter_extrato(self):
        pass
    
    @abstractmethod
    def gravar_extrato(self, extrato: list[dict]) -> None:
        pass