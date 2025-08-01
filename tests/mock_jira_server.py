# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import annotations

from re import DOTALL, IGNORECASE, match, search
from typing import Optional

from requests import Response
from requests_mock import Adapter
from requests_mock.request import _RequestObjectProxy
from requests_mock.response import create_response


class CustomMatcherFactory:
    response_status_code: int

    def __init__(self, response_status_code: int = 200):
        self.response_status_code = response_status_code

    def custom_matcher(self, request: _RequestObjectProxy) -> Optional[Response]:
        if (
            search(pattern="^/rest/api/2/field", string=request.path, flags=IGNORECASE)
            is not None
        ):
            return mock_get_all_fields_response(
                request, status_code=self.response_status_code
            )
        if (
            search(pattern="^/rest/api/2/myself", string=request.path, flags=IGNORECASE)
            is not None
        ):
            return mock_get_myself_response(
                request, status_code=self.response_status_code
            )
        if (
            search(
                pattern="^/rest/api/2/serverinfo", string=request.path, flags=IGNORECASE
            )
            is not None
        ):
            return mock_get_server_info_response(
                request, status_code=self.response_status_code
            )
        if (
            search(
                pattern=r"^/rest/api/2/project/\w{1,}$",
                string=request.path,
                flags=IGNORECASE,
            )
            is not None
        ):
            return mock_get_project_detail_response(
                request, status_code=self.response_status_code
            )
        if (
            search(
                pattern="^/rest/api/2/project$", string=request.path, flags=IGNORECASE
            )
            is not None
        ):
            return mock_get_all_projects_response(
                request, status_code=self.response_status_code
            )
        if (
            match(
                pattern=r"^/rest/api/2/issue$",
                string=request.path,
                flags=IGNORECASE | DOTALL,
            )
            is not None
        ):
            return mock_create_issue_response(
                request, status_code=self.response_status_code
            )
        if (
            match(
                pattern=r"^/rest/api/2/issue/createmeta/\w{1,}?/issuetypes$",
                string=request.path,
                flags=IGNORECASE | DOTALL,
            )
            is not None
        ):
            return mock_get_project_issue_types_response(
                request, status_code=self.response_status_code
            )
        if (
            match(
                pattern=r"^/rest/api/2/issue/createmeta/\w{1,}?/issuetypes/\w{1,}?$",
                string=request.path,
                flags=IGNORECASE | DOTALL,
            )
            is not None
        ):
            return mock_get_project_issue_fields_response(
                request, status_code=self.response_status_code
            )
        return None


def mock_jira_requests(response_status_code: int = 200) -> Adapter:
    adapter = Adapter(False)
    adapter.add_matcher(CustomMatcherFactory(response_status_code).custom_matcher)
    return adapter


def mock_get_server_info_response(
    request: _RequestObjectProxy, status_code: int = 200
) -> Response:
    return create_response(
        request=request,
        status_code=status_code,
        reason="Bad Request" if status_code == 400 else "OK",
        json={
            "baseUrl": "https://your_jira.com",
            "version": "8.20.13",
            "versionNumbers": [8, 20, 13],
            "deploymentType": "Server",
            "buildNumber": 820013,
            "buildDate": "2022-09-21T00:00:00.000-0700",
            "databaseBuildNumber": 820013,
            "serverTime": "2023-03-29T00:15:35.205-0700",
            "scmInfo": "e83256f8976830734d21b999890eb027cb94ffc2",
            "serverTitle": "YourJira",
        },
    )


def mock_get_myself_response(
    request: _RequestObjectProxy, status_code: int = 200
) -> Response:
    return create_response(
        request=request,
        status_code=status_code,
        reason="Bad Request" if status_code == 400 else "OK",
        json={
            "self": "https://your_jira.com/rest/api/2/user?username=sharry.xu",
            "key": "sharry.xu",
            "name": "sharry.xu",
            "emailAddress": "sharry.xu@company.com",
            "avatarUrls": {
                "48x48": "https://your_jira.com/secure/useravatar?ownerId=sharry.xu&avatarId=17002",
                "24x24": "https://your_jira.com/secure/useravatar?size=small&ownerId=sharry.xu&avatarId=17002",
                "16x16": "https://your_jira.com/secure/useravatar?size=xsmall&ownerId=sharry.xu&avatarId=17002",
                "32x32": "https://your_jira.com/secure/useravatar?size=medium&ownerId=sharry.xu&avatarId=17002",
            },
            "displayName": "Sharry Xu",
            "active": True,
            "deleted": False,
            "timeZone": "Asia/Shanghai",
            "locale": "en_US",
            "groups": {"size": 91, "items": []},
            "applicationRoles": {"size": 1, "items": []},
            "expand": "groups,applicationRoles",
        },
    )


