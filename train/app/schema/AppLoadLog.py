from pydantic import BaseModel

class AppLoadLogV3(BaseModel):
    game_code : str
    os : str
    os_version : str
    crash_sdk_version : str
    app_version : str
    package_name : str
    user_key : str
    model : str
    device_id : str
    geo : str
    city : str
    report_datetime : str
    memory_warning : str
    carrier : str
    session_key : str
    emulator : str
    network_kind : str
    vendor_user_key : str
    vendor_device_id : str

    class Config:
        orm_mode = True

