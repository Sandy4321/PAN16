# PAN16
Software submitted for PAN16 Author Clustering (http://pan.webis.de/clef16/pan16-web/author-identification.html)<br />
The submission got 3rd and 4th best for Mean F-Score and MAP (submission team: sari16). The complete results can be seen here (http://www.tira.io/task/author-clustering/dataset/pan16-author-clustering-test-dataset2-2016-04-12/) <br />
The notebook paper will be published soon at http://pan.webis.de/publications.html

Before running the code, please make sure to install all dependencies software (sklearn, gensim).<br />
To run the software, type this following command in terminal:
```python
  python main.py -c $inputDataset -o $outputDir
```
The system used the character n-gram features together with K-means clustering. The number of clusters were optimized using Silhoutte Coefficient. <br \>
Initially, we also tried to use word embeddings as the features. However, since the results didn't show any significant improvement, we decided to use character n-grams in our final software.<br \>

We have created word2vec model for Dutch (see under "model" directory) and used Google word2vec binary model (you have to download it by your own and put it under "model" directory)