def mock_get_all_fields_response(
    request: _RequestObjectProxy, status_code: int = 200
) -> Response:
    return create_response(
        request=request,
        status_code=status_code,
        reason="Bad Request" if status_code == 400 else "OK",
        json=[
            {
                "id": "customfield_14303",
                "name": "Script Execution Order",
                "custom": True,
                "orderable": True,
                "navigable": True,
                "searchable": True,
                "clauseNames": ["cf[14303]", "Script Execution Order"],
                "schema": {
                    "type": "string",
                    "custom": "com.atlassian.jira.plugin.system.customfieldtypes:textarea",
                    "customId": 14303,
                },
            },
            {
                "id": "status",
                "name": "Status",
                "custom": False,
                "orderable": False,
                "navigable": True,
                "searchable": True,
                "clauseNames": ["status"],
                "schema": {"type": "status", "system": "status"},
            },
            {
                "id": "comment",
                "name": "Comment",
                "custom": False,
                "orderable": True,
                "navigable": False,
                "searchable": True,
                "clauseNames": ["comment"],
                "schema": {"type": "comments-page", "system": "comment"},
            },
            {
                "id": "customfield_15601",
                "name": "Domain",
                "custom": True,
                "orderable": True,
                "navigable": True,
                "searchable": True,
                "clauseNames": ["cf[15601]", "Domain"],
                "schema": {
                    "type": "option",
                    "custom": "com.atlassian.jira.plugin.system.customfieldtypes:select",
                    "customId": 15601,
                },
            },
            {
                "id": "description",
                "name": "Description",
                "custom": False,
                "orderable": True,
                "navigable": True,
                "searchable": True,
                "clauseNames": ["description"],
                "schema": {"type": "string", "system": "description"},
            },
        ],
    )


def mock_get_project_detail_response(
    request: _RequestObjectProxy, status_code: int = 200
) -> Response:
    return create_response(
        request=request,
        status_code=status_code,
        reason="Bad Request" if status_code == 400 else "OK",
        json={
            "expand": "description,lead,issueTypes,url,projectKeys,permissions,insight",
            "self": "https://your_jira.com/rest/api/2/project/10000",
            "id": "10000",
            "key": "SD",
            "description": "",
            "lead": {
                "self": "https://your_jira.com/rest/api/2/user?accountId=557058:c9b9c393-abd3-45a5-ac41-b3c2f5e2d96c",
                "accountId": "557058:c9b9c393-abd3-45a5-ac41-b3c2f5e2d96c",
                "avatarUrls": {
                    "48x48": "https://secure.gravatar.com/avatar/FAT-2.png",
                    "24x24": "https://secure.gravatar.com/avatar/FAT-2.png",
                    "16x16": "https://secure.gravatar.com/avatar/FAT-2.png",
                    "32x32": "https://secure.gravatar.com/avatar/FAT-2.png",
                },
                "displayName": "Good Know",
                "active": True,
            },
            "components": [],
            "issueTypes": [
                {
                    "self": "https://your_jira.com/rest/api/2/issuetype/10002",
                    "id": "10002",
                    "description": "A task that needs to be done.",
                    "iconUrl": "https://your_jira.com/rest/api/2/universal_avatar/view/type/issuetype/avatar/10552?size=medium",
                    "name": "Task",
                    "subtask": False,
                    "avatarId": 10552,
                    "hierarchyLevel": 0,
                },
                {
                    "self": "https://your_jira.com/rest/api/2/issuetype/10003",
                    "id": "10003",
                    "description": "The sub-task of the issue",
                    "iconUrl": "https://your_jira.com/rest/api/2/universal_avatar/view/type/issuetype/avatar/10553?size=medium",
                    "name": "Sub-task",
                    "subtask": True,
                    "avatarId": 10553,
                    "hierarchyLevel": -1,
                },
                {
                    "self": "https://your_jira.com/rest/api/2/issuetype/10001",
                    "id": "10001",
                    "description": "For general requests",
                    "iconUrl": "https://your_jira.com/rest/api/2/universal_avatar/view/type/issuetype/avatar/10551?size=medium",
                    "name": "General request",
                    "subtask": True,
                    "avatarId": 10551,
                    "hierarchyLevel": 0,
                },
                {
                    "self": "https://your_jira.com/rest/api/2/issuetype/10150",
                    "id": "10150",
                    "description": "For requests that require approval.",
                    "iconUrl": "https://your_jira.com/rest/api/2/universal_avatar/view/type/issuetype/avatar/10306?size=medium",
                    "name": "Service Request with Approvals",
                    "subtask": False,
                    "avatarId": 10306,
                    "hierarchyLevel": 0,
                },
            ],
            "url": "https://your_jira.site/portal/1",
            "assigneeType": "UNASSIGNED",
            "versions": [],
            "name": "Sandbox",
            "roles": {},
            "avatarUrls": {
                "48x48": "https://your_jira.com/rest/api/2/universal_avatar/view/type/project/avatar/10414",
                "24x24": "https://your_jira.com/rest/api/2/universal_avatar/view/type/project/avatar/10414?size=small",
                "16x16": "https://your_jira.com/rest/api/2/universal_avatar/view/type/project/avatar/10414?size=xsmall",
                "32x32": "https://your_jira.com/rest/api/2/universal_avatar/view/type/project/avatar/10414?size=medium",
            },
            "projectTypeKey": "service_desk",
            "simplified": False,
            "style": "classic",
            "isPrivate": False,
            "properties": {},
        },
    )


