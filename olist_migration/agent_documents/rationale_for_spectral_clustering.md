------------------------------
## Methodology: Spectral Co-Clustering via Bipartite Graph Relaxation## Data Preprocessing and Matrix Formulation
The raw input matrix tracks interaction frequencies, measuring the total shopping occurrences between individual products across specific weeks of the year. Due to vast discrepancies in overall product velocities and seasonal volume baselines, a direct raw frequency representation introduces severe scaling biases. To resolve this, the raw interaction matrix undergoes Term Frequency-Inverse Document Frequency (TF-IDF) transformation. In this context, weeks function as "documents" and product shopping activities operate as "terms." The normalized affinity element $A_{i,j}$ is defined as:
$$A_{i,j} = \text{TF}(i, j) \times \log\left(\frac{1 + \vert{}V_W\vert{}}{1 + \text{DF}(j)}\right) + 1$$ 
where $\text{TF}(i, j)$ is the frequency of product $j$ during week $i$, $\vert{}V_W\vert{}$ is the total number of evaluated weeks, and $\text{DF}(j)$ represents the number of weeks in which product $j$ exhibits nonzero shopping activity. This normalization scheme scales down globally dominant evergreen items and shifts structural focus onto localized, highly indicative seasonal buying spikes.

## Data Representation and the Temporal-Product Dual-Manifold
Traditional clustering paradigms often isolate temporal trends from product hierarchies, partitioning weeks based on static sales volumes or clustering products by static attributes. This asymmetric approach fails to capture the intrinsic duality of retail dynamics, where seasonal behaviors and product trends exhibit coupled, non-linear dependencies. To capture these interactions without enforcing rigid Euclidean constraints, we adopt a temporal-product dual-manifold assumption. We posit that the temporal entities (weeks of the year) and consumer demand entities (product shopping activities) reside on distinct, low-dimensional continuous manifolds embedded within higher-dimensional ambient spaces. By respecting the joint topology of these co-dependent manifolds, this representation preserves the non-linear, seasonal cross-domain interactions that independent distance metrics inherently distort.

## Discrete Approximation and Bipartite Graph Signals
Because the underlying continuous manifolds are coupled, we discretize the joint space by constructing an undirected bipartite affinity graph $G = (V_W \cup V_P, E)$. The vertex set is partitioned into two disjoint domains: $V_W$, representing the discrete weeks of the year, and $V_P$, representing the distinct product shopping activities. The edges $E$ reflect the localized engagement intensity between a given week and a product, parameterized by the pre-processed week-to-product interaction matrix $A$. Under this framework, structural properties are evaluated using bipartite graph signals, allowing a seamless transition from continuous differential geometry to spectral graph theory.
Unlike standard unipartite clustering, the continuous Laplace-Beltrami operators governing each domain are replaced by a unified bipartite Graph Laplacian system. This system is mathematically initialized using the normalized week-product affinity matrix:
$$B = D_W^{-1/2} A D_P^{-1/2}$$ 
where $D_W$ and $D_P$ are diagonal degree matrices tracking the total scaled shopping activity per week and the total velocity per product, respectively. This formulation provides a rigorous mathematical proxy for measuring joint smoothness, ensuring that temporally aligned weeks and highly correlated product activities are mapped into shared localized neighborhoods.

## Spectral Relaxation and Singular Value Decomposition
With the system modeled as a bipartite topology, the objective of co-clustering translates into a bipartite graph-cut minimization problem. This optimization seeks to partition weeks ($V_W$) and product activities ($V_P$) simultaneously to minimize cross-cluster edge weights, isolating distinct seasonal shopping regimes while maintaining balanced partition scales. While finding the exact optimal discrete co-partition is an NP-hard combinatorial bottleneck, spectral co-clustering resolves this computational constraint via continuous relaxation.
By allowing discrete indicator vectors for both weeks and products to take on continuous real values, the objective function simplifies via the Rayleigh Quotient. Minimizing this quotient subject to proper orthogonality constraints transforms the intractable combinatorial problem into an exact linear algebra problem: the Singular Value Decomposition (SVD) of the normalized interaction matrix $B$.
The fundamental properties of this system guarantee that the left singular vectors represent the smoothest coordinate mappings for the weeks of the year, while the right singular vectors represent the mappings for product activities. By embedding both entity types into a unified, low-dimensional spectral subspace, the non-linearities of the dual manifolds are flattened, rendering the joint clusters linearly separable.

## Subspace Projection and Post-Spectral Partitioning
To transition from the continuous spectral embeddings back to discrete cluster assignments, we project the data into a low-dimensional joint subspace defined by the primary singular vectors. Following the Dhillon formulation, a combined embedding matrix $Z$ is constructed by stacking the scaled left and right singular vectors: [2] 

$$Z = \begin{bmatrix} D_W^{-1/2} U \\ D_P^{-1/2} V \end{bmatrix}$$ 
where $U$ and $V$ contain the optimal singular components corresponding to the target cluster scale $K$. Because the SVD step flattens the dual-manifold non-linearities, the coordinate mappings within $Z$ are structurally optimized for isotropic distance metrics. [1, 2] 
We apply the $K$-means clustering algorithm to the rows of this unified embedding matrix. The algorithm groups elements by iteratively minimizing the sum of squared Euclidean distances to the nearest cluster centroids: [1, 3] 

$$\arg\min_{\mathcal{S}} \sum_{k=1}^{K} \sum_{z \in \mathcal{S}_k} \Vert{}z - \mu_k\Vert{}^2$$ 


where $\mathcal{S}_k$ denotes the $k$-th joint partition and $\mu_k$ is the coordinate centroid of that cluster. This final partitioning step simultaneously generates the row and column cluster labels, mapping specific seasonal calendar windows directly to their corresponding product shopping surges in a clean, block-diagonal format. [3] 

------------------------------


[1] [https://pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/articles/PMC10242062/)
[2] [https://faculty.cc.gatech.edu](https://faculty.cc.gatech.edu/~vempala/papers/dfkvv.pdf)
[3] [https://www.ibm.com](https://www.ibm.com/think/topics/k-means-clustering)
