import flatbuffers
from fastapi.testclient import TestClient

from train.app.application import app
from train.app.domain import AppLoadLogV3Fb

client = TestClient(app)

def test_post_app_tracking_member():

    builder = flatbuffers.Builder(1024)

    model = builder.CreateString("SM-G950N")
    os = builder.CreateString("Android")
    os_version = builder.CreateString("1.0.0")
    crash_sdk_version = builder.CreateString("1.0.0")
    app_version = builder.CreateString("1.0.0")
    package_name = builder.CreateString("com.robokim")
    user_key = builder.CreateString("test")
    device_id = builder.CreateString("test")
    game_code = builder.CreateString("robokim")
    geo = builder.CreateString("KR")
    city = builder.CreateString("Seoul")
    report_datetime = builder.CreateString("2021-01-01 00:00:00")
    memory_warning = builder.CreateString("0")
    carrier = builder.CreateString("SKT")
    session_key = builder.CreateString("test")
    emulator = False
    network_kind = builder.CreateString("WIFI")
    vendor_user_key = builder.CreateString("test")
    vendor_device_id = builder.CreateString("test")


    AppLoadLogV3Fb.Start(builder)
    AppLoadLogV3Fb.AddGameCode(builder, game_code)
    AppLoadLogV3Fb.AddOs(builder, os)
    AppLoadLogV3Fb.AddOsVersion(builder, os_version)
    AppLoadLogV3Fb.AddCrashSdkversion(builder, crash_sdk_version)
    AppLoadLogV3Fb.AddAppVersion(builder, app_version)
    AppLoadLogV3Fb.AddPackageName(builder, package_name)
    AppLoadLogV3Fb.AddModel(builder, model)
    AppLoadLogV3Fb.AddUserKey(builder, user_key)
    AppLoadLogV3Fb.AddDeviceId(builder, device_id)
    AppLoadLogV3Fb.AddGeo(builder, geo)
    AppLoadLogV3Fb.AddCity(builder, city)
    AppLoadLogV3Fb.AddReportDatetime(builder, report_datetime)
    AppLoadLogV3Fb.AddMemoryWarning(builder, memory_warning)
    AppLoadLogV3Fb.AddCarrier(builder, carrier)
    AppLoadLogV3Fb.AddSessionKey(builder, session_key)
    AppLoadLogV3Fb.AddEmulator(builder, emulator)
    AppLoadLogV3Fb.AddNetworkKind(builder, network_kind)
    AppLoadLogV3Fb.AddVendorUserKey(builder, vendor_user_key)
    AppLoadLogV3Fb.AddVendorDeviceId(builder, vendor_device_id)

    appload_v3 = AppLoadLogV3Fb.End(builder)
    builder.Finish(appload_v3)
    appload_v3 = builder.Output()

    print("apploadV3 : " + str(appload_v3))

    response = client.post(url= "/api/v1/init", content=bytes(appload_v3),
                           headers={"Content-Type": "application/flatbuffers-v3"})
    assert response.status_code == 200


