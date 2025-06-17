import pandas as pd
import matplotlib.pyplot as plt

# 1. 데이터 로드
df = pd.read_csv('data/bills.csv', encoding='euc-kr')

# 2. 필요한 열 추출 및 전처리
df_cleaned = df[['자치구명', '물건금액(만원)']].dropna()
df_cleaned['물건금액(만원)'] = pd.to_numeric(df_cleaned['물건금액(만원)'], errors='coerce')
df_cleaned = df_cleaned.dropna()

# 3. 자치구별 총 거래 금액 계산
top10 = df_cleaned.groupby('자치구명')['물건금액(만원)'] \
                  .sum() \
                  .sort_values(ascending=False) \
                  .head(10)

# 4. 시각화
plt.figure(figsize=(12, 6))
top10.plot(kind='bar', color='skyblue')
plt.title('거래 금액 상위 10개 자치구')
plt.xlabel('자치구')
plt.ylabel('총 거래 금액 (만원)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('top10_gu_plot.png')  # 그래프 저장
plt.show()
