"""Paired, question-clustered analysis of recorded evaluations and human reviews."""
import math
import numpy as np
from sklearn.metrics import cohen_kappa_score
from services.evaluator import METHODS


def analyze(records, reviews):
    successful = [r for r in records if r.get('status') == 'ok']
    lookup = {(r['sample_id'], r['method']): r for r in successful}
    if len(lookup) != len(successful):
        raise ValueError('Duplicate sample/method records')
    raters = {}
    for r in reviews:
        key = (r['sample_id'], r['reviewer_id'])
        if key in raters:
            raise ValueError('Duplicate reviewer/sample grade')
        score = float(r['overall_score'])
        if not math.isfinite(score) or not 0 <= score <= 10:
            raise ValueError('Review scores must be finite and between 0 and 10')
        if r['reviewer_id'] not in ('reviewer_1', 'reviewer_2'):
            raise ValueError('Use reviewer_1 and reviewer_2')
        raters[key] = score
    ids = sorted({r['sample_id'] for r in successful})
    complete = [sid for sid in ids if all((sid,m) in lookup for m in METHODS) and all((sid,r) in raters for r in ('reviewer_1','reviewer_2'))]
    if not complete:
        return {'status':'insufficient_data', 'paired_sample_count':0, 'methods':{}, 'conclusion':'No samples have all three successful methods and two independent human grades.'}
    engines = {lookup[(sid,m)]['evaluation']['engine'] for sid in complete for m in METHODS}
    if len(engines) != 1:
        raise ValueError('Cannot combine offline and live results')
    contexts = {(r.get('dataset_sha256'),r.get('pack_sha256'),r.get('prompt_version'),r.get('provider'),r.get('model')) for r in records}
    if len(contexts) != 1:
        raise ValueError('Cannot combine different datasets, packs, prompts, or model settings')
    r1 = np.array([raters[(sid,'reviewer_1')] for sid in complete])
    r2 = np.array([raters[(sid,'reviewer_2')] for sid in complete])
    truth = (r1+r2)/2
    groups = [lookup[(sid,METHODS[0])]['question_id'] for sid in complete]
    clusters = sorted(set(groups))
    rng = np.random.default_rng(42)
    # Resample entire questions to respect dependence among answers to one question.
    bootstrap = [np.concatenate([np.flatnonzero(np.array(groups)==g) for g in rng.choice(clusters,len(clusters),replace=True)]) for _ in range(2000)] if len(clusters)>1 else []
    def interval(values):
        if not bootstrap:
            return None
        return [round(float(v),4) for v in np.percentile([np.mean(values[index]) for index in bootstrap],[2.5,97.5])]
    results, errors = {}, {}
    for method in METHODS:
        pred = np.array([lookup[(sid,method)]['evaluation']['overall_score'] for sid in complete],dtype=float)
        err = abs(pred-truth);errors[method]=err
        bins_true,bins_pred=np.rint(truth).astype(int),np.rint(pred).astype(int)
        kappa = float(cohen_kappa_score(bins_true,bins_pred,labels=list(range(11)),weights='quadratic')) if len(set(bins_true)|set(bins_pred))>1 else None
        results[method] = {
            'mae':round(float(err.mean()),4), 'mae_question_bootstrap_ci95':interval(err),
            'rmse':round(float(np.sqrt(np.mean((pred-truth)**2))),4),
            'pearson_r':round(float(np.corrcoef(truth,pred)[0,1]),4) if np.std(truth)>0 and np.std(pred)>0 else None,
            'quadratic_weighted_kappa': kappa if kappa is None or math.isfinite(kappa) else None,
            'within_one_point_percent':round(float(np.mean(err<=1)*100),2),
            'mean_latency_ms':round(float(np.mean([lookup[(sid,method)]['evaluation']['latency_ms'] for sid in complete])),2),
            'cost_usd':None, 'unsupported_feedback_rate':None,
        }
    demo = engines != {'live_llm'}
    return {'status':'demo_only' if demo else 'measured', 'paired_sample_count':len(complete),
        'excluded_or_incomplete_samples':len({r['sample_id'] for r in records})-len(complete), 'question_clusters':len(clusters),
        'human_inter_rater_mae':round(float(np.mean(abs(r1-r2))),4),'methods':results,
        'method3_minus_method1_mae':round(float(np.mean(errors[METHODS[2]]-errors[METHODS[0]])),4),
        'paired_difference_question_bootstrap_ci95':interval(errors[METHODS[2]]-errors[METHODS[0]]),
        'conclusion':('Offline demonstration only; these are not LLM research findings.' if demo else 'Descriptive results on the paired reviewed subset. Negative M3−M1 error favors Method 3. Inspect uncertainty and exclusions; this does not establish learning gains.'),
        'limitations':['Cost and unsupported feedback are not measured.','Scores on different questions are not pre/post learning gains.','Question clustering does not account for repeated participants; use one independent answer per participant or additional participant-aware analysis.']}
