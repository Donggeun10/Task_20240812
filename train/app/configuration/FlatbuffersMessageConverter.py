from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

from train.app.domain.AppLoadLogV3Fb import AppLoadLogV3
from train.app.domain.CrashReportMessage import InitMessage, LogVersion

class FlatBuffersRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            content_type = self.headers.get("Content-Type")
            body :bytes = await super().body()
            if content_type == "application/flatbuffers-v3":
                if self.url.path == "/api/v1/init":
                    appload_v3 = AppLoadLogV3.GetRootAsAppLoadLogV3(bytearray(body),0)
                    self._body = InitMessage(appload_v3.GameCode().decode('utf-8'),
                                             appload_v3.Os().decode('utf-8'),
                                             appload_v3.to_dict(), LogVersion.v3)
                else:
                    print("invalid url"+self.url.path)
            else:
                print("content_type :" + content_type)
        else:
            print("invalid body")

        return self._body


class FlatBuffersRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = FlatBuffersRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler