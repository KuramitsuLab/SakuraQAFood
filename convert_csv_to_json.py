#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSVファイルをJSON形式に変換するスクリプト
"""

import csv
import json
import os
import glob

def process_original_csv(file_path, start_id=1):
    """
    オリジナル_食.csvを処理する関数
    形式: 質問, A, B, C, D, 正解
    """
    questions = []

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # ヘッダー行をスキップ

        for idx, row in enumerate(reader, start=start_id):
            if len(row) < 6:
                continue

            question_text = row[0]
            choices = {
                'A': row[1],
                'B': row[2],
                'C': row[3],
                'D': row[4]
            }
            correct_answer_key = row[5].strip().upper()

            # 正解を最初に配置し、残りの選択肢を追加
            if correct_answer_key in choices:
                correct_choice = choices[correct_answer_key]
                other_choices = [choices[key] for key in ['A', 'B', 'C', 'D'] if key != correct_answer_key]
                choice_list = [correct_choice] + other_choices
            else:
                # 正解が不明な場合は順番通り
                choice_list = [choices['A'], choices['B'], choices['C'], choices['D']]

            question_obj = {
                "questionID": f"Q{idx:03d}",
                "keyword": "",
                "category": "食",
                "question": question_text,
                "choice": choice_list,
                "year": "",
                "reference_url": "",
                "authored_by": "claude"
            }

            questions.append(question_obj)

    return questions

def process_culture_csv(file_path, start_id=1):
    """
    日本の食文化(現代).csvを処理する関数
    形式: 年代情報, キーワード, 関連記事, 問題内容, A, B, C, D
    """
    questions = []

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # ヘッダー行をスキップ

        for idx, row in enumerate(reader, start=start_id):
            if len(row) < 8:
                continue

            year = row[0].strip()
            keyword = row[1].strip()
            reference_url = row[2].strip()
            question_text = row[3].strip()

            # 改行を含む質問文を整形
            question_text = question_text.replace('\n', ' ').strip()

            choices = [
                row[4].strip(),  # A (正解と仮定)
                row[5].strip(),  # B
                row[6].strip(),  # C
                row[7].strip()   # D
            ]

            # 空の選択肢をフィルタリング
            choices = [c for c in choices if c]

            # 4つの選択肢がない場合はスキップ
            if len(choices) < 4:
                continue

            question_obj = {
                "questionID": f"Q{idx:03d}",
                "keyword": keyword,
                "category": "日本の食文化(現代)",
                "question": question_text,
                "choice": choices,
                "year": year,
                "reference_url": reference_url,
                "authored_by": "claude"
            }

            questions.append(question_obj)

    return questions

def detect_csv_type(file_path):
    """
    CSVファイルのヘッダーを読み取って形式を判定する
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)

            # ヘッダーの内容で判定
            if len(header) >= 6 and '正解' in header:
                return 'original'
            elif len(header) >= 8 and '年代情報' in header[0]:
                return 'culture'
            else:
                return 'unknown'
    except Exception as e:
        print(f"  エラー: {e}")
        return 'unknown'

def main():
    all_questions = []
    question_id = 1

    # すべてのCSVファイルを取得
    csv_files = glob.glob("*.csv")

    print(f"発見されたCSVファイル: {len(csv_files)}個")

    for csv_file in csv_files:
        print(f"処理中: {csv_file}")

        # CSVの形式を判定
        csv_type = detect_csv_type(csv_file)
        print(f"  形式: {csv_type}")

        if csv_type == 'original':
            questions = process_original_csv(csv_file, start_id=question_id)
            print(f"  {len(questions)}個の質問を抽出")
            all_questions.extend(questions)
            question_id += len(questions)

        elif csv_type == 'culture':
            questions = process_culture_csv(csv_file, start_id=question_id)
            print(f"  {len(questions)}個の質問を抽出")
            all_questions.extend(questions)
            question_id += len(questions)
        else:
            print(f"  未知の形式のためスキップ")

    # JSONファイルに出力
    output_file = "questions.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)

    print(f"\n合計 {len(all_questions)}個の質問を {output_file} に出力しました")

if __name__ == "__main__":
    main()
