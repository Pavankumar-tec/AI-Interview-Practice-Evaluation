import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import app as server

class LearningTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.db=patch.object(server,'DATABASE_PATH',Path(self.temp.name)/'test.db');self.db.start()
        self.env=patch.dict('os.environ',{'LLM_PROVIDER':'offline_semantic'});self.env.start()
        self.client=server.app.test_client()
    def tearDown(self):
        self.env.stop();self.db.stop();self.temp.cleanup()
    def test_complete_loop_persists_and_exports(self):
        state=self.client.post('/api/learning/start',json={'concept_id':'indexes'}).get_json();sid=state['id']
        self.assertNotIn('lesson',state)
        for stage,next_stage in [('explain','defend'),('defend','learn'),('learn','transfer'),('transfer','complete')]:
            response=self.client.post(f'/api/learning/{sid}/advance',json={'stage':stage,'answer':'An index uses storage and adds work for writes.'})
            self.assertEqual(response.status_code,200)
            state=response.get_json();self.assertEqual(state['stage'],next_stage)
        restored=self.client.get(f'/api/learning/{sid}').get_json();self.assertEqual(len(restored['history']),4)
        self.assertIn('attachment',self.client.get(f'/api/learning/{sid}/export').headers['Content-Disposition'])
    def test_stale_and_empty_requests_do_not_advance(self):
        sid=self.client.post('/api/learning/start',json={'concept_id':'http'}).get_json()['id']
        url=f'/api/learning/{sid}/advance'
        self.assertEqual(self.client.post(url,json={'stage':'transfer','answer':'x'}).status_code,409)
        self.assertEqual(self.client.post(url,json={'stage':'explain','answer':'  '}).status_code,400)
        self.assertEqual(self.client.get(f'/api/learning/{sid}').get_json()['stage'],'explain')
    def test_live_error_keeps_answer_stage(self):
        sid=self.client.post('/api/learning/start',json={'concept_id':'http'}).get_json()['id']
        with patch.object(server,'evaluate_interview_response',side_effect=RuntimeError('Provider failed')):
            self.assertEqual(self.client.post(f'/api/learning/{sid}/advance',json={'stage':'explain','answer':'Valid text'}).status_code,502)
        self.assertEqual(self.client.get(f'/api/learning/{sid}').get_json()['history'],[])
    def test_no_generated_research_results(self):
        self.assertEqual(self.client.get('/api/research/benchmark').get_json()['status'],'not_measured')
