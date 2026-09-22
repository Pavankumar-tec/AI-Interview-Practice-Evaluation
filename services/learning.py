"""Draft concept packs; faculty review is required before a formal study."""
import json
from pathlib import Path

PACKS = json.loads((Path(__file__).resolve().parents[1] / 'data/concepts.json').read_text())
PACK_MAP = {p['id']: p for p in PACKS}
STAGES = ('explain', 'defend', 'learn', 'transfer', 'complete')


def question_for(pack, stage):
    return {'question_text': pack[stage], 'category': 'Technical Knowledge',
            'rubric': pack['rubrics'][stage], 'reference_material': pack['lesson'], 'keywords': pack['keywords']}


def public_state(record):
    pack = PACK_MAP[record['concept_id']]
    stage = record['stage']
    state = {'id': record['id'], 'concept_id': pack['id'], 'title': pack['title'],
             'stage': stage, 'history': json.loads(record['history']), 'content_status': pack['status']}
    if stage in ('explain', 'defend', 'transfer'):
        state['question'] = pack[stage]
    if stage in ('learn', 'transfer', 'complete'):
        state.update(lesson=pack['lesson'], activity=pack['activity'], sources=pack['sources'])
    return state
