"""Install the two requested skills without overwriting existing user skills."""
from pathlib import Path
import argparse
import hashlib
import shutil

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('find-skills', 'ui-ux-pro-max')

def files(path):
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dest', type=Path, default=Path.home() / '.agents/skills')
    args = parser.parse_args()
    args.dest.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        source = ROOT / '.agents/skills' / name
        target = args.dest / name
        if target.exists():
            if files(source) != files(target):
                raise SystemExit(f'Existing skill differs; not overwritten: {target}')
            print(f'Already installed: {name}')
            continue
        shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        assert files(source) == files(target)
        print(f'Installed and verified: {name} -> {target}')
    print('skill-creator is bundled with Codex; no duplicate installed.')