def mock_get_all_projects_response(
    request: _RequestObjectProxy, status_code: int = 200
) -> Response:
    return create_response(
        request=request,
        status_code=status_code,
        reason="Bad Request" if status_code == 400 else "OK",
        json=[
            {
                "expand": "description,lead,url,projectKeys",
                "self": "https://your_jira.com/rest/api/2/project/15200",
                "id": "15200",
                "key": "POC",
                "name": "POC",
                "avatarUrls": {
                    "48x48": "https://your_jira.com/secure/projectavatar?avatarId=13903",
                    "24x24": "https://your_jira.com/secure/projectavatar?size=small&avatarId=13903",
                    "16x16": "https://your_jira.com/secure/projectavatar?size=xsmall&avatarId=13903",
                    "32x32": "https://your_jira.com/secure/projectavatar?size=medium&avatarId=13903",
                },
                "projectTypeKey": "software",
            },
            {
                "expand": "description,lead,url,projectKeys",
                "self": "https://your_jira.com/rest/api/2/project/11503",
                "id": "11503",
                "key": "APPSEC",
                "name": "Application Security",
                "avatarUrls": {
                    "48x48": "https://your_jira.com/secure/projectavatar?pid=11503&avatarId=16004",
                    "24x24": "https://your_jira.com/secure/projectavatar?size=small&pid=11503&avatarId=16004",
                    "16x16": "https://your_jira.com/secure/projectavatar?size=xsmall&pid=11503&avatarId=16004",
                    "32x32": "https://your_jira.com/secure/projectavatar?size=medium&pid=11503&avatarId=16004",
                },
                "projectTypeKey": "software",
            },
            {
                "expand": "description,lead,url,projectKeys",
                "self": "https://your_jira.com/rest/api/2/project/15200",
                "id": "10100",
                "key": "SD",
                "name": "Sandbox",
                "avatarUrls": {
                    "48x48": "https://your_jira.com/secure/projectavatar?avatarId=13903",
                    "24x24": "https://your_jira.com/secure/projectavatar?size=small&avatarId=13903",
                    "16x16": "https://your_jira.com/secure/projectavatar?size=xsmall&avatarId=13903",
                    "32x32": "https://your_jira.com/secure/projectavatar?size=medium&avatarId=13903",
                },
                "projectTypeKey": "software",
            },
        ],
    )


