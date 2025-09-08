from pydantic import BaseModel, Field

class MovimentosPagbankParams(BaseModel):
    data_movimento: str = Field(..., alias="dataMovimento", description="Data do movimento no formato YYYY-MM-DD")
    page_number: int = Field(..., alias="pageNumber", ge=1, description="Número da página da consulta")
    page_size: int = Field(..., alias="pageSize", ge=1, le=1000, description="Quantidade de registros por página")
    tipo_movimento: int = Field(..., alias="tipoMovimento", description="Tipo de movimento")
    
    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True)

if __name__ == "__main__":
    # Exemplo de uso
    params = MovimentosPagbankParams(
        data_movimento="2025-06-13",
        page_number=1,
        page_size=10,
        tipo_movimento=2
    )
    print(params.to_dict())
    # Saída esperada: {'dataMovimento': '2025-06-13', 'pageNumber': 1, 'pageSize': 10, 'tipoMovimento': 2}