import os

from jina import Client, Document, DocumentArray

from jcloud.flow import CloudFlow

flows_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flows')
flow_file = 'http-flow-new-syntax.yml'
protocol = 'http'


def test_basic_http_flow_with_new_syntax():
    with CloudFlow(path=os.path.join(flows_dir, flow_file)) as flow:
        assert flow.endpoints != {}
        assert 'gateway' in flow.endpoints
        gateway = flow.endpoints['gateway']
        assert gateway.startswith(f'{protocol}s://')

        da = Client(host=gateway).post(
            on='/',
            inputs=DocumentArray(Document(text=f'text-{i}') for i in range(50)),
        )
        assert len(da.texts) == 50