def mock_get_project_issue_types_response(
    request: _RequestObjectProxy, status_code: int = 200
) -> Response:
    return create_response(
        request=request,
        status_code=status_code,
        reason="Bad Request" if status_code == 400 else "OK",
        json={
            "maxResults": 50,
            "startAt": 0,
            "total": 7,
            "isLast": True,
            "values": [
                {
                    "self": "https://your_jira.com/rest/api/2/issuetype/10500",
                    "id": "10500",
                    "description": "Represents a Production Release item",
                    "iconUrl": "https://your_jira.com/secure/viewavatar?size=xsmall&avatarId=12207&avatarType=issuetype",
                    "name": "Release",
                    "subtask": False,
                },
                {
                    "self": "https://your_jira.com/rest/api/2/issuetype/10700",
                    "id": "10700",
                    "description": "Hotfix release",
                    "iconUrl": "https://your_jira.com/secure/viewavatar?size=xsmall&avatarId=12208&avatarType=issuetype",
                    "name": "Hotfix",
                    "subtask": False,
                },
                {
                    "self": "https://your_jira.com/rest/api/2/issuetype/11",
                    "id": "11",
                    "description": "",
                    "iconUrl": "https://your_jira.com/secure/viewavatar?size=xsmall&avatarId=12211&avatarType=issuetype",
                    "name": "Request",
                    "subtask": False,
                },
                {
                    "self": "https://your_jira.com/rest/api/2/issuetype/11000",
                    "id": "11000",
                    "description": "",
                    "iconUrl": "https://your_jira.com/secure/viewavatar?size=xsmall&avatarId=12206&avatarType=issuetype",
                    "name": "Server Config",
                    "subtask": False,
                },
                {
                    "self": "https://your_jira.com/rest/api/2/issuetype/12500",
                    "id": "12500",
                    "description": "Production Release",
                    "iconUrl": "https://your_jira.com/secure/viewavatar?size=xsmall&avatarId=12210&avatarType=issuetype",
                    "name": "Release Support",
                    "subtask": False,
                },
                {
                    "self": "https://your_jira.com/rest/api/2/issuetype/14",
                    "id": "14",
                    "description": "",
                    "iconUrl": "https://your_jira.com/images/icons/issuetypes/undefined.png",
                    "name": "Research",
                    "subtask": False,
                },
                {
                    "self": "https://your_jira.com/rest/api/2/issuetype/7",
                    "id": "7",
                    "description": "Created by Jira Software - do not edit or delete. Issue type for a user story.",
                    "iconUrl": "https://your_jira.com/secure/viewavatar?size=xsmall&avatarId=12215&avatarType=issuetype",
                    "name": "Story",
                    "subtask": False,
                },
            ],
        },
    )


