"""Usage: python -m scripts.study --help. Outputs never overwrite existing files."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import random
import subprocess
from datetime import datetime, timezone
from services.evaluator import METHODS, PROMPT_VERSION, build_prompt, evaluate_interview_response
from services.learning import PACK_MAP, question_for
from services.research_service import analyze


def load_dataset(path):
    rows=[json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
    if not rows:
        raise ValueError('Dataset is empty')
    seen=set()
    for row in rows:
        sid=row.get('sample_id')
        if not isinstance(sid,str) or not sid.strip() or sid in seen:
            raise ValueError('Unique nonempty sample_id required')
        seen.add(sid)
        if row.get('concept_id') not in PACK_MAP or row.get('stage') not in ('explain','defend','transfer'):
            raise ValueError('Invalid concept or stage')
        if row.get('source_type') not in ('student','authored','synthetic'):
            raise ValueError('source_type must be student, authored, or synthetic')
        if not isinstance(row.get('answer'),str) or not row['answer'].strip():
            raise ValueError('Nonempty answer required')
        if not row.get('provenance') or row.get('split') not in ('pilot','test'):
            raise ValueError('Record provenance and split (pilot/test)')
        if row['source_type']=='student' and row.get('consent_recorded') is not True:
            raise ValueError('Student answers require documented consent')
    return rows


def create_file(path):
    dest=Path(path);dest.parent.mkdir(parents=True,exist_ok=True)
    return dest.open('x',encoding='utf-8',newline='')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    v=sub.add_parser('validate');v.add_argument('dataset')
    b=sub.add_parser('review-sheet');b.add_argument('dataset');b.add_argument('--out',required=True);b.add_argument('--reviewer',choices=['reviewer_1','reviewer_2'],required=True)
    r=sub.add_parser('run');r.add_argument('dataset');r.add_argument('--out',required=True);r.add_argument('--offline-demo',action='store_true');r.add_argument('--expert-reviewed',action='store_true',help='Attest that frozen pack/rubrics were reviewed; record reviewer sign-off separately');r.add_argument('--split',choices=['pilot','test'],default='pilot')
    a=sub.add_parser('analyze');a.add_argument('run');a.add_argument('reviews',nargs='+');a.add_argument('--out',required=True)
    args=parser.parse_args()
    if args.command=='analyze':
        records=[json.loads(line) for line in Path(args.run).read_text().splitlines() if line.strip()]
        reviews=[]
        for path in args.reviews:
            with open(path,newline='',encoding='utf-8-sig') as file:
                for row in csv.DictReader(file):
                    if row.get('overall_score','').strip():
                        reviews.append(row)
        unknown={r['sample_id'] for r in reviews}-{r['sample_id'] for r in records}
        if unknown:
            raise ValueError('Reviews contain samples outside this run; use matching run and review sheets')
        report=analyze(records,reviews)
        report['run_sha256']=digest(args.run)
        report['review_file_sha256']=[digest(path) for path in args.reviews]
        with create_file(args.out) as file: json.dump(report,file,indent=2,allow_nan=False)
        print(report['conclusion']);return
    rows=load_dataset(args.dataset)
    if args.command=='validate':
        print(f'Validated {len(rows)} answers; provenance labels are declarations, not independently verified.');return
    if args.command=='review-sheet':
        fields=['sample_id','reviewer_id','question','answer','rubric','reference_material','overall_score','notes']
        # Independently shuffled sheets conceal generation labels, AI scores and other reviewers.
        random.Random(41 if args.reviewer=='reviewer_1' else 93).shuffle(rows)
        with create_file(args.out) as file:
            writer=csv.DictWriter(file,fieldnames=fields);writer.writeheader()
            for row in rows:
                q=question_for(PACK_MAP[row['concept_id']],row['stage'])
                item=dict(sample_id=row['sample_id'],reviewer_id=args.reviewer,question=q['question_text'],answer=row['answer'],rubric=json.dumps(q['rubric']),reference_material=q['reference_material'],overall_score='',notes='')
                # Prevent spreadsheet formulas in candidate-controlled text.
                writer.writerow({k:("'"+v if isinstance(v,str) and v.lstrip().startswith(('=','+','-','@')) else v) for k,v in item.items()})
        print('Blind review sheet written. Distribute separately; do not share AI outputs.');return
    selected=[row for row in rows if row['split']==args.split]
    if not selected: raise ValueError('No samples in selected split')
    if not args.offline_demo and not args.expert_reviewed:
        raise ValueError('Expert review sign-off is required before a live study run')
    config={'provider':os.environ.get('LLM_PROVIDER','openai'),'model':os.environ.get('LLM_MODEL'),'api_key':os.environ.get('LLM_API_KEY')}
    if not args.offline_demo and (not config['model'] or not config['api_key'] or config['provider'] not in ('openai','gemini','anthropic')):
        raise ValueError('Set LLM_PROVIDER, LLM_MODEL and LLM_API_KEY for a live run')
    if not args.offline_demo and subprocess.check_output(['git','status','--porcelain'],text=True).strip():
        raise ValueError('Commit the reviewed code and content before a live study run')
    manifest={'dataset_sha256':digest(args.dataset),'pack_sha256':digest(Path(__file__).resolve().parents[1]/'data/concepts.json'),
        'prompt_version':PROMPT_VERSION,'provider':'offline' if args.offline_demo else config['provider'],
        'model':'lexical-demo' if args.offline_demo else config['model'],'split':args.split,'expert_reviewed_attestation':args.expert_reviewed,
        'temperature':0.2,'started_at':datetime.now(timezone.utc).isoformat(),
        'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()}
    jobs=[(row,m) for row in selected for m in METHODS];random.Random(42).shuffle(jobs)
    failures=0
    with create_file(args.out) as file:
        for row,method in jobs:
            q=question_for(PACK_MAP[row['concept_id']],row['stage'])
            record=dict(manifest,sample_id=row['sample_id'],question_id=row['concept_id']+':'+row['stage'],method=method,
                source_type=row['source_type'],prompt=build_prompt(q,row['answer'],method))
            try:
                record['evaluation']=evaluate_interview_response(q,row['answer'],method,provider_config=None if args.offline_demo else config)
                record['status']='ok'
            except (RuntimeError,ValueError) as exc:
                record.update(status='error',error=str(exc));failures+=1
            file.write(json.dumps(record,allow_nan=False)+'\n');file.flush()
    print(f'Recorded {len(jobs)} calls; {failures} failed. No failures were replaced with offline scores.')
    if failures: raise SystemExit(2)


if __name__=='__main__':
    try: main()
    except (ValueError,FileExistsError,KeyError) as exc: raise SystemExit(str(exc))
