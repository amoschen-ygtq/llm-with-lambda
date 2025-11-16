from pydantic import BaseModel, Field, field_validator


class OnlineCourse(BaseModel):
    """Information about an online course."""

    title: str = Field(..., description="The title of the online course")
    instructor: str = Field(..., description="The name of the course instructor")
    platform: str = Field(..., description="The platform where the course is hosted")
    url: str = Field(..., description="The URL of the online course")
    description: str = Field(
        ..., description="A brief description of the course content"
    )
    duration_hours: float | None = Field(
        None, description="The total duration of the course in hours"
    )
    level: str | None = Field(
        None,
        description="The difficulty level of the course (e.g., Beginner, Intermediate, Advanced)",
    )
    rating: float | None = Field(
        None, description="The average user rating of the course"
    )
    num_reviews: int | None = Field(
        None, description="The number of user reviews for the course"
    )

    @field_validator("duration_hours", "rating", "num_reviews", mode="before")
    @classmethod
    def strip_commas(cls, v: object) -> object:
        if isinstance(v, str):
            return v.replace(",", "")
        return v
