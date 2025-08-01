import pytest
from requests_mock import Mocker

from jira_cloud_api.jira_cloud_api import JiraApi, JiraApiOptions
from jira_cloud_api.jira_request import (
    CreateIssueRequest,
    GetProjectIssueFieldsRequest,
    GetProjectIssueTypesRequest,
)
from tests.mock_jira_server import mock_jira_requests

DEFAULT_jira_cloud_api_OPTIONS = JiraApiOptions(
    url="https://localhost",
    access_token="access_token",
    user_email="sharry.xu@outlook.com",
)

jira_cloud_api = JiraApi(DEFAULT_jira_cloud_api_OPTIONS)


def test_jira_cloud_api_constructor():
    with pytest.raises(ValueError) as e:
        _ = JiraApi(
            JiraApiOptions(
                url="https://localhost.atlassian.net",
                access_token="access_token",
            )
        )

        assert "User email must be provided" in str(e.value)


def test_get_server_info():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        response = jira_cloud_api.get_server_info()

        assert response is not None


def test_get_server_info_failed():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(response_status_code=400),
    ):
        response = jira_cloud_api.get_server_info()

        assert response.status_code == 400


def test_get_myself():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        response = jira_cloud_api.get_myself()

        assert response is not None


def test_get_all_projects():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        respose = jira_cloud_api.get_all_projects()

        assert respose is not None


def test_get_project_detail():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        respose = jira_cloud_api.get_project_detail("SAND")

        assert respose is not None


def test_get_project_issue_types():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        respose = jira_cloud_api.get_project_issue_types(
            GetProjectIssueTypesRequest(
                project_id_or_key="SAND", start_at=0, max_results=1, query_all=True
            )
        )

        assert respose is not None


def test_get_all_fields():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        respose = jira_cloud_api.get_all_fields()

        assert respose is not None


def test_get_project_issue_fields():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        respose = jira_cloud_api.get_project_issue_fields(
            GetProjectIssueFieldsRequest(
                project_id_or_key="SAND",
                issue_type_id="10002",
                start_at=0,
                max_results=1,
                query_all=True,
            )
        )

        assert respose is not None


def test_create_issue():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        respose = jira_cloud_api.create_issue(
            CreateIssueRequest(
                fields={
                    "project.key": "SAND",
                    "project.id": "10000",
                    "summary": "Test issue creation",
                    "description": "This is a test issue created via API.",
                    "issuetype.id": "10002",
                }
            )
        )

        assert respose is not None
