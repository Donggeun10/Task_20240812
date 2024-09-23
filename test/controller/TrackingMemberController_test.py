import base64
from datetime import datetime

from fastapi.testclient import TestClient

from train.app.application import app
from train.app.schema.App_tracking_member import app_tracking_member_create

client = TestClient(app)

def test_get_hello():
    with TestClient(app) as client:
        # basic authentication is required
        token = make_basic_auth_token("robot", "play")
        response = client.get("/hello", headers={"Authorization": f"Basic {token}"})
        assert response.status_code == 200


def test_get_app_tracking_members():
    with TestClient(app) as client:
        response = client.get("/app-tracking-members")
        assert response.status_code == 200


def test_post_app_tracking_member():
    with TestClient(app) as client:
        current_datetime = datetime.now()
        current_date_time = current_datetime.strftime("%Y%m%d%H%M%S")
        member = app_tracking_member_create(title_code="tc", market_os="mo",
                                            user_id="user_id_"+current_date_time, user_name="user_name_"+current_date_time)

        print("member.user_id : " + member.user_id)
        response = client.post(url= "/app-tracking-member", json=member.to_dict(),
                               headers={"Content-Type": "application/json"})
        assert response.status_code == 201

def test_put_app_tracking_member():
    with TestClient(app) as client:
        current_datetime = datetime.now()
        current_date_time = current_datetime.strftime("%Y%m%d%H%M%S")
        user_id = "user_id_"+current_date_time
        member = app_tracking_member_create(title_code="tc", market_os="mo", user_id=user_id, user_name="user_name_"+current_date_time)

        print("member.user_id : " + member.user_id)
        response = client.put(url= "/app-tracking-member/"+user_id,
                              json=member.to_dict(),
                               headers={"Content-Type": "application/json"})
        assert response.status_code == 404

# generate a basic authentication token
def make_basic_auth_token(username: str, password: str) -> str:
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    return encoded_credentials