$$
\begin{array}{ll}
\textbf{Algorithm 2 } \text{Kinematics of the parallel continuum robot computation } f(\textcolor{red}{\mathbf{u}_a}) = \textcolor{green}{\mathbf{y}_e} \\[0.5em]
\hline \\[-0.5em]
1:\ \text{Initialize } \mathbf{q}^0 = [\mathbf{q}_1^0;\ \mathbf{q}_2^0;\ \mathbf{q}_3^0;\ \mathbf{q}_4^0] \\
2:\ \text{Step 2 and 3 of Algorithm 1} \\
3:\ \textbf{while } \|\mathbf{q}^i - \mathbf{q}^{i-1}\| > \epsilon \textbf{ do} \\
4:\ \quad \text{Find the residual:} \\[0.5em]
\qquad \left\{
\begin{array}{l}
\mathbf{F}_1(\mathbf{q}_1^{i-1}) + \mathbf{M}_1\mathbf{g} + \mathbf{F}_{ext} = \mathbf{b}_1 \\
\vdots \\
\mathbf{F}_4(\mathbf{q}_4^{i-1}) + \mathbf{M}_4\mathbf{g} + \mathbf{F}_{ext} = \mathbf{b}_4
\end{array}
\right. & (14) \\[1em]
5:\ \quad \text{Compute } \mathbf{A}_1(\mathbf{q}_1^{i-1}),\ \ldots,\ \mathbf{A}_4(\mathbf{q}_4^{i-1}) \text{ by linearizing } \mathbf{F}_j\ (j \in [1,4]) \\
\quad\ \quad \text{and use the coupling method to obtain } \mathbf{A} \text{ and } \mathbf{b}. \text{ Then solve:} \\[0.5em]
\qquad \left\{
\begin{array}{l}
\mathbf{A}\, d\mathbf{q} = \mathbf{b} + \mathbf{H}_\mathrm{a}^T \boldsymbol{\lambda}_\mathrm{a} \\
\text{subject to}\\
\boldsymbol{\delta}_\mathrm{a}(\mathbf{q}^{i-1}) + \mathbf{H}_\mathrm{a}\, d\mathbf{q} = \textcolor{red}{\mathbf{u}_a}
\end{array}
\right. & (15) \\[1em]
6:\ \quad \text{Step 8 and 9 of Algorithm 1} \\
7:\ \textbf{end while} \\
8:\ \textbf{return: } \textcolor{green}{\mathbf{y}_e} = \boldsymbol{\delta}_\mathrm{e}(\mathbf{q}^{i-1}) + \mathbf{H}_\mathrm{e}\, d\mathbf{q}\\
\hline 
\end{array}
$$ 
{width=55%, .center}