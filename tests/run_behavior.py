from pathlib import Path
import subprocess, hashlib, json, uuid

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'tests/.tmp/behavior/final-run'
if BASE.exists():
    BASE = BASE.with_name('run-' + uuid.uuid4().hex[:12])
BASE.mkdir(parents=True, exist_ok=True)
sources = list((ROOT / '.agents/skills').rglob('*'))
before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources if p.is_file()}
events=[]
def git(where,*args):
    cmd=['git','-c',f'safe.directory={where.resolve().as_posix()}',*args]
    r=subprocess.run(cmd,cwd=where,text=True,capture_output=True)
    events.append({'command':cmd,'exit_code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip()})
    if r.returncode: raise RuntimeError(r.stderr)
    return r.stdout.strip()
def write(name,content):
    p=BASE/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding='utf-8'); return p

git(BASE,'init','-b','behavior-case')
git(BASE,'config','user.name','Behavior Test')
git(BASE,'config','user.email','behavior@example.invalid')
write('seed.txt','isolated baseline\n')
git(BASE,'add','seed.txt'); git(BASE,'commit','-m','test: isolated baseline')
head=git(BASE,'rev-parse','HEAD')
for n in range(1,4): write(f'materials/meeting-{n}.md',f'# 会议 {n}\n议题：事项 {n}\n决定：完成行动 {n}\n')
plan=write('PLAN.md','''# PLAN: 三份会议材料整理
## 目标
整理三份会议材料，交付 report.md。
## 不做什么
不补充材料之外的事实，不发送报告。
## 背景输入
materials/meeting-1.md、meeting-2.md、meeting-3.md。
## 实施步骤
- [ ] 逐份提取议题和决定。
- [ ] 按来源生成报告并核验。
## 验收标准
- [ ] report.md 包含三个来源小节。
- [ ] 三条决定与原文一致。
## 验证手段
检查报告中三个材料路径，并逐条比对三条决定；验证器检查各来源与决定字符串。
''')
write('snapshots/PLAN-created.md',plan.read_text(encoding='utf-8'))
handoff=write('HANDOFF.md','# HANDOFF\n## 当前 (Now)\n目标：旧目标：汇总全部历史。\n下一步：读取全部历史。\n## 计划 (Plan)\n见 PLAN.md（当前在第 1 步）\n')
write('snapshots/HANDOFF-old.md',handoff.read_text(encoding='utf-8'))
handoff.write_text('# HANDOFF\n## 当前 (Now)\n目标：整理三份会议材料。\n在途：生成报告。\n下一步：逐条核对三个决定。\n## 计划 (Plan)\n见 PLAN.md（当前在第 2 步）\n## 在途决策 (Decisions)\n改为仅整理三份材料，因为委托范围缩小。\n',encoding='utf-8')
assert '旧目标' not in handoff.read_text(encoding='utf-8') and len(handoff.read_text(encoding='utf-8').splitlines()) <= 80
write('snapshots/HANDOFF-updated.md',handoff.read_text(encoding='utf-8'))
log=write('devlog/2026-10-12.md','# 2026-10-12\n\n## 第一轮\n主线：限定三份会议材料。\n决策：仅引用材料中事实，避免扩大范围。\n下一步：核对报告。\n')
with log.open('a',encoding='utf-8') as f: f.write('\n## 第二轮\n主线：完成三份材料报告并核验。\n决策：按来源逐条核验决定。\n下一步：归档计划。\n')
assert all(x in log.read_text(encoding='utf-8') for x in ['第一轮','第二轮'])
report=write('report.md','# 会议材料整理报告\n'+''.join(f'\n## materials/meeting-{n}.md\n议题：事项 {n}\n决定：完成行动 {n}\n' for n in range(1,4)))
assert all(f'决定：完成行动 {n}' in report.read_text(encoding='utf-8') for n in range(1,4))
plan.write_text(plan.read_text(encoding='utf-8').replace('- [ ]','- [x]'),encoding='utf-8')
archive=BASE/'archive/plans/2026-10-12-三份会议材料整理.md'; archive.parent.mkdir(parents=True,exist_ok=True); plan.rename(archive)
handoff.write_text('# HANDOFF\n## 当前 (Now)\n目标：三份会议材料整理已完成。\n在途：无。\n下一步：收到新委托后确定范围。\n## 在途决策 (Decisions)\n已完成计划归档，报告按三个来源核验。\n',encoding='utf-8')
with log.open('a',encoding='utf-8') as f: f.write('\n## 收尾\n验收全部通过，计划已归档。用户要求不提交推送，保留当前 HEAD。\n下一步：等待新委托。\n')
assert not plan.exists() and archive.exists() and '见 PLAN.md' not in handoff.read_text(encoding='utf-8')
assert git(BASE,'rev-parse','HEAD')==head
write('no-commit-evidence.json',json.dumps({'before_HEAD':head,'after_HEAD':git(BASE,'rev-parse','HEAD'),'plan_archived':True},indent=2))

# git-push uses a separate isolated repository and an explicitly selected local bare target.
push=BASE/'push-case'; push.mkdir(exist_ok=True)
bare=BASE/'local-remote.git'; bare.mkdir(exist_ok=True)
git(bare,'init','--bare'); git(push,'init','-b','review-feature')
git(push,'config','user.name','Behavior Test'); git(push,'config','user.email','behavior@example.invalid')
git(push,'remote','add','origin',str(bare.resolve()))
(push/'authorized.txt').write_text('authorized test change\n',encoding='utf-8')
git(push,'status','--short'); branch=git(push,'branch','--show-current'); git(push,'remote','-v'); git(push,'diff'); git(push,'diff','--cached')
git(push,'add','authorized.txt'); git(push,'commit','-m','test: authorized isolated change'); git(push,'push','--set-upstream','origin',branch)
assert git(push,'rev-parse','HEAD')==git(bare,'rev-parse',f'refs/heads/{branch}')
assert git(push,'branch','--show-current')=='review-feature'
assert git(push,'rev-parse','--abbrev-ref','--symbolic-full-name','@{u}')=='origin/review-feature'
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources if p.is_file()}
assert before==after, 'Source skills changed during test'
write('commands.json',json.dumps(events,ensure_ascii=False,indent=2))
print(json.dumps({'artifact_directory':str(BASE),'plan':'PASS','handoff':'PASS','devlog':'PASS','done':'PASS','git-push':'PASS','source_unchanged':True,'baseline_HEAD':head,'push_HEAD':git(push,'rev-parse','HEAD')},indent=2))
