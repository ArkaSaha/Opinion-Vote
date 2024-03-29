# Opinion-Vote

This repository contains the code and data used in the experiments of the ICDE 2023 paper titled _"Voting-based Opinion Maximization"_ by Arkaprava Saha, Xiangyu Ke, Arijit Khan and Laks V.S. Lakshmanan.

## Data

<!--The datasets used in the experiments are available [here](https://drive.google.com/drive/folders/1CsTtR7Aq4ZmTtTBwvRtQnuYiZAK50eyh?usp=sharing).-->
Here we describe the format of the datasets to be used in the experiments. For reference, we have provided our DBLP dataset in the file `dblp.zip`. Every folder corresponds to a dataset, and has one sub-folder for each candidate. For our DBLP dataset, the candidates are Yannis E. Ioannidis (0) and Joseph A. Konstan (1).

Each subfolder contains the following files:
1. `attribute.txt`: Consists of 2 lines. One contains `n`, the number of nodes. The other contains `m`, the number of edges with non-zero weights for the corresponding candidate.
2. `opinion.txt`: Consists of `n` lines of the form `v b`, where `b` denotes the initial opinion of user `v` for the corresponding candidate.
3. `stubbornness.txt`: Consists of `n` lines of the form `v d`, where `d` denotes the stubbornness of user `v` for the corresponding candidate.
4. `graph_vote.txt`: Consists of `m` lines of the form `u v w`, where `w` denotes the weight of the edge `(u, v)` for the corresponding candidate.

<!--
The candidates for each dataset are numbered starting from 0 and increasing by 1 in the following order:
1. `mask`: Against, For
2. `distancing`: Against, For
3. `election`: Democratic, Green, Libertarian, Republican
4. `yelp`: American, Canadian, Chinese, French, German, Indian, Italian, Japanese, Korean, Mexican
5. `dblp`: Yannis E. Ioannidis, Joseph A. Konstan
-->

## Code Usage

We show the commands needed to run our various experiments with our provided code.

### Generating the Seed Nodes

We show how to run the various methods for generating the seeds (as explained in Section VIII-A of our paper). Some additional required parameters (`p` for the p-Approval score and, in addition to `p`, position weights `omega[1], ..., omega[p]` for the Positional-p-Approval score) are taken as input from the user at runtime.

#### Direct Matrix Multiplication

The seeds generated by the direct matrix multiplication method can be generated by the following command:
```bash
python DMM.py path-to-dataset number-of-candidates target-candidate time-horizon number-of-seeds score path-to-seeds
```
The parameter `score` can take one of the values `Cumulative`, `Plurality`, `p-Approval`, `Positional-p-Approval` and `Copeland`.

#### Random Walk and Sketch-Based Approximation

The seeds can be generated by our proposed random walk and sketch-based methods using the following command:
```bash
python run.py dataset number-of-seeds time-horizon number-of-candidates target-candidate score mode path-to-seeds
```
The parameter `score` can take one of the values `Cumulative`, `Plurality`, `p-Approval`, `Positional-p-Approval` and `Copeland`. The parameter `mode` can take one of the values `Random-Walk` and `Sketch`. For every combination of values of `score` and `mode`, some additional required parameters are taken as input from the user at runtime. These parameters are listed below.
1. Cumulative score; Random Walk: `delta`, `rho`
2. Cumulative score; Sketch: `epsilon`
3. Plurality (all variants) and Copeland scores; Random Walk: `rho`
4. Plurality (all variants) and Copeland scores; Sketch: `rho`, `theta`
<!--
#### IC and LT Baselines

Their code can be found [here](http://sourceforge.net/projects/im-imm/).

#### Degree Centrality and PageRank Baselines

The seeds according to these methods can be generated by the following command:
```bash
python baselines.py path-to-graph-file method number-of-seeds path-to-seeds
```
The parameter `method` can take one of the values `DC` and `PR`, denoting Degree Centrality and PageRank respectively.

#### Greedy Baseline

The seeds according to this method can be generated by the following command:
```bash
python greedy.py path-to-dataset target-candidate number-of-seeds time-horizon path-to-seeds
```

#### Random Walk with Restart (RWR) Baseline

The seeds according to this method can be generated by the following command:
```bash
python rwr.py path-to-dataset target-candidate number-of-seeds path-to-seeds
```
-->
### Running Time and Memory Usage

These values are displayed on the standard output when the command for generating the seeds is run.

### Computing the Scores of the Returned Seeds

Given a seed set, the score obtained can be computed by the following command:
```bash
python score.py path-to-dataset number-of-candidates target-candidate time-horizon score [path-to-seeds]
```
The parameter `score` can take one of the values `Cumulative`, `Plurality`, `p-Approval`, `Positional-p-Approval` and `Copeland`. The parameter `path-to-seeds` can be omitted to refer to the empty seed set.
<!--
### Minimum Number of Seeds for the Target to Win

The minimum number of seed nodes needed for the target candidate to win can be computed by the following command:
```bash
python winning.py path-to-dataset number-of-candidates target-candidate time-horizon score mode path-to-seeds
```
The parameter `mode` can take one of the values `Matrix`, `Random-Walk` and `Sketch`. The minimum number of seeds is displayed on the standard output.

### Seed Set Characteristics

Here we discuss the code for the experiments related to studying the effects of network properties on the returned seed set (Section VIII-G of our [extended version](./OpinionMax.pdf)).

#### Generation of Ranked Seed Nodes

The generation of the top ranked seed nodes according to our scores, degree centrality and PageRank have been discussed above. The same can be generated according to initial opinions, difference in initial opinions and stubbornness by the following command:
```bash
python find_seed.py path-to-dataset target-candidate number-of-seeds method order path-to-seeds
```
The parameter `method` can take one of the values `opin`, `diff` and `stub`, denoting initial opinions, difference in initial opinions and stubbornness respectively. The parameter `order` can take one of the values `asc` and `desc`, denoting ascending and descending order respectively.

#### Ranking Similarity

The similarity of the node rankings obtained by our scores to those obtained by the other methods can be computed (according to a metric) by the following command:
```bash
python stat.py path-to-our-seeds path-to-other-seeds metric
```
The parameter `metric` can take one of the values `prec`, `ndcg` and `tau`, denoting precision, normalized discounted cumulative gain and Kendall's tau respectively.

### Convergence of Opinions

The variation of the number of nodes changing opinions with respect to time can be computed by the following command:
```bash
python converge.py path-to-dataset target-candidate time-horizon tolerance-percentage path-to-output
```
The tolerance denotes the maximum percentage change in opinion allowed for it to be considered negligible.
 -->