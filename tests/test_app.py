def test_get_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert expected_activity in data


def test_signup_and_remove(client):
    # Arrange
    email = "test.user@example.com"
    activity = "Chess Club"

    # Act (signup)
    post = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert (signup)
    assert post.status_code == 200
    participants = client.get("/activities").json()[activity]["participants"]
    assert email in participants

    # Act (remove)
    delete = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert (remove)
    assert delete.status_code == 200
    participants = client.get("/activities").json()[activity]["participants"]
    assert email not in participants


def test_signup_duplicate_returns_400(client):
    # Arrange
    email = "michael@mergington.edu"  # already in Chess Club participants
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert resp.status_code == 400


def test_remove_nonexistent_participant_returns_400(client):
    # Arrange
    email = "nobody@example.com"
    activity = "Chess Club"

    # Act
    resp = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert resp.status_code == 400
