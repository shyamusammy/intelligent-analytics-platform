from pydantic import BaseModel, Field


class DashboardChart(BaseModel):
    title: str
    chart_type: str
    data: dict


class DashboardResult(BaseModel):
    charts: list[DashboardChart] = Field(default_factory=list)
