import pandas as pd
import matplotlib.pyplot as plt

# 1. CSV 파일 불러오기 (현재 경로에 있어야 함)
try:
    df = pd.read_csv('bills.csv', encoding='euc-kr')
except FileNotFoundError:
    print("❌ 'bills.csv' 파일이 현재 디렉터리에 없습니다. 같은 폴더에 넣어주세요.")
    exit()

# 2. 필요한 열 추출 및 전처리
df_cleaned = df[['자치구명', '물건금액(만원)']].dropna()
df_cleaned['물건금액(만원)'] = pd.to_numeric(df_cleaned['물건금액(만원)'], errors='coerce')
df_cleaned = df_cleaned.dropna()

# 3. 자치구별 총 거래 금액 계산 (상위 10개)
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

# 5. 저장 및 출력
plt.savefig('top10_gu_plot.png')
plt.show()
