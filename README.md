# Electricity-Trading-HW3-
本專案目的為使用過去發電量以及用電量資料建構一 Gated Recurrent Unit(GRU)模型，用過去七天的資料預測未來一天的用電情形，並將結果用於課 程中電力交易之系統。

# Development Environment
|Package|Version|
|:---:|:---:|
|Tensorflow|2.3
|Keras|2.4.3
|Numpy|1.18.5
|Pandas|1.2.4
|Scikit-learn|0.24.1

# Training Dataset
使用課程提供之訓練數據，先將資料進行前處理後，以便進行後續訓練。

# Electricity use 
➢ 資料來源:由課程助教提供。
➢ 資料內容:資料內含每小時之產電與用電資料，總共 291600 筆，並將資料存放於 training_data 資料夾中，其詳細內容如下表所示。

![GITHUB](https://github.com/Ku-Jo-Chiao/Electricity-Trading-HW3-/blob/main/figure/dataformat.png)

➢ 其整體資料分布如下圖所示。

![GITHUB](https://github.com/Ku-Jo-Chiao/Electricity-Trading-HW3-/blob/main/figure/data_original.png)

# Data preprocessing
➢ 前處理方法:計算淨用電量與 RobustScaler

➢ 概述:將產電資料與用電資料相減取得每日淨用電量，在使用 RobustScaler進行資料處理。RobustScaler 是使用中位數和四分位數，確保每個特徵的統 計屬性都位於同一範圍。它會忽略與其他點有很大不同的數據點，即忽略 異常值 outlier。其公式如下圖所示。其中 X'為新數據、X 為舊數據、 X.median 為數據之中位數、IQR 為數據之四分位距。

➢ 公式:X' = (X - X.median) / IQR

➢ 處理後結果如下圖所示。

![GITHUB](https://github.com/Ku-Jo-Chiao/Electricity-Trading-HW3-/blob/main/figure/data_robust.png)

# Model Training
1. 使用 elect2.py 於本機中訓練模型。其詳細步驟如下列所述。 1. 將上述預處理之成果輸出成 CSV 檔以利後續訓練。
  * 為 csv 檔加入表頭["Number", "RS"]。
  * 刪除"Number"列並選取最後 n 列作為未來預測用途。
  
  ![GITHUB](https://github.com/Ku-Jo-Chiao/Electricity-Trading-HW3-/blob/main/figure/dtp1.png)
  
2. 分割資料集
  * 最後輸出 x_train - 三維數值 (N 比數值,天數,數值) 
  * 最後輸出 y_train - 二維數值 (N 比數值,數值)
  
  ![GITHUB](https://github.com/Ku-Jo-Chiao/Electricity-Trading-HW3-/blob/main/figure/dtp2.png)
  
3. 建構模型
  * 輸入層:(24,32) 
  * 輸出層:(24,1)
   
  ![GITHUB](https://github.com/Ku-Jo-Chiao/Electricity-Trading-HW3-/blob/main/figure/model.png)
  
4. 訓練結果
  * Loss結果如下圖所示。
  
  ![GITHUB](https://github.com/Ku-Jo-Chiao/Electricity-Trading-HW3-/blob/main/figure/loss.png)

# Trade logic
使用上述模型訓練出之模型進行淨用電量預測，當預測出淨用電量為負的，則 需要購買電以補足缺口，而購買價格需比市場電價電價來得低，目前市場電價 1 度約為 2.5 元新台幣。當預測出淨用電量為正，則代表有多餘的電力可以出 售，而出售價格訂定為 1 度 1.5 元新台幣。期望達成淨用電量為 0 的目標。

# Daya Output
最終決定好買賣狀態後進行資料輸出，輸出為 output.csv，一次會輸出未來 24 小時內每小時交易狀態，其格式如下表所示。

![GITHUB](https://github.com/Ku-Jo-Chiao/Electricity-Trading-HW3-/blob/main/figure/output.png)
