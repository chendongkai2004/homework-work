import argparse
import random
import fractions
from fractions import Fraction
import os
from typing import List, Tuple, Optional, Set
import re
import sys


class ExpressionGenerator:
    def __init__(self, range_num: int):
        self.range_num = range_num
        self.generated_expressions: Set[str] = set()

    def generate_number(self) -> str:
        """生成自然数或真分数"""
        # 如果范围太小，只生成自然数
        if self.range_num <= 2:
            return str(random.randint(0, self.range_num - 1))

        if random.random() < 0.3:  # 30%概率生成分数
            # 确保分母范围有效
            min_denominator = 2
            max_denominator = max(min_denominator, self.range_num - 1)

            if min_denominator <= max_denominator:
                denominator = random.randint(min_denominator, max_denominator)
                numerator = random.randint(1, denominator - 1)

                if random.random() < 0.2 and numerator < denominator:  # 20%概率生成带分数
                    whole = random.randint(1, min(3, self.range_num // 2))
                    return f"{whole}'{numerator}/{denominator}"
                else:
                    return f"{numerator}/{denominator}"

        # 生成自然数
        return str(random.randint(0, self.range_num - 1))

    def parse_number(self, num_str: str) -> Fraction:
        """将数字字符串转换为Fraction"""
        try:
            if "'" in num_str:
                whole, fraction = num_str.split("'")
                numerator, denominator = fraction.split('/')
                return Fraction(int(whole)) + Fraction(int(numerator), int(denominator))
            elif '/' in num_str:
                numerator, denominator = num_str.split('/')
                return Fraction(int(numerator), int(denominator))
            else:
                return Fraction(int(num_str))
        except:
            return Fraction(0)

    def format_number(self, fraction: Fraction) -> str:
        """将Fraction格式化为要求的数字格式"""
        if fraction == 0:
            return "0"

        # 确保分母为正
        if fraction.denominator < 0:
            fraction = Fraction(-fraction.numerator, -fraction.denominator)

        whole = fraction.numerator // fraction.denominator
        remainder = abs(fraction.numerator) % fraction.denominator

        if whole == 0:
            if remainder == 0:
                return "0"
            else:
                return f"{remainder}/{fraction.denominator}"
        else:
            if remainder == 0:
                return str(whole)
            else:
                return f"{whole}'{remainder}/{fraction.denominator}"

    def generate_operator(self) -> str:
        """生成运算符"""
        weights = [0.25, 0.25, 0.25, 0.25]  # +, -, ×, ÷ 的权重
        return random.choices(['+', '-', '×', '÷'], weights=weights)[0]

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

    def tokenize_expression(self, expression: str) -> List[str]:
        """将表达式分词"""
        # 移除等号
        expression = expression.replace(' =', '').strip()

        tokens = []
        current = ''
        i = 0

        while i < len(expression):
            char = expression[i]

            if char in '()+-×÷':
                if current:
                    tokens.append(current)
                    current = ''
                tokens.append(char)
                i += 1
            elif char.isspace():
                if current:
                    tokens.append(current)
                    current = ''
                i += 1
            else:
                current += char
                i += 1

        if current:
            tokens.append(current)

        return tokens

    def is_valid_expression(self, expression: str) -> bool:
        """检查表达式是否有效"""
        try:
            tokens = self.tokenize_expression(expression)

            # 检查运算符数量
            operators = [token for token in tokens if token in ['+', '-', '×', '÷']]
            if len(operators) > 3:
                return False

            # 计算表达式
            result = self.evaluate_expression(tokens)

            return True
        except Exception as e:
            return False

    def normalize_expression(self, expression: str) -> str:
        """规范化表达式以检测重复（简化版本）"""
        # 移除空格
        expr = expression.replace(' ', '').replace(' =', '')

        # 简单的重复检测：排序数字（对于加法和乘法）
        # 这是一个简化的实现，实际需要更复杂的表达式树比较
        return expr

    def generate_simple_expression(self) -> str:
        """生成简单的表达式（1-3个运算符）"""
        # 当范围很小时，限制运算符数量
        max_operators = min(3, self.range_num - 1)
        if max_operators < 1:
            num_operators = 1
        else:
            num_operators = random.randint(1, max_operators)

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

    def add_parentheses(self, expression: str, num_operators: int) -> str:
        """为表达式添加括号"""
        parts = expression.split()

        if num_operators == 2:
            if random.random() < 0.5:
                return f"({parts[0]} {parts[1]} {parts[2]}) {parts[3]} {parts[4]}"
            else:
                return f"{parts[0]} {parts[1]} ({parts[2]} {parts[3]} {parts[4]})"
        else:  # 3个运算符
            options = [
                f"({parts[0]} {parts[1]} {parts[2]}) {parts[3]} {parts[4]} {parts[5]} {parts[6]}",
                f"{parts[0]} {parts[1]} ({parts[2]} {parts[3]} {parts[4]}) {parts[5]} {parts[6]}",
                f"{parts[0]} {parts[1]} {parts[2]} {parts[3]} ({parts[4]} {parts[5]} {parts[6]})",
                f"({parts[0]} {parts[1]} {parts[2]} {parts[3]} {parts[4]}) {parts[5]} {parts[6]}",
                f"{parts[0]} {parts[1]} ({parts[2]} {parts[3]} {parts[4]} {parts[5]} {parts[6]})"
            ]
            return random.choice(options)

    def generate_expression(self, max_attempts: int = 100) -> Optional[str]:
        """生成一个有效的表达式"""
        for attempt in range(max_attempts):
            expression = self.generate_simple_expression()

            # 检查有效性
            if self.is_valid_expression(expression):
                normalized = self.normalize_expression(expression)
                if normalized not in self.generated_expressions:
                    self.generated_expressions.add(normalized)
                    return expression

        return None

    def calculate_expression(self, expression: str) -> Fraction:
        """计算表达式的值"""
        tokens = self.tokenize_expression(expression)
        return self.evaluate_expression(tokens)


class MathExerciseGenerator:
    def __init__(self):
        self.generator = None

    def generate_exercises(self, count: int, range_num: int) -> Tuple[List[str], List[str]]:
        """生成练习题和答案"""
        self.generator = ExpressionGenerator(range_num)
        exercises = []
        answers = []

        generated_count = 0
        attempts = 0
        max_attempts = count * 10  # 防止无限循环

        while generated_count < count and attempts < max_attempts:
            expression = self.generator.generate_expression()
            if expression:
                try:
                    result = self.generator.calculate_expression(expression)
                    answer = self.generator.format_number(result)

                    exercises.append(expression)
                    answers.append(answer)
                    generated_count += 1
                except Exception as e:
                    print(f"Error calculating expression: {e}")

            attempts += 1

        return exercises, answers

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
                        print(f"Error checking exercise {i + 1}: {e}")
                        wrong.append(i + 1)

        except Exception as e:
            print(f"Error reading files: {e}")

        return correct, wrong


def main():
    parser = argparse.ArgumentParser(description='小学四则运算题目生成器')
    parser.add_argument('-n', type=int, help='生成题目的数量')
    parser.add_argument('-r', type=int, help='数值范围')
    parser.add_argument('-e', type=str, help='题目文件')
    parser.add_argument('-a', type=str, help='答案文件')

    args = parser.parse_args()

    # 验证参数
    if args.e and args.a:
        # 检查答案模式
        if not os.path.exists(args.e):
            print(f"错误：题目文件 {args.e} 不存在")
            return
        if not os.path.exists(args.a):
            print(f"错误：答案文件 {args.a} 不存在")
            return

        math_gen = MathExerciseGenerator()
        math_gen.generator = ExpressionGenerator(10)  # 范围参数不影响检查

        correct, wrong = math_gen.check_answers(args.e, args.a)

        with open('Grade.txt', 'w', encoding='utf-8') as f:
            f.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
            f.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")

        print(f"检查完成！")
        print(f"正确: {len(correct)} 题")
        print(f"错误: {len(wrong)} 题")
        print(f"结果已保存到 Grade.txt")

    elif args.n and args.r:
        # 生成题目模式
        if args.n <= 0:
            print("错误：题目数量必须大于0")
            return
        if args.r <= 1:
            print("错误：数值范围必须大于1")
            return

        if args.n > 10000:
            print("警告：题目数量超过10000，生成可能需要一些时间...")

        math_gen = MathExerciseGenerator()
        exercises, answers = math_gen.generate_exercises(args.n, args.r)

        # 保存题目
        with open('Exercises.txt', 'w', encoding='utf-8') as f:
            for i, exercise in enumerate(exercises, 1):
                f.write(f"{i}. {exercise}\n")

        # 保存答案
        with open('Answers.txt', 'w', encoding='utf-8') as f:
            for i, answer in enumerate(answers, 1):
                f.write(f"{i}. {answer}\n")

        print(f"生成完成！共生成 {len(exercises)} 道题目")
        print(f"题目文件: Exercises.txt")
        print(f"答案文件: Answers.txt")

    else:
        print("错误：参数不完整")
        print("生成题目用法: python math_exercise.py -n <题目数量> -r <数值范围>")
        print("检查答案用法: python math_exercise.py -e <题目文件> -a <答案文件>")
        sys.exit(1)


if __name__ == "__main__":
    main()