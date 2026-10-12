"""Validate repository manifests, links and context budgets (Python 3.11+)."""
from pathlib import Path
import json
import re
import tomllib
import yaml

ROOT = Path(__file__).resolve().parents[1]

def validate():
    names = set()
    skills = sorted((ROOT / '.agents/skills').glob('*/SKILL.md'))
    expected = {'plan', 'handoff', 'devlog', 'done', 'git-push', 'structure-guide', 'find-skills', 'ui-ux-pro-max', 'think', 'grill-me', 'grill-with-docs', 'implement', 'ponytail', 'grilling', 'domain-modeling', 'tdd', 'code-review', 'codebase-design'}
    assert {p.parent.name for p in skills} == expected, 'Missing or unexpected project skills'
    for p in skills:
        text = p.read_text(encoding='utf-8')
        meta = yaml.safe_load(text.split('---', 2)[1])
        assert meta['name'] == p.parent.name
        assert meta['name'] not in names
        names.add(meta['name'])
        assert isinstance(meta['description'], str) and meta['description'].strip()
        assert len(text.splitlines()) <= 200
        assert 'disable-model-invocation' not in meta and 'argument-hint' not in meta
        ui = p.parent / 'agents/openai.yaml'
        if ui.exists():
            policy = yaml.safe_load(ui.read_text(encoding='utf-8')).get('policy', {})
            if 'allow_implicit_invocation' in policy:
                assert isinstance(policy['allow_implicit_invocation'], bool)
    for p in (ROOT / '.agents/skills').rglob('*.md'):
        text = p.read_text(encoding='utf-8')
        assert '.claude/' not in text and 'CLAUDE.md' not in text, p
        assert 'archive$plans' not in text and 'templates$' not in text, p
        without_examples = re.sub(r'```[^\n]*\n.*?```', '', text, flags=re.S)
        for link in re.findall(r'\]\(([^)]+)\)', without_examples):
            if '://' not in link and not link.startswith('#'):
                assert (p.parent / link.split('#')[0]).exists(), (p, link)
    dependencies = json.loads((ROOT / 'skills-dependencies.json').read_text(encoding='utf-8'))
    for parent, children in dependencies.items():
        assert parent in names and set(children).issubset(names), (parent, children)
    config = tomllib.loads((ROOT / '.codex/config.toml').read_text(encoding='utf-8'))
    assert config['agents']['enabled'] is True
    assert config['mcp_servers']['firecrawl']['url'] == 'https://mcp.firecrawl.dev/v2/mcp-oauth'
    assert config['mcp_servers']['context7']['url'] == 'https://mcp.context7.com/mcp'
    agents = list((ROOT / '.codex/agents').glob('*.toml'))
    assert len(agents) == 2
    for p in agents:
        data = tomllib.loads(p.read_text(encoding='utf-8'))
        for field in ('name', 'description', 'developer_instructions'):
            assert isinstance(data[field], str) and data[field].strip(), (p, field)
    for file, budget in [('AGENTS.md', 200), ('HANDOFF.md', 80)]:
        assert len((ROOT / file).read_text(encoding='utf-8').splitlines()) <= budget
    print(f'PASS: {len(skills)} skills, {len(agents)} agent manifests, TOML/YAML, links and budgets')

if __name__ == '__main__':
    validate()
