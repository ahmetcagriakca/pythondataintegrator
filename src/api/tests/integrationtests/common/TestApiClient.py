import json


class TestApiClient:
    def __init__(self, client):
        self.client = client

    def print_error_detail(self, data):
        print(data['message'] if 'message' in data else '')
        print(data['traceback'] if 'traceback' in data else '')
        print(data['message'] if 'message' in data else '')

    def get(self, url):
        response = self.client.get(
            url,
            content_type='application/json',
        )

        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        return response_data

    def post(self, url, request_data):
        # insert connection
        data = json.dumps(request_data)
        response = self.client.post(
            url,
            data=data,
            content_type='application/json',
        )
        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        return response_data

    def put(self, url, request_data):
        data = json.dumps(request_data)
        response = self.client.put(
            url,
            data=data,
            content_type='application/json',
        )
        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        return response_data

    def delete(self, url, request_data):
        data = json.dumps(request_data)
        response = self.client.delete(
            url,
            data=data,
            content_type='application/json',
        )
        response_data = json.loads(response.get_data(as_text=True))
        print(response_data)
        assert response.status_code == 200
        self.print_error_detail(response_data)
        return response_data
