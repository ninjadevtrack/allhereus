import pytest
from freezegun import freeze_time

pytestmark = pytest.mark.django_db


@freeze_time("2012-01-14")
def test_creating_csvs(client, teacher):
    """
    ensure that we can create csv files correctly
    """

    client.force_login(teacher)

    res = client.get('/checkins.csv')
    assert res.status_code == 200
    assert res.get('Content-Type') == 'text/csv'
    assert res.get('Content-Disposition') == 'attachment; filename="AllHere Checkins Archive 2012-01-14 00:00:00.csv"'
    header_rows = b'date,teacher,student,status,visit type,info learned,info better,success score\r\n'
    assert res.content == header_rows
