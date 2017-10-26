# Girder Job Mocking tool

The following package provides the tool ```girder-jobmock``` which can be used to create Jobs in Girder using a number of different patterns. It does not do any actual processing and is intended to be used to develop novel visualizations of Jobs and their relationships. 

## Install

Close the repository and create a virtual environment.
**NOTE** You must use Python >= 3.5

```
git clone git@kwgitlab.kitware.com:chris.kotfila/girder_jobmock.git jobmock
cd jobmock
mkvirtualenv -a . -ppython3 jobmock 
```

Install the package
```
pip install .
```

## Example Usage

Create a single Job
```
$> girder-jobmock single
```

Create a single Job with a transition delay between running and success of 2 seconds
```
$> girder-jobmock single -d 2
```

Run a basic workflow
```
$> girder-jobmock workflow -d 2
```

Create a group of 10 jobs
```
$> girder-jobmock group -n 10
```

Create a group of 10 jobs with transition delays taken from a normal distribution with mean 10 seconds, variance 5
```
$> girder-jobmock group -n 10 -d 10 -d 5
```


Create a group of 10 jobs with transition delays taken from a skewed normal distribution with mean 10 seconds, variance 3 and skew 50, transition ~30% to error instead of success.
```
$> girder-jobmock group -n 10 -d 10 -d 5 -d 50 -e 0.3
```

Visualize a skewed normal distribution with mean 10 seconds, variance 3 and skew 50

```
$> girder-jobmock dist -d 10 -d 5 -d 50
```

![matplotlib image](misc/dist.png)


Finally remove all jobs created by jobmock:
```
$> girder-jobmock clean
```

## Devops

This package comes with a complete environment for testing against.  Please see the [devops/](devops/) folder for more information.


## Distribution shenanigans

Many commands in girder-jobmock accept a ```-d``` or ```--delay``` flag.  The ```-d``` Flag can be specified up to three times. The first time indicates the delay in seconds before the job will transition to a 'finished' state (either SUCCESS or ERROR). If only on ```-d``` is specified then each task will take exactly this amount of time.  If two ```-d``` are specified,  then the first ```-d``` is the delay,  and the second ```-d``` is the 'jitter.' The amount of time before the task completes will be pulled from a normal distribution with mean of the first ```-d``` and standard deviation of the second ```-d```. In reality,  most task run-times are skewed distributions. If you specify a third ```-d``` This will be the skew of distribution.  It can be difficult to visualize these distributions so we provide the ```dist``` command which will plot 5000 randomly generated numbers from the distribution defined by the sequences of ```-d``` flags you pass to it. This should give you a good sense of the timing ranges your tasks will run in.
