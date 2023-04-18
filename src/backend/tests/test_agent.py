import pytest
import logging as lg

from src.backend.config import SUCCESS

# this costs money, so we don't want to run it by default
# TODO: Mocks https://python.langchain.com/en/latest/modules/models/llms/examples/fake_llm.html
test_agents = False
if not test_agents:
    lg.info("Skipping agent tests")
    pytest.skip("Skipping agent tests", allow_module_level=True)


def test_send_message(client):
    # TODO: Understand what is causing resource warning due to unclosed sockets
    response = client.post('/api/send_message', json={"message": "respond with the word: 'here'"})
    assert response.status_code == SUCCESS
    assert "here" in response.get_data(True).lower()

