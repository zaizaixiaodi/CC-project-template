"""Read-only live MCP checks; no API key is written to the report."""
import argparse
import json
import os
from pathlib import Path
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
ENDPOINTS = {'firecrawl': 'https://mcp.firecrawl.dev/v2/mcp', 'context7': 'https://mcp.context7.com/mcp'}

class Client:
    def __init__(self, name):
        self.url = ENDPOINTS[name]
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
        key = os.environ.get('FIRECRAWL_API_KEY' if name == 'firecrawl' else 'CONTEXT7_API_KEY')
        if key:
            self.headers['Authorization'] = 'Bearer ' + key
        self.seq = 0

    def request(self, method, params=None, notification=False):
        self.seq += 1
        payload = {'jsonrpc': '2.0', 'method': method}
        if not notification:
            payload['id'] = self.seq
        if params is not None:
            payload['params'] = params
        request = urllib.request.Request(self.url, json.dumps(payload).encode(), self.headers)
        with urllib.request.urlopen(request, timeout=55) as response:
            session = response.headers.get('Mcp-Session-Id')
            if session:
                self.headers['Mcp-Session-Id'] = session
            body = response.read().decode()
        if not body.strip():
            return {}
        if body.lstrip().startswith('{'):
            result = json.loads(body)
        else:
            events = [json.loads(line[5:].strip()) for line in body.splitlines() if line.startswith('data:') and line[5:].strip()]
            result = next((x for x in events if x.get('id') == self.seq), events[-1] if events else {})
        if 'error' in result:
            raise RuntimeError('MCP protocol error: ' + str(result['error'].get('code')))
        return result.get('result', {})

    def start(self):
        result = self.request('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'project-template-test', 'version': '1.0'}})
        self.headers['MCP-Protocol-Version'] = result.get('protocolVersion', '2024-11-05')
        self.request('notifications/initialized', notification=True)
        return result

def check(name, live):
    report = {'endpoint': ENDPOINTS[name]}
    try:
        client = Client(name)
        init = client.start()
        tools = client.request('tools/list').get('tools', [])
        report.update(server=init.get('serverInfo'), tools=[t['name'] for t in tools], handshake='PASS')
        if not live:
            return report
        if name == 'firecrawl':
            result = client.request('tools/call', {'name': 'firecrawl_scrape', 'arguments': {'url': 'https://example.com', 'formats': ['markdown']}})
            content = json.dumps(result, ensure_ascii=False)
            report['scrape'] = 'PASS' if not result.get('isError') and 'Example Domain' in content else 'FAIL'
            report['content_chars'] = len(content)
        else:
            result = client.request('tools/call', {'name': 'resolve-library-id', 'arguments': {'libraryName': 'nextjs', 'query': 'Next.js App Router documentation'}})
            content = json.dumps(result, ensure_ascii=False)
            report['resolve_library'] = 'PASS' if not result.get('isError') and 'next' in content.lower() else 'FAIL'
            result = client.request('tools/call', {'name': 'query-docs', 'arguments': {'libraryId': '/vercel/next.js', 'query': 'How do I create a page with the App Router?'}})
            content = json.dumps(result, ensure_ascii=False)
            report['query_docs'] = 'PASS' if not result.get('isError') and ('page' in content.lower()) else 'FAIL'
            report['content_chars'] = len(content)
    except Exception as error:
        report['error'] = str(error)[:300]
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('server', choices=[*ENDPOINTS, 'all'], default='all', nargs='?')
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    names = list(ENDPOINTS) if args.server == 'all' else [args.server]
    report = {name: check(name, args.live) for name in names}
    output = ROOT / 'tests' / ('mcp-' + args.server + '-results.json')
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if all(not x.get('error') and all(v != 'FAIL' for v in x.values()) for x in report.values()) else 1)
