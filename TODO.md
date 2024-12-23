## TODOs

### Preprocessing data
- [x] initial preprocessing of the data
  - [x] mrna
  - [x] mirna
  - [x] circrna
  - [x] te_counts
  - [x] pirna
    - doesnt contain all the samples and from previous results not that strong of a predictor, might be better to omit it
- [x] preprocessor for splitting data into cross validation splits

### Experiments code
- [x] base class for evaluating an experiment
- [ ] implement all the models to use the new interface
  - [x] KNN
  - [x] SVM
  - [x] XGBoost
  - [x] MLP
  - [ ] GNN models
    - [x] sample based gnn
    - [x] bipartite gnn
    - [ ] feature gnn
- [x] differential expression analysis with DeSeq2 (probably could reuse the one that is already finished)
- [ ] thesis mentions DiplomaThesis repo as a reference, should probably delete the original from git and rename the cleaned up DiplomaThesis2 to DiplomaThesis

### Hyperparameter and model selection comparision
- [ ] should improve the hyperparameter search report for the gnn models, this should also probably be done on each dataset separately
  - [ ] e.g. should show the performance of MOGONET, BipartiteGNN and FeatureGNN changes wrt to the hyperparameters on each dataset
- [ ] similarily the comparision of different model architectures and setups could also be improved

### Repeat experiments across datasets
- [ ] BRCA
- [ ] LGG
- do not need to do the complete evaluation with everything if there isn't time, just the comparision of the performance of the models is enough
- should also include the mRNA, circRNA, TE counts combination for MDS dataset

### Feature importance
- [ ] Describe feature importance in more detail (the cross validation part isnt mentioned anywhere yet)

### Finishline
- [ ] Redo feature importances for mogonet with agrregations for disease, risk and mutation
- [ ] Evaluations for additoinal datasets
  - [ ] BRCA
  - [ ] LGG
- [ ] Add feature graph model

### Target validation
- [mirnas](https://www.cuilab.cn/hmdd)
- [ctdbase](https://ctdbase.org/)

### For later
- [ ] increase the number of splits to obtain better estimates, especially useful for tasks such as mutation and risk where there is not very many samples
- [ ] proper validation of the GNN models
- [ ] add learning rate scheduler to the gnn trainer
- [ ] use standard scaler instead of minmax scaler and recompute everything
- [ ] relationship between circrnas and mrnas https://circinteractome.nia.nih.gov/
- [ ] transcription factors should be included in the network creation
- [ ] fix the feature preprocessing, COV selection should be after log transform, since log transform is used to stabilize variance and normalize the data and COV relies on the data following normal distribution, then we do not even need to use COV and can use simple variance filtering
- [ ] high variance in feature importance for mogonet, accumulation of feature importance across multiple training runs could be a solution
- [ ] vytisteni diplomky

### Thesis chapters adjustments
- [ ] 1. Introduction
- [ ] 2. Biological background
- [ ] 3. Graph Neural Networks
- [ ] 4. Classification from omic data
- [ ] 5. State of the art GNN approaches
- [ ] 6. Methods
- [ ] 7. Data
- [ ] 8. Results
- [ ] 9. Conclusions

### Thesis notes
- [ ] cite ALIs table with his thesis
- cite uhkt papers with connections to MDS data
  - https://www.mdpi.com/2073-4409/9/4/794
  - https://febs.onlinelibrary.wiley.com/doi/10.1002/1878-0261.13486
