from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, constr
from tortoise.contrib.pydantic import pydantic_model_creator

from db_setup import initiate_db
from models import Users, TestResults, TestSession, FatigueTest

initiate_db()

User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
Test_Results_Pydantic = pydantic_model_creator(TestResults, name="TestResults")
Test_ResultsIn_Pydantic = pydantic_model_creator(TestResults, name="TestResults", exclude_readonly=True)
Test_Session_Pydantic = pydantic_model_creator(TestSession, name="TestSession")
Test_Fatigue_Pydantic = pydantic_model_creator(FatigueTest, name="FatigueTest")


class UserModel(BaseModel):
    id: int
    username: constr(max_length=24)
    role = constr(max_length=10)
    #: This will hold the auth key to the API
    age = int
    phone_number = constr(max_length=10)

    class Config:
        orm_mode = True


class FatigueTestModelIn(BaseModel):
    blink_time: Optional[datetime]
    blink_duration: Optional[float]

    class Config:
        orm_mode = True


class AttentionTestModelIn(BaseModel):
    number_shown_time: Optional[datetime]
    button_pressed_time: Optional[datetime]
    number_shown: Optional[int]
    button_pressed: Optional[int]

    class Config:
        orm_mode = True


class SessionModelIn(BaseModel):
    fatigue_test: Optional[List[FatigueTestModelIn]]
    attention_test: Optional[List[AttentionTestModelIn]]

    class Config:
        orm_mode = True


class TestResultModelIn(BaseModel):
    test_session: Optional[SessionModelIn]

    class Config:
        orm_mode = True

