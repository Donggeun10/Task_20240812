from fastapi import Header, HTTPException
from starlette import status


def application_vnd(content_type: str = Header(...)):
    """Require request MIME-type to be application/flatbuffers-v3 or application/flatbuffers-v4"""
    if {"application/flatbuffers-v3","application/flatbuffers-v4"}.issubset(content_type):
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,f"Unsupported media type: {content_type}. It must be application/flatbuffers-v3,v4",)