# MHRC-Bench: A Multilingual Hardware Repository-Level Code Completion Benchmark

## 基本信息
- arXiv ID: 2601.03708
- 作者: Qingyun Zou, Jiahao Cui, Nuo Chen, Bingsheng He, Weng-Fai Wong
- 机构: School of Computing, National University of Singapore

## 核心方法

### 问题背景
大型语言模型（LLM）在通用编程语言的代码补全任务上取得了显著进展，但现有代码补全benchmark几乎完全专注于软件代码，而忽视了硬件描述语言。

### MHRC-Bench数据集
提出**MHRC-Bench**，包含：
- **MHRC-Bench-Train**: 训练数据集，用于微调代码LLM
- **MHRC-Bench-Eval**: 评估数据集

覆盖三种主要硬件编程范式：
1. **RTL (Register Transfer Level)**: Verilog/SystemVerilog, VHDL
2. **HLS (High-Level Synthesis)**: Xilinx HLS C/C++
3. **DSL (Domain-Specific Language)**: Chisel

### 数据集规模
- 47,175个源文件
- 来自584个GitHub仓库
- 支持多语言（Chisel, SystemVerilog, Verilog, HLS C/C++, VHDL）

### 标注层次
1. **代码结构层次**: 使用tree-sitter解析为具体语法树（CST），根据CST节点深度分配到不同的桶中
2. **硬件语义层次**: 代码分为9个子类别，包括：
   - Declaration and Definition（声明和定义）
   - Control Flow Block（控制流块）
   - Monitoring and Checking Logic（监控和检查逻辑）

## 实验结果

### 主实验结果
| 模型 | V/SV EM | V/SV ES | VHDL EM | VHDL ES | Chisel EM | Chisel ES | HLS EM | HLS ES |
|------|---------|---------|---------|---------|------------|------------|--------|--------|
| Qwen2.5-Coder-7B (Base) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| + Tuning | **28.5** | **63.7** | **32.1** | **65.1** | **26.4** | **55.7** | **31.5** | **60.2** |
| GPT-5 | 16.5 | 53.9 | 30.0 | 65.6 | 28.6 | 67.0 | 21.5 | 57.6 |

### 关键发现
1. **预训练模型几乎为零**: 所有预训练模型的EM分数接近零，说明仓库级硬件代码补全对预训练模型极具挑战性
2. **微调效果显著**: 微调后Qwen2.5-Coder-7B在EM和ES上大幅超越更大的通用模型
3. **超越GPT-5**: 微调后的Qwen2.5-Coder-14B在所有语言上超越GPT-5、Grok-4和DeepSeek V3.2
4. **编译通过率**: 微调显著提高了代码编译通过率

### CodeBLEU结果
| 模型 | Chisel | V/SV | VHDL | HLS |
|------|--------|------|------|-----|
| Qwen2.5-Coder-7B | 14.8 | 22.9 | 22.2 | 21.0 |
| + Tuning | **49.3** | **54.2** | **56.3** | **52.7** |
| GPT-5 | 42.7 | 45.9 | 41.2 | 51.0 |

## 关键贡献

1. **首个多语言仓库级硬件代码补全benchmark**: 覆盖硬件设计流程中的三种主要硬件编程范式

2. **细粒度标注**: 提供代码结构层次和硬件语义层次的注释

3. **训练数据集**: MHRC-Bench-Train有效提升小规模代码LLM的硬件代码补全能力

4. **全面评估**: 评估了通用LLM、开源代码LLM和基于检索的方法，揭示了LLM在硬件代码补全中的关键性能趋势

5. **新洞察**: 发现硬件代码补全与软件代码补全存在根本性差异：随着代码结构深度增加，性能表现因结构粒度而异
