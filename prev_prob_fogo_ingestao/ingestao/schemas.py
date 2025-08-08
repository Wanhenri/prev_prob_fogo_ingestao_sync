from pydantic import BaseModel
from typing import List, Optional



class Previsao(BaseModel):
    CD_MUN: int
    NM_MUN_y: str
    SIGLA_UF: str
    AREA_KM2: float
    Sum_Frs: Optional[float]
    alerta: Optional[float]
    fc_2021: Optional[float]
    fc_2022: Optional[float]
    fc_2023: Optional[float]
    fc_2024: Optional[float]
    Trend: Optional[float]
    Secas: Optional[float]
    prev_t: Optional[float]
    prev_p: Optional[float]
    regra: Optional[str]
    ano: int
    trimestre: str
