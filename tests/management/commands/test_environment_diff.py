from unittest import mock
import io
import pytest

from django.core.management import call_command

from directory_components.management.commands import helpers


@pytest.fixture(autouse=True)
def mock_client():
    patched = mock.patch('hvac.Client', mock.Mock(is_authenticated=True))
    yield patched.start()
    patched.stop()


@pytest.fixture(autouse=True)
def mock_get_secrets():
    patched = mock.patch.object(
        helpers,
        'get_secrets',
        return_value={'EXAMPLE_A': True, 'EXAMPLE_B': False}
    )
    yield patched.start()
    patched.stop()


def test_environment_diff(mock_get_secrets):
    mock_get_secrets.side_effect = [
        {'FOO': True, 'BAZ': True},
        {'BAR': False, 'BOX': False},
    ]
    out = io.StringIO()

    call_command(
        'environment_diff',
        project='example-project',
        environment_a='example-environment-a',
        environment_b='example-environment-a',
        token='secret-token',
        domain='example.com',
        stdout=out
    )
    out.seek(0)
    result = out.read()

    assert result == (
        "- {'BAZ': True, 'FOO': True}\n+ {'BAR': False, 'BOX': False}\n"
    )


@mock.patch.object(helpers, 'get_secrets_wizard')
def test_wizard(mock_get_secrets_wizard):
    mock_get_secrets_wizard.side_effect = [
        {'FOO': True, 'BAZ': True},
        {'BAR': False, 'BOX': False},
    ]
    out = io.StringIO()

    call_command(
        'environment_diff',
        token='secret-token',
        domain='example.com',
        wizard=True,
        stdout=out
    )
    out.seek(0)
    result = out.read()

    assert result == (
        "- {'BAZ': True, 'FOO': True}\n+ {'BAR': False, 'BOX': False}\n"
    )
