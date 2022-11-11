class Empresa:
    def __init__(self, 
                 CNPJ:str=None, 
                 nomefantasia:str=None,
                 razaosocial:str=None,
                ):
        self.set_CNPJ(CNPJ)
        self.set_nomefantasia(nomefantasia)
        self.set_razaosocial(razaosocial)

    def set_CNPJ(self, CNPJ:str):
        self.CNPJ = CNPJ

    def set_nomefantasia(self, nomefantasia:str):
        self.nomefantasia = nomefantasia
        
    def set_razaosocial(self, razaosocial:str):
        self.razaosocial = razaosocial

    def get_CNPJ(self) -> str:
        return self.CNPJ

    def get_nomefantasia(self) -> str:
        return self.nomefantasia
        
    def get_razaosocial(self) -> str:
        return self.razaosocial
    
    def to_string(self) -> str:
        return f"CNPJ: {self.get_cnpj()} | Razão Social: {self.get_razaosocial()} | Nome Fantasia: {self.get_nomefantasia()}"