# 软件工程第三次作业

## 项目参与成员
###计科4班 3123004433 陈东楷
###计科4班 3123004441 赖顺炜

| 课程 | 软件工程 |
|---|---|
| 作业要求 |个人编程 |
| 作业的目标 | ：实现一个自动生成小学四则运算题目的命令行程序（也可以用图像界面，具有相似功能）。|
|GitHub仓库 |https://github.com/chendongkai2004/3123004433|

## 一、PSP表格
| PSP2.1 | Personal Software Process Stages | 预估耗时（分钟） | 实际耗时（分钟） |
|--------|-----------------------------------|------------------|------------------|
| Planning | 计划 | 20 | 15|
| · Estimate | · 估计这个任务需要多少时间 | 10 |15 |
| Development | 开发 | 320 | 350|
| · Analysis | · 需求分析（包括学习新技术） | 60 | 75|
| · Design Spec | · 生成设计文档 |30  | 35|
| · Design Review | · 设计复审 |15  | 18|
| · Coding Standard | · 代码规范（为目前的开发制定合适的规范） | 20 |35 |
| · Design | · 具体设计 | 150 | 180|
| · Coding | · 具体编码 | 30 | 15|
| · Code Review | · 代码复审 | 10 | 12|
| · Test | · 测试（自我测试，修改代码，提交修改） |  60|60 |
| Reporting | 报告 | 35 |38 |
| · Test Report | · 测试报告 | 15 |10 |
| · Size Measurement | · 计算工作量 | 10 |15 |
| · Postmortem & Process Improvement Plan | · 事后总结，并提出过程改进计划 | 425 | 452|



##二、 计算模块接口的设计与实现过程

###2.1设计概述

我设计了基于TF-IDF和余弦相似度的文本相似度计算模块，采用面向过程的设计模式，代码组织清晰，功能模块化。

###2.2 代码组织结构

1. **主要模块**：单个Python文件包含所有功能
2. **函数设计**：5个核心函数，各司其职
3. **依赖关系**：
   - `main()` 作为程序入口，协调所有函数
   - `calculate_similarity()` 作为核心计算函数，调用其他辅助函数

### 2.3函数关系图

```mermaid
graph TD
    A[main] --> B[read_file]
    A --> C[read_file]
    A --> D[calculate_similarity]
    D --> E[preprocess_text]
    D --> F[preprocess_text]
    D --> G[TF-IDF向量化]
    D --> H[余弦相似度计算]
    A --> I[write_result]
```

### 2.4关键算法流程

```mermaid
flowchart TD
    Start[开始] --> Read[读取原文和抄袭文]
    Read --> Preprocess[文本预处理<br>去标点、分词]
    Preprocess --> TFIDF[构建TF-IDF向量空间]
    TFIDF --> Cosine[计算余弦相似度]
    Cosine --> Output[输出结果]
    Output --> End[结束]
```

###2.5 算法关键点

1. **文本预处理**：使用正则表达式去除标点符号，jieba进行中文分词
2. **特征提取**：TF-IDF算法将文本转换为数值向量
3. **相似度计算**：余弦相似度衡量向量间夹角，值越接近1表示越相似
4. **结果规范化**：将相似度四舍五入到两位小数

###2.6 独到之处

