# rocket-sim  
**Two-Stage Rocket Trajectory Simulator (Python)**

---

## Overview（概要）
本リポジトリは、**2段式ロケットの打ち上げ軌道を数値シミュレーションする  
Python製の軌道シミュレータ**です。

重力・空気抵抗・推進モデルを考慮し、  
**重力ターンによる打ち上げ → 段間分離 → 上段燃焼**までを  
2次元で再現します。

Streamlit による可視化UIを備えており、  
パラメータ変更による挙動の違いを直感的に確認できます。

---

## Features（できること）
- 2段式ロケットの打上げ軌道シミュレーション（2D）
- 重力・空気抵抗（指数大気モデル）を考慮
- 推力・Isp・燃焼時間による推進モデル
- 重力ターン（ピッチプログラム）
- 段間分離時の質量変化を再現
- 以下の可視化：
  - 軌道（ダウンレンジ vs 高度）
  - 高度 vs 時間
  - 速度 vs 時間
  - 動圧（Max-Q 指標）
- Streamlit によるGUI操作

---

## Motivation（作成背景）
ロケット開発では、以下のような解析業務が重要になります。

- 打上げ軌道最適化  
- 段間分離条件の評価  
- 推力・空力モデルの妥当性検証  

本シミュレータでは、

> **物理モデル → 数値計算 → 可視化 → パラメータスタディ**

という開発フローを一通り自作することで、  
**IST開発部インターン業務例（打上げ軌道最適化・段間分離解析）に直結する  
基礎スキルを身につけること**を目的としています。

---

## Project Structure（構成）
```text
rocket-sim/
├── app/                 # Streamlit UI
│   └── streamlit_app.py
├── src/                 # Core simulation logic
│   ├── atmosphere.py    # Atmospheric model
│   ├── vehicle.py       # Rocket / stage definition
│   ├── guidance.py      # Gravity turn guidance
│   ├── dynamics.py      # Equations of motion
│   └── simulate.py      # Numerical integration (RK4)
├── run_demo.py          # CLI demo script
├── requirements.txt
└── README.md
```

---

## Physics Model（物理モデル概要）

本シミュレータでは、ロケットを**質点**とみなし、  
**2次元平面内の並進運動**としてモデル化しています。

### 運動方程式
- 運動モデル：2次元並進運動
- 重力：一定重力近似

### 空気抵抗
空気抵抗は以下の式でモデル化しています。

$$
D = \frac{1}{2}\rho v^2 C_d A
$$

ここで，
- $\rho$：大気密度  
- $v$：速度  
- $C_d$：抗力係数  
- $A$：代表断面積  

を表します。

### 大気密度（指数モデル）
大気密度は高度に対して指数関数的に減少するモデルを用いています。

$$
\rho(h) = \rho_0 \exp\left(-\frac{h}{H}\right)
$$

ここで，
- $\rho_0$：海面高度での大気密度  
- $h$：高度  
- $H$：スケールハイト  

です。

### 推進による質量流量
推進による質量流量は，推力と比推力から次式で与えられます。

$$
\dot{m} = \frac{T}{I_{sp} g_0}
$$

ここで，
- $T$：推力  
- $I_{sp}$：比推力  
- $g_0$：標準重力加速度  

を表します。

### 数値積分
時間積分には **4次のRunge–Kutta法（RK4）** を使用しています。

---

## Setup（実行方法）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Run

### GUI(Streamlit)

```bash
streamlit run app/streamlit_app.py
```

### CUI(Demo)
```bash
python run_demo.py
```

---

## Example Output(出力例)
- 軌道図（ダウンレンジ vs 高度）
- 高度・速度・動圧の時間履歴

---

## Future Work（今後の拡張）
- 打上げ軌道の自動最適化（SciPy / CMA-ES）
- 段間分離時の相対運動解析
- Max-Q制約付き軌道設計
- 地球中心重力モデルへの拡張
- 3次元軌道対応