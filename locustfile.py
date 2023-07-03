from locust import HttpUser, task


class HelloWordUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/")
