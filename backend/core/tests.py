import pytest

pytestmark = pytest.mark.django_db


def test_homepage(client):
    """
    sanity check for the homepage
    """
    res = client.get('/')
    assert res.status_code == 200


def test_login(client):
    """
    sanity check for the login
    """
    res = client.get('/login')
    assert res.status_code == 200


def test_signup(client):
    """
    sanity check for the signup
    """
    res = client.get('/signup')
    assert res.status_code == 200


def test_forgotpassword(client):
    """
    sanity check for the forgotpassword
    """
    res = client.get('/forgotpassword')
    assert res.status_code == 200


def test_profile(client):
    """
    sanity check for the profile
    """
    res = client.get('/profile')
    assert res.status_code == 200


def test_profile_edit(client):
    """
    sanity check for the profile_edit
    """
    res = client.get('/profile/edit')
    assert res.status_code == 200


def test_checkins(client):
    """
    sanity check for the checkins
    """
    res = client.get('/checkins/')
    assert res.status_code == 200


def test_checkins_add(client):
    """
    sanity check for the checkins_add
    """
    res = client.get('/checkins/add')
    assert res.status_code == 200


def test_checkin(client, checkin):
    """
    sanity check for the individual checkin view
    """
    res = client.get(f'/checkins/{checkin.id}/')
    assert res.status_code == 200


def test_checkin_edit(client, checkin):
    """
    sanity check for the individual checkin edit view
    """
    res = client.get(f'/checkins/{checkin.id}/edit')
    assert res.status_code == 200


def test_teams(client):
    """
    sanity check for the teams view
    """
    res = client.get(f'/teams/')
    assert res.status_code == 200


def test_team(client):
    """
    sanity check for the team view
    """
    # TODO: create team
    team = 1
    res = client.get(f'/teams/{team}/')
    assert res.status_code == 200
