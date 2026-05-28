$$
\begin{array}{ll}
\textbf{Algorithm 3 } \text{Inverse Kinematics obtained by optimization } \textcolor{red}{\mathbf{u}_a} = f^{-1}(\textcolor{green}{\mathbf{y}_e}) \\
\hline
1:\ \text{Initialize } \mathbf{q}^0 = [\mathbf{q}_1^0; \mathbf{q}_2^0] \\
2:\ \text{Step 2 and 3 of Algorithm 1} \\
3:\ \textbf{while } \|\mathbf{q}^i - \mathbf{q}^{i-1}\| > \epsilon \textbf{ do} \\
4:\ \quad \text{Find the residual (like Algorithme 2):} \\
   \qquad\qquad \mathbf{F}(\mathbf{q}^{i-1}) + \mathbf{Mg} + \mathbf{F}_{ext} = \mathbf{b} & (19)\\
5:\ \quad \text{Compute } \mathbf{A} \text{ and } \mathbf{b} \text{ and solve} \\
   \qquad\qquad \left\{ \begin{array}{l} \mathbf{A}\,d\mathbf{q} = \mathbf{b} + \mathbf{H}_a^T \boldsymbol{\lambda}_a \\ \text{subject to} \\ \displaystyle\min_{\boldsymbol{\lambda}_a} \tfrac{1}{2}(\boldsymbol{\delta}_e(\mathbf{q}_{i-1}) + \mathbf{H}_e d\mathbf{q}) - \textcolor{green}{\mathbf{y}_e})^2 \end{array} \right. & (20) \\
6:\ \quad \text{Step 8 and 9 of Algorithm 1} \\
7:\ \textbf{end while} \\
8:\ \textbf{return: } \textcolor{red}{\mathbf{u}_a} = \boldsymbol{\delta}_a(\mathbf{q}^{i-1}) + \mathbf{H}_a\,d\mathbf{q} \\
\hline
\end{array}
$$