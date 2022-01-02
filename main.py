# pylint: disable=E0611,E0401
from typing import List

from data_models import User_Pydantic, UserModel, UserIn_Pydantic, Test_Results_Pydantic, TestResultModelIn
from db_setup import app
from models import TestResults, Users, TestSession, FatigueTest, SustainedAttentionTest


@app.get("/users", response_model=List[UserModel])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@app.post("/users", response_model=UserModel)
async def create_user(user: UserIn_Pydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@app.get("/results/{user_id}", response_model=List[Test_Results_Pydantic])
async def get_results(user_id: int):
    return await Test_Results_Pydantic.from_queryset(TestResults.filter(user_id=user_id).all())


@app.post("/results/{user_id}", response_model=TestResultModelIn)
async def create_result(user_id: int, results: TestResultModelIn):

    test_result = TestResults(user_id=user_id)
    await test_result.save()

    session = TestSession(
        test_result=test_result,
    )
    await session.save()

    session_id = session

    fa_tests = []
    for item in results.test_session.fatigue_test:
        fa_test = FatigueTest(test_result=test_result, **item.dict())
        fa_test.test_session = session_id
        await fa_test.save()
        fa_tests.append(fa_test)

    sat_tests = []
    for item in results.test_session.attention_test:
        sat_test = SustainedAttentionTest(test_result=test_result, **item.dict())
        sat_test.test_session = session_id
        await sat_test.save()
        sat_tests.append(sat_test)
