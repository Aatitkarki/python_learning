"""02a–02c: complete manual operations plus plotted optimization/statistics experiments."""
import argparse
import json
import math
import random
from pathlib import Path

def add(a, b):
    if len(a) != len(b): raise ValueError('Shape mismatch')
    return [x+y for x,y in zip(a,b)]
def dot(a, b):
    if len(a) != len(b): raise ValueError('Shape mismatch')
    return sum(x*y for x,y in zip(a,b))
def transpose(matrix):
    if not matrix or not matrix[0] or any(len(r)!=len(matrix[0]) for r in matrix): raise ValueError('Nonempty rectangular matrix required')
    return [list(col) for col in zip(*matrix)]
def matmul(a,b):
    transpose(a); cols=transpose(b)
    return [[dot(row,col) for col in cols] for row in a]
def norm(v): return math.sqrt(dot(v,v))
def distance(a,b): return norm(add(a,[-x for x in b]))
def cosine(a,b):
    denominator=norm(a)*norm(b)
    if denominator==0: raise ValueError('Zero vector')
    return dot(a,b)/denominator
def rotate(v,angle):
    if len(v)!=2: raise ValueError('2D vector required')
    c,s=math.cos(angle),math.sin(angle)
    return [c*v[0]-s*v[1],s*v[0]+c*v[1]]
def mean(xs):
    if not xs: raise ValueError('Empty sample')
    return sum(xs)/len(xs)
def variance(xs, sample=True):
    if len(xs)<=int(sample): raise ValueError('Insufficient sample')
    m=mean(xs); return sum((x-m)**2 for x in xs)/(len(xs)-int(sample))
def standard_deviation(xs,sample=True): return math.sqrt(variance(xs,sample))
def covariance(xs,ys):
    if len(xs)!=len(ys) or len(xs)<2: raise ValueError('Paired sample required')
    mx,my=mean(xs),mean(ys)
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/(len(xs)-1)
def correlation(xs,ys):
    den=standard_deviation(xs)*standard_deviation(ys)
    if den==0: raise ValueError('Constant sample')
    return covariance(xs,ys)/den

def permutation_test(a,b,repeats=2000,seed=42):
    if repeats<1: raise ValueError('Positive repeats required')
    observed=abs(mean(a)-mean(b)); combined=list(a)+list(b); rng=random.Random(seed); extreme=0
    for _ in range(repeats):
        shuffled=rng.sample(combined,len(combined))
        extreme += abs(mean(shuffled[:len(a)])-mean(shuffled[len(a):])) >= observed
    return (extreme+1)/(repeats+1)

def objective(w,b,x,y,penalty=0): return mean([(w*a+b-t)**2 for a,t in zip(x,y)])+penalty*w*w

def gradient_check(x,y,w=.7,b=-.2,penalty=.1):
    residual=[w*a+b-t for a,t in zip(x,y)]
    analytic=[2*mean([a*r for a,r in zip(x,residual)])+2*penalty*w,2*mean(residual)]
    h=1e-5
    numeric=[(objective(w+h,b,x,y,penalty)-objective(w-h,b,x,y,penalty))/(2*h),
             (objective(w,b+h,x,y,penalty)-objective(w,b-h,x,y,penalty))/(2*h)]
    return max(abs(a-b) for a,b in zip(analytic,numeric))

def run(output):
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from projects.stage02.solution import fit
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    fig,axes=plt.subplots(1,2,figsize=(10,4)); x=np.linspace(.1,3,100)
    for name,y in [('linear',2*x+1),('quadratic',x*x),('log',np.log(x))]: axes[0].plot(x,y,label=name)
    axes[0].set(xlabel='x (unitless)',ylabel='f(x)');axes[0].legend()
    v=[2,1];rotated=rotate(v,math.pi/2)
    for vec,label in [(v,'original'),(rotated,'rotated 90 degrees')]: axes[1].quiver(0,0,*vec,angles='xy',scale_units='xy',scale=1,label=label)
    axes[1].set(xlim=(-3,3),ylim=(-3,3),xlabel='x',ylabel='y',aspect='equal');axes[1].legend()
    fig.tight_layout();fig.savefig(out/'algebra.png');plt.close(fig)
    experiments=[];fig,ax=plt.subplots()
    for rate in [.001,.05,1.]:
        w,b,loss=fit([-2,-1,0,1,2],[-3,-1,1,3,5],steps=80,lr=rate,penalty=.1)
        experiments.append(dict(rate=rate,weight=w,bias=b,initial_loss=loss[0],final_loss=loss[-1]))
        ax.semilogy(loss,label=str(rate))
    ax.set(xlabel='Update',ylabel='Regularized MSE');ax.legend(title='Learning rate');fig.savefig(out/'optimization.png');plt.close(fig)
    rng=np.random.default_rng(42)
    bernoulli=rng.binomial(1,.3,10000); binomial=rng.binomial(20,.3,10000); normal=rng.normal(0,1,10000)
    bootstrap=rng.choice(bernoulli,(1000,len(bernoulli)),replace=True).mean(axis=1)
    fig,ax=plt.subplots();ax.hist(binomial,bins=np.arange(-.5,21.5));ax.set(xlabel='Successes in 20 independent trials',ylabel='Count');fig.savefig(out/'binomial.png');plt.close(fig)
    report={'optimization':experiments,'gradient_error':gradient_check([-1,0,1],[-1,1,3]),
            'bernoulli_rate':float(bernoulli.mean()),'bootstrap_mean_interval':np.quantile(bootstrap,[.025,.975]).tolist(),
            'normal_percentiles':np.percentile(normal,[5,50,95]).tolist(),'covariance':covariance([1,2,3],[2,4,6]),
            'correlation':correlation([1,2,3],[2,4,6]),'permutation_p':permutation_test([1,2,3],[7,8,9]),
            'eigenvector_check':matmul([[2,0],[0,3]],[[1],[0]])==[[2],[0]],
            'numpy_agreement':bool(np.allclose(rotate(v,math.pi/2),np.array([[0,-1],[1,0]])@v)),
            'limits':'IID resampling cannot remove sampling bias. Repeated hypothesis selection inflates false positives; predeclare tests or adjust for multiplicity.'}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='work/reference_answers/stage02');a=p.parse_args();print(json.dumps(run(a.output),indent=2))
