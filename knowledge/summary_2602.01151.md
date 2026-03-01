# On the Palindromic/Reverse-Complement Duplication Correcting Codes

## 基本信息
- arXiv ID: 2602.01151
- 作者: Yubo Sun, Gennian Ge

## 核心方法

**研究背景**：DNA存储中的体内(in-vivo)存储会面临重复错误——在复制过程中可能发生回文重复(palindromic duplication)和反向互补重复(reverse-complement duplication)错误。

**核心方法**：

1. **m-RCD根方法**：定义m-反向互补重复根(m-RCD root)，即任意两个长度为m的相邻子串，第二个不是第一个的反向互补。证明如果码字不含长度为m的回文重复，则可纠正长度k≥3m-3的不相交重复。

2. **长重复码构造**：使用m-RCD根构造可纠正任意数量长重复的码，只需1个冗余符号。编码/解码复杂度为O(n)。

3. **Gilbert-Varshamov界**：证明存在冗余为$2\log_q n + \log_q\log_q n + O(1)$的码，渐进率达1。

4. **短重复(长度1)码构造**：对于q≥4，提出两种构造：
   - 第一种：冗余$2t\log_q n + O(\log_q\log_q n)$，编码O(n)，解码$O(n(\log_2 n)^4)$
   - 第二种：冗余$(2t-1)\log_q n + O(\log_q\log_q n)$，编码/解码$O(n\cdot \mathrm{poly}(\log_2 n))$

## 实验结果

理论结果（无数值实验）：
- 单符号冗余可纠正长重复：k≥3⌈log_q n⌉
- 冗余界：$2\log_q n + \log_q\log_q n + O(1)$
- 短重复构造1：$2t\log_q n + O(\log_q\log_q n)$
- 短重复构造2：$(2t-1)\log_q n + O(\log_q\log_q n)$

## 关键贡献

1. **单冗余符号纠正任意数量长重复**：首次实现仅需1个冗余符号即可纠正任意数量的不相交回文/反向互补重复

2. **理论下界**：给出Gilbert-Varshamov界，证明最优冗余约为$2\log_q n$

3. **高效实现**：提供O(n)编码和O(n)解码复杂度的实用算法

4. **冗余优化**：两种构造均优于直接使用插入删除纠正码（后者需要$5\log_q n$或$(4t-1)\log_q n$冗余）
