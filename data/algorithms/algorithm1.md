$$
\begin{array}{ll}
\textbf{Algorithm 1 } \text{Statics of the continuum legs} \\
\hline
1:\ \text{Initialize } \mathbf{q}^0 \\
2:\ \text{Define a tolerance } \epsilon \\
3:\ i \leftarrow 0 \\
4:\ \textbf{while } \|\mathbf{q}^i - \mathbf{q}^{i-1}\| > \epsilon \textbf{ do} \\
5:\ \quad \text{Find the residual:} \\
    \quad\quad \mathbf{F}(\mathbf{q}^{i-1}) + \mathbf{Mg} + \mathbf{F}_{ext} = \mathbf{b} & (3)\\
6:\  \quad \text{Approximate } \mathbf{F}(\mathbf{q}^i) \text{ by a linearization around } \mathbf{q}^{i-1}\text{:} \\
  \quad\quad \mathbf{F}(\mathbf{q}^i) \approx \mathbf{F}(\mathbf{q}^{i-1}) + \underbrace{\dfrac{\partial \mathbf{F}(\mathbf{q}^{i-1})}{\partial \mathbf{q}}}_{-\mathbf{A}} d\mathbf{q} & (4)\\
7:\ \quad \text{Solve the following system:} \\
    \quad\quad \mathbf{A}\, d\mathbf{q} = \mathbf{b} & (5)\\
8:\ \quad \text{Update } \mathbf{q}^i \text{ (with } 0 < \alpha < 1\text{):} \\
    \quad\quad \mathbf{q}^i = \mathbf{q}^{i-1} + \alpha\, d\mathbf{q} & (6)\\
9:\ \quad i \leftarrow i + 1 \\
10:\ \textbf{end while} \\
11:\ \textbf{Convergence reached: } \mathbf{q}^i \\
\hline
\end{array}
$$
{width=65%, .center}