def mock_get_project_issue_fields_response(
    request: _RequestObjectProxy, status_code: int = 200
) -> Response:
    return create_response(
        request=request,
        status_code=status_code,
        reason="Bad Request" if status_code == 400 else "OK",
        json={
            "maxResults": 50,
            "startAt": 0,
            "total": 5,
            "isLast": True,
            "values": [
                {
                    "required": True,
                    "schema": {"type": "issuetype", "system": "issuetype"},
                    "name": "Issue Type",
                    "fieldId": "issuetype",
                    "hasDefaultValue": False,
                    "operations": [],
                    "allowedValues": [
                        {
                            "self": "https://your_jira.com/rest/api/2/issuetype/7",
                            "id": "7",
                            "description": "Created by Jira Software - do not edit or delete. Issue type for a user story.",
                            "iconUrl": "https://your_jira.com/secure/viewavatar?size=xsmall&avatarId=12215&avatarType=issuetype",
                            "name": "Story",
                            "subtask": False,
                            "avatarId": 12215,
                        }
                    ],
                },
                {
                    "required": False,
                    "schema": {
                        "type": "option",
                        "custom": "com.atlassian.jira.plugin.system.customfieldtypes:select",
                        "customId": 11700,
                    },
                    "name": "HTC Approved",
                    "fieldId": "customfield_11700",
                    "hasDefaultValue": False,
                    "operations": ["set"],
                    "allowedValues": [
                        {
                            "self": "https://your_jira.com/rest/api/2/customFieldOption/12602",
                            "value": "Yes",
                            "id": "12602",
                            "disabled": False,
                        }
                    ],
                },
                {
                    "required": False,
                    "schema": {
                        "type": "option",
                        "custom": "com.atlassian.jira.plugin.system.customfieldtypes:select",
                        "customId": 12426,
                    },
                    "name": "Deployment Impact",
                    "fieldId": "customfield_12426",
                    "hasDefaultValue": False,
                    "operations": ["set"],
                    "allowedValues": [
                        {
                            "self": "https://your_jira.com/rest/api/2/customFieldOption/13483",
                            "value": "Low",
                            "id": "13483",
                            "disabled": False,
                        },
                        {
                            "self": "https://your_jira.com/rest/api/2/customFieldOption/13484",
                            "value": "Medium",
                            "id": "13484",
                            "disabled": False,
                        },
                        {
                            "self": "https://your_jira.com/rest/api/2/customFieldOption/13485",
                            "value": "High",
                            "id": "13485",
                            "disabled": False,
                        },
                    ],
                },
                {
                    "required": True,
                    "schema": {"type": "string", "system": "summary"},
                    "name": "Summary",
                    "fieldId": "summary",
                    "hasDefaultValue": False,
                    "operations": ["set"],
                },
                {
                    "required": False,
                    "schema": {"type": "string", "system": "description"},
                    "name": "Description",
                    "fieldId": "description",
                    "hasDefaultValue": False,
                    "operations": ["set"],
                },
                {
                    "required": True,
                    "schema": {
                        "type": "array",
                        "items": "myvalue",
                        "system": "myvalue",
                    },
                    "name": "My Value",
                    "fieldId": "MyValue",
                    "hasDefaultValue": False,
                    "operations": ["set"],
                    "allowedValues": [
                        {
                            "self": "https://your_jira.com/rest/api/2/customFieldOption/13483",
                            "value": "1",
                            "id": "13483",
                            "avataUrls": {
                                "48*48": "www.abc.com",
                                "24*24": "www.cde.com",
                            },
                            "disabled": False,
                        },
                        {
                            "self": "https://your_jira.com/rest/api/2/customFieldOption/13484",
                            "value": "2",
                            "id": "13484",
                            "avataUrls": {
                                "48*48": "www.abc.com",
                                "24*24": "www.cde.com",
                            },
                            "disabled": False,
                        },
                        {
                            "self": "https://your_jira.com/rest/api/2/customFieldOption/13485",
                            "value": "3",
                            "id": "13485",
                            "avataUrls": {
                                "48*48": "www.abc.com",
                                "24*24": "www.cde.com",
                            },
                            "disabled": True,
                        },
                    ],
                },
            ],
        },
    )


def mock_create_issue_response(
    request: _RequestObjectProxy, status_code: int = 200
) -> Response:
    return create_response(
        request=request,
        status_code=status_code,
        reason="Bad Request" if status_code == 400 else "OK",
        json={
            "id": "1252056",
            "key": "SD-123",
            "self": "https://your_jira.com/rest/api/2/issue/1252056",
        },
    )


def mock_jira_requests_with_error_response() -> Adapter:
    adapter = Adapter(False)
    adapter.add_matcher(custom_matcher_with_error_response)
    return adapter


def custom_matcher_with_error_response(
    request: _RequestObjectProxy,
) -> Optional[Response]:
    if (
        search(pattern="rest/api/2/myself", string=request.path, flags=IGNORECASE)
        is not None
    ):
        return mock_get_myself_response(request, status_code=200)
    if (
        search(pattern="rest/api/2/serverinfo", string=request.path, flags=IGNORECASE)
        is not None
    ):
        # Server info should be 200, otherwise, following tests cannot be executed as expected.
        return mock_get_server_info_response(request, status_code=200)
    if (
        search(pattern="rest/api/2/search", string=request.path, flags=IGNORECASE)
        is not None
    ):
        return mock_search_with_error_response(request)
    if (
        search(pattern="rest/api/2/field", string=request.path, flags=IGNORECASE)
        is not None
    ):
        return mock_get_all_fields_response(request, status_code=200)
    if (
        match(
            pattern=r"^/rest/api/2/issue$",
            string=request.path,
            flags=IGNORECASE | DOTALL,
        )
        is not None
    ):
        return mock_create_issue_with_error_response(request)
    return None


def mock_create_issue_with_error_response(request: _RequestObjectProxy) -> Response:
    return create_response(
        request=request,
        status_code=400,
        json={"errorMessages": [], "errors": {"issuetype": "issue type is required"}},
    )


def mock_search_with_error_response(request: _RequestObjectProxy) -> Response:
    return create_response(
        request=request,
        status_code=400,
        json={
            "errorMessages": [
                "Error in the JQL Query: The quoted string ')' has not been completed. (line 1, character 8)"
            ],
            "errors": {},
        },
    )
