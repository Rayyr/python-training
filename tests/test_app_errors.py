def test_500_error_handler(client):
    app = client.application
    app.config["PROPAGATE_EXCEPTIONS"] = False

    @app.route("/test-trigger-500")
    def trigger_500():
        raise RuntimeError("intentional test error")

    response = client.get("/test-trigger-500")
    assert response.status_code == 500
    assert b"Server Error" in response.data