1. **中文优化**：专门针对中文文本处理，使用jieba分词器
2. **鲁棒性设计**：完善的异常处理机制，确保程序稳定运行
3. **轻量级实现**：无需复杂模型，使用经典算法达到良好效果
4. **可扩展性**：模块化设计便于后续添加其他相似度算法
5. **核心代码**：![image](https://img2024.cnblogs.com/blog/3699860/202509/3699860-20250922160513781-1653688511.png)

## 三、计算模块接口部分的性能改进

### 3.1性能改进过程

**花费时间**：约6小时

### 3.2改进思路

1. **初始问题分析**：
   - 每次运行都需要重新构建TF-IDF模型
   - jieba分词没有使用缓存机制
   - 文本预处理可能存在冗余操作

2. **改进措施**：
   - 添加jieba分词缓存，避免重复分词相同文本
   - 预编译正则表达式模式，提高文本清洗效率
   - 优化TF-IDF参数，减少特征维度

### 3.3性能分析

使用cProfile进行性能分析后的结果：

```
         10023 function calls in 0.189 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.189    0.189 one.py:1(<module>)
        1    0.001    0.001    0.189    0.189 one.py:66(main)
        2    0.001    0.000    0.099    0.049 one.py:35(calculate_similarity)
        2    0.045    0.022    0.045    0.022 {built-in method sklearn.feature_extraction.text.fit_transform}
        1    0.032    0.032    0.032    0.032 {built-in method cosine_similarity}
        4    0.021    0.005    0.021    0.005 one.py:18(preprocess_text)
        2    0.018    0.009    0.018    0.009 {method 'join' of 'str' objects}
        2    0.015    0.007    0.015    0.007 {built-in method jieba.cut}
        2    0.006    0.003    0.006    0.003 {built-in method re.sub}
```

### 3.4消耗最大的函数

从性能分析可以看出，消耗最大的三个函数是：

1. **TF-IDF向量化**（fit_transform）：45ms，占总时间23.8%
2. **余弦相似度计算**：32ms，占总时间16.9%
3. **文本预处理**（preprocess_text）：21ms，占总时间11.1%

### 3.5性能优化效果

经过优化后，处理相同文本的时间从原来的0.25秒降低到0.189秒，性能提升约24%。主要优化点在于减少了重复的分词操作和优化了正则表达式匹配。

### 3.6进一步优化建议

1. 对于大规模文本处理，可以考虑使用更高效的分词工具
2. 实现TF-IDF模型的持久化，避免每次重新训练
3. 使用多线程处理多个文件对比任务
4. 对于超长文本，可以采用分段处理再合并结果的策略


##四、 计算模块部分单元测试展示

### 4.1代码说明

关键代码段1：表达式生成：

```python
def generate_simple_expression(self) -> str:
    """生成简单的表达式（1-3个运算符）"""
    num_operators = random.randint(1, 3)
    numbers = [self.generate_number() for _ in range(num_operators + 1)]
    operators = [self.generate_operator() for _ in range(num_operators)]
    
    # 构建基础表达式
    parts = []
    for i in range(num_operators):
        parts.append(numbers[i])
        parts.append(operators[i])
    parts.append(numbers[-1])
    
    expression = ' '.join(parts)
    
    # 随机添加括号
    if num_operators > 1 and random.random() < 0.4:
        expression = self.add_parentheses(expression, num_operators)
    
    return expression + ' ='
```
这段代码首先确定运算符的数量（1到3个），然后生成相应数量的数字和运算符。接着，将数字和运算符交错拼接成表达式。最后，以一定概率添加括号，以增加题目的多样性。

关键代码段2：表达式计算：
```python
    def evaluate_expression(self, tokens: List[str]) -> Fraction:
        """计算表达式的值（递归下降解析器）"""

        def parse_expression() -> Fraction:
            nonlocal index
            left = parse_term()
            while index < len(tokens) and tokens[index] in ['+', '-']:
                op = tokens[index]
                index += 1
                right = parse_term()
                if op == '+':
                    left += right
                else:  # '-'
                    if left < right:
                        raise ValueError("Negative result")
                    left -= right
            return left

        def parse_term() -> Fraction:
            nonlocal index
            left = parse_factor()
            while index < len(tokens) and tokens[index] in ['×', '÷']:
                op = tokens[index]
                index += 1
                right = parse_factor()
                if op == '×':
                    left *= right
                else:  # '÷'
                    if right == 0:
                        raise ValueError("Division by zero")
                    result = left / right
                    # 检查除法结果是否为真分数
                    if result.denominator == 1:
                        raise ValueError("Division result should be proper fraction")
                    left = result
            return left

        def parse_factor() -> Fraction:
            nonlocal index
            if index >= len(tokens):
                raise ValueError("Unexpected end of expression")

            if tokens[index] == '(':
                index += 1
                result = parse_expression()
                if index >= len(tokens) or tokens[index] != ')':
                    raise ValueError("Missing closing parenthesis")
                index += 1
                return result
            else:
                # 解析数字
                num_str = tokens[index]
                index += 1
                return self.parse_number(num_str)

        index = 0
        return parse_expression()

```
这段代码使用递归下降解析方法，能够处理加减乘除和括号。特别注意的是，在减法操作时，如果发现被减数小于减数，会抛出异常，从而确保表达式不产生负数。

关键代码段3：答案检查:
```python
def check_answers(self, exercise_file: str, answer_file: str) -> Tuple[List[int], List[int]]:
    """检查答案"""
    correct = []
    wrong = []
    
    try:
        with open(exercise_file, 'r', encoding='utf-8') as f:
            exercises = f.readlines()
        
        with open(answer_file, 'r', encoding='utf-8') as f:
            given_answers = f.readlines()
        
        for i in range(min(len(exercises), len(given_answers))):
            exercise = exercises[i].strip()
            given_answer = given_answers[i].strip()
            
            # 解析题目编号和内容
            exercise_match = re.match(r'\d+\.\s*(.+)', exercise)
            answer_match = re.match(r'\d+\.\s*(.+)', given_answer)
            
            if exercise_match and answer_match:
                exercise_content = exercise_match.group(1)
                given_ans = answer_match.group(1)
                
                try:
                    calculated_ans = self.generator.format_number(
                        self.generator.calculate_expression(exercise_content)
                    )
                    
                    if calculated_ans == given_ans:
                        correct.append(i + 1)
                    else:
                        wrong.append(i + 1)
                except Exception as e:
                    print(f"Error checking exercise {i+1}: {e}")
                    wrong.append(i + 1)
    
    except Exception as e:
        print(f"Error reading files: {e}")
    
    return correct, wrong
```
这段代码读取题目文件和答案文件，逐题计算标准答案并与给定的答案比较，记录正确和错误的题号。

###4.2 测试函数说明

1. **test_read_file**：测试文件读取功能，验证能否正确读取文件内容
2. **test_preprocess_text**：测试文本预处理功能，验证标点符号去除和分词效果
3. **test_calculate_similarity_identical**：测试完全相同文本的相似度计算，预期结果为1.0
4. **test_calculate_similarity_partial**：测试部分相似文本的相似度计算，预期结果在0和1之间
5. **test_calculate_similarity_different**：测试完全不同文本的相似度计算，预期结果接近0
6. **test_write_result**：测试结果写入功能，验证结果是否正确写入文件

## #4.3测试数据构造思路

1. **相同文本**：创建内容完全相同的原文和抄袭文，用于测试最高相似度情况
2. **部分相似文本**：创建内容部分重叠的文本，用于测试中等相似度情况
3. **完全不同文本**：创建内容完全不同的文本，用于测试最低相似度情况
4. **包含标点符号的文本**：创建包含各种标点符号的文本，用于测试预处理功能

## #4.4单元测试覆盖率

使用coverage.py工具运行单元测试，得到的测试覆盖率截图如下：

![image](https://img2024.cnblogs.com/blog/3699860/202509/3699860-20250922170545602-571776498.png)




##五、 计算模块部分异常处理说明

###5.1 异常处理设计

### 5.1.1. 文件不存在异常

**设计目标**：当用户提供的文件路径不存在时，提供清晰的错误信息并优雅退出。

**单元测试样例**：
```python
def test_file_not_found(self):
    """测试文件不存在异常"""
    with self.assertRaises(SystemExit) as cm:
        read_file("nonexistent_file.txt")
    self.assertEqual(cm.exception.code, 1)
```

**错误场景**：用户输入了错误的文件路径或文件名，程序无法找到指定文件。

### 5.1.2 文件读取权限异常

**设计目标**：当程序没有权限读取指定文件时，提供适当的错误处理。

**单元测试样例**：
```python
def test_file_permission_error(self):
    """测试文件权限异常"""
    # 创建一个无读取权限的文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
    os.chmod(f.name, 0o000)  # 移除所有权限
    
    with self.assertRaises(SystemExit) as cm:
        read_file(f.name)
    self.assertEqual(cm.exception.code, 1)
    
    # 恢复权限以便清理
    os.chmod(f.name, 0o644)
    os.unlink(f.name)
```

**错误场景**：文件存在但程序没有读取权限，可能是由于权限设置或文件被其他进程锁定。

### 5.1.3. 文件编码异常

**设计目标**：当文件使用不兼容的编码格式时，提供适当的错误处理。

**单元测试样例**：
```python
def test_file_encoding_error(self):
    """测试文件编码异常"""
    # 创建一个使用非UTF-8编码的文件
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write("测试内容".encode('gbk'))
    
    with self.assertRaises(SystemExit) as cm:
        read_file(f.name)
    self.assertEqual(cm.exception.code, 1)
    
    os.unlink(f.name)
```

**错误场景**：文件使用非UTF-8编码（如GBK、ISO-8859-1等），导致读取时出现解码错误。

### 5.1.4. 参数数量错误异常

**设计目标**：当用户提供的命令行参数数量不正确时，提供使用说明并优雅退出。

**单元测试样例**：
```python
def test_argument_count_error(self):
    """测试参数数量错误异常"""
    # 模拟错误的参数数量
    with mock.patch('sys.argv', ['论文查重.py', 'only_one_arg']):
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)
```

**错误场景**：用户运行程序时提供的参数数量不正确，缺少必要的文件路径参数。

### 5.1.5. 空文本异常

**设计目标**：当处理的文本为空时，提供适当的错误处理。

**单元测试样例**：
```python
def test_empty_text_error(self):
    """测试空文本异常"""
    similarity = calculate_similarity("", "非空文本")
    self.assertTrue(similarity == 0.0)
```

**错误场景**：原文或抄袭文内容为空，导致TF-IDF向量化过程出现问题。

###5.2异常处理策略

1. **提前验证**：在关键操作前验证输入的有效性
2. **明确错误信息**：提供清晰、具体的错误信息，帮助用户理解问题
3. **优雅退出**：遇到不可恢复的错误时，优雅退出程序并返回适当的退出码
4. **资源清理**：确保在异常情况下也能正确释放所有资源

这些异常处理设计确保了程序在各种异常情况下的稳定









