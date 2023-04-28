import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as client:
            response = client.get("/users")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_homepage(self):
        """Test if going to homepage redirects to /users"""

        with self.client as client:
            response = client.get("/", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- Users Pages -->', html)

    def test_create_new_user(self):
        """test if the page creates new user and redirects"""

        with self.client as client:

            response = client.post(
                "/users/new",
                data={
                    "first_name":"test2_first",
                    "last_name":"test2_last",
                    "image_url":""
                },
                follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('test2_first', html)

    def test_user_profile(self):
        """Test to see if user profile loads user"""

        with self.client as client:
            response = client.get(f"/users/{self.user_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- user profile test -->', html)
            self.assertIn('test1_first', html)

    def test_edit_user_profile(self):
        """Test to see if edit user profile page loads"""

        with self.client as client:
            response = client.get(f"/users/{self.user_id}/edit")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- edit user test -->', html)
            self.assertIn('test1_first', html)

    def test_delete_user(self):
        """test if users page properly deletes and loads all users"""

        with self.client as client:

            response = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertNotIn("test1_first", html)
            self.assertEqual(response.status_code, 200)


class PostViewTestCase(TestCase):
    """Test views for posts."""

    def setUp(self):
        """Create test client, add sample data."""

        # Delete all post records
        Post.query.delete()

        # Delete all user records
        User.query.delete()

        self.client = app.test_client()

        post_test_user = User(
            first_name="test3_first",
            last_name="test3_last",
            image_url=None,
        )

        db.session.add(post_test_user)
        db.session.commit()

        test_post = Post(
            title="post1_title",
            content="post1_content",
            user_id=post_test_user.id,
        )

        db.session.add(test_post)
        db.session.commit()

        # Save user_id
        self.user_id = post_test_user.id
        # Save post_id
        self.post_id = test_post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_posts(self):
        """Test that post shows up on user page"""

        with self.client as client:
            response = client.get(f"/users/{self.user_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("post1_title", html)

    def test_new_post(self):
        """Test that new form page displays"""

        with self.client as client:
            response = client.get(f"/users/{self.user_id}/posts/new")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<!-- form test comment -->", html)

    def test_create_new_post(self):
        """Test new post shows up on user page"""

        with self.client as client:

            response = client.post(
                f"/users/{self.user_id}/posts/new",
                data={
                    "title": "post2_title",
                    "content": "post2_content",
                    "user_id": self.user_id
                },
                follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertIn("post2_title", html)
            self.assertEqual(response.status_code, 200)

    def test_view_post(self):
        """Test viewing a specific post in the view post page"""

        with self.client as client:
            response = client.get(f"/posts/{self.post_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<!-- post test comment -->", html)
            self.assertIn("post1_content", html)

    def test_delete_post(self):
        """Test that deleted post doesn't show up on page"""

        with self.client as client:
            response = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertNotIn("post1_title", html)
            self.assertEqual(response.status_code, 200)