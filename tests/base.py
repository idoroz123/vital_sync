import unittest


class ServerTestBase(unittest.TestCase):
    session = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from app import app, db

        assert app.config["USING_TEST_CONFIG"]

        app.testing = True
        cls.flask_test_client = app.test_client()

        with app.app_context():
            db.create_all()
            cls.session = db.session

    @classmethod
    def tearDownClass(cls):
        from app import app, db

        with app.app_context():
            db.drop_all()
