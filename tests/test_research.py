import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from services.evaluator import METHODS, build_prompt, evaluate_interview_response, validate_result
from services.learning import PACKS, question_for
from services.research_service import analyze
from scripts.study import load_dataset

class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.q={'question_text':'QUESTION_SENTINEL','rubric_json':json.dumps([{'name':'RUBRIC_SENTINEL'}]),'reference_material':'REFERENCE_SENTINEL'}
    def test_prompt_conditions_do_not_leak(self):
        prompts=[build_prompt(self.q,'ANSWER_SENTINEL',m) for m in METHODS]
        self.assertNotIn('RUBRIC_SENTINEL',prompts[0]);self.assertNotIn('REFERENCE_SENTINEL',prompts[0])
        self.assertIn('RUBRIC_SENTINEL',prompts[1]);self.assertNotIn('REFERENCE_SENTINEL',prompts[1])
        self.assertIn('REFERENCE_SENTINEL',prompts[2])
    def test_live_failure_never_becomes_demo(self):
        with patch('services.evaluator.call_live_llm',return_value=None):
            with self.assertRaises(RuntimeError):
                evaluate_interview_response(self.q,'answer',provider_config={'api_key':'test','model':'test','provider':'openai'})
    def test_quote_check_and_invalid_score(self):
        response={'overall_score':6,'criterion_scores':{},'evidence_quotes':['actual','fabricated'],'suggestions':[],'followup_question':'Why?'}
        checked=validate_result(response,'actual answer')
        self.assertEqual(checked['evidence_quotes'],['actual']);self.assertTrue(checked['review_flag'])
        self.assertIsNone(checked['unsupported_feedback_count'])
        for bad in (float('nan'),True,11,-1):
            with self.assertRaises(ValueError):validate_result(dict(response,overall_score=bad),'actual')
    def test_packs_have_distinct_transfer(self):
        self.assertEqual(len(PACKS),12)
        for pack in PACKS:
            self.assertNotEqual(pack['explain'],pack['transfer'])
            self.assertEqual(sum(c['max_score'] for c in question_for(pack,'transfer')['rubric']),10)
    def test_demo_is_not_research(self):
        result=evaluate_interview_response(question_for(PACKS[0],'explain'),'lookup storage writes query')
        self.assertFalse(result['research_eligible']);self.assertEqual(result['token_cost'],0)
    def test_dataset_requires_consent(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'input.jsonl';row=json.loads(Path('data/pilot.example.jsonl').read_text().splitlines()[0]);row['source_type']='student'
            path.write_text(json.dumps(row))
            with self.assertRaises(ValueError):load_dataset(path)

class AnalysisTests(unittest.TestCase):
    def records(self):
        records=[];reviews=[]
        for i in range(3):
            for method in METHODS:
                records.append({'sample_id':str(i),'question_id':str(i),'method':method,'status':'ok',
                    'evaluation':{'engine':'offline_lexical_demo','overall_score':i+3,'latency_ms':1}})
            for reviewer in ('reviewer_1','reviewer_2'):
                reviews.append({'sample_id':str(i),'reviewer_id':reviewer,'overall_score':i+3})
        return records,reviews
    def test_missing_reviews_do_not_create_results(self):
        records,_=self.records();self.assertEqual(analyze(records,[])['status'],'insufficient_data')
    def test_complete_subset_and_demo_label(self):
        records,reviews=self.records();records[0]['status']='error'
        result=analyze(records,reviews)
        self.assertEqual(result['paired_sample_count'],2);self.assertEqual(result['excluded_or_incomplete_samples'],1)
        self.assertEqual(result['status'],'demo_only');self.assertEqual(result['method3_minus_method1_mae'],0)
    def test_duplicates_and_mixed_engines_rejected(self):
        records,reviews=self.records()
        with self.assertRaises(ValueError):analyze(records+[records[0]],reviews)
        records[0]['evaluation']['engine']='live_llm'
        with self.assertRaises(ValueError):analyze(records,reviews)
    def test_constant_scores_have_no_fake_correlation(self):
        records,reviews=self.records()
        for r in records:r['evaluation']['overall_score']=5
        for r in reviews:r['overall_score']=5
        result=analyze(records,reviews)
        self.assertIsNone(result['methods'][METHODS[0]]['pearson_r'])
        self.assertIsNone(result['methods'][METHODS[0]]['quadratic_weighted_kappa'])

class LiveSchemaTests(unittest.TestCase):
    def test_weighted_total_must_match(self):
        q=question_for(PACKS[0],'explain')
        result={'overall_score':9,'criterion_scores':{c['id']:{'name':c['name'],'score':0,'max_score':c['max_score'],'feedback':'Missing'} for c in q['rubric']},'evidence_quotes':[],'suggestions':[],'followup_question':'Why?'}
        with patch('services.evaluator.call_live_llm',return_value={'text':json.dumps(result),'model':'test','usage':{}}):
            with self.assertRaises(RuntimeError):evaluate_interview_response(q,'Some answer',provider_config={'api_key':'test','model':'test'})
    def test_valid_live_record_preserves_usage(self):
        q=question_for(PACKS[0],'explain')
        result={'overall_score':10,'criterion_scores':{c['id']:{'name':c['name'],'score':c['max_score'],'max_score':c['max_score'],'feedback':'Covered'} for c in q['rubric']},'evidence_quotes':['Some answer'],'suggestions':[],'followup_question':'Why?'}
        with patch('services.evaluator.call_live_llm',return_value={'text':json.dumps(result),'model':'test-resolved','usage':{'total_tokens':123}}):
            actual=evaluate_interview_response(q,'Some answer',provider_config={'api_key':'test','model':'test'})
        self.assertEqual(actual['usage']['total_tokens'],123);self.assertIsNone(actual['token_cost'])
        self.assertEqual(actual['model'],'test-resolved');self.assertTrue(actual['research_eligible'])
