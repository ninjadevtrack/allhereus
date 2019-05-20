import pytest

pytestmark = pytest.mark.django_db


def test_homepage(client, teacher):
    """
    sanity check for the homepage
    """
    client.force_login(teacher)
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
    res = client.get('/password_reset/')
    assert res.status_code == 200


def test_profile(client, teacher):
    """
    sanity check for the profile
    """
    client.force_login(teacher)
    res = client.get('/profile')
    assert res.status_code == 200


def test_profile_edit(client, teacher):
    """
    sanity check for the profile_edit
    """
    client.force_login(teacher)
    res = client.get('/profile/edit')
    assert res.status_code == 200


def test_checkins(client, teacher):
    """
    sanity check for the checkins
    """
    client.force_login(teacher)
    res = client.get('/checkins/')
    assert res.status_code == 200


def test_checkin(client, teacher, checkin):
    """
    sanity check for the individual checkin view
    """
    client.force_login(teacher)
    res = client.get(f'/checkins/{checkin.id}/')
    assert res.status_code == 200


def test_checkin_edit(client, checkin, teacher):
    """
    sanity check for the individual checkin edit view
    """
    client.force_login(teacher)
    res = client.get(f'/checkins/{checkin.id}/edit')
    assert res.status_code == 200

def test_checkins_add(client, teacher):
    """
    sanity check for the checkins_add
    """
    client.force_login(teacher)
    res = client.get('/checkins/add')
    assert res.status_code == 200



#def test_teams(client):
#    """
#    sanity check for the teams view
#    """
#    res = client.get(f'/teams/')
#    assert res.status_code == 200


#def test_team(client):
#    """
#    sanity check for the team view
#    """
#    # TODO: create team
#    team = 1
#    res = client.get(f'/teams/{team}/')
#    assert res.status_code == 200
