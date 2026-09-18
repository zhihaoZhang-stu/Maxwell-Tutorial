# 一、设计需求案例
设计案例LLC变换器拓扑结构：

[<img src="imgs/img_01.png" width="400">](imgs/img_01.png)

变换器参数：

| Vin | 534V  | Po | 500W   |
|-----|-------|----|--------|
| Nps | 6:1:1 | fs | 500kHz |
| Vo  | 44.5V | Lm  | 40uH   |

# 二、设计变压器
变压器具体设计过程略过，最终的结构如图所示：

[<img src="imgs/img_02.png" width="400">](imgs/img_02.png)

每个磁芯柱上有两匝原边绕组(红色)串联；两个副边绕组(蓝色)S1、S2，分别串联2匝。最终整个变压器的匝数比是12:2:2。

这个步骤已经确定了变压器的完整尺寸及大致的气隙长度。

# 三、在涡流场中调整气隙长度以满足励磁电感要求

## 3.1 三种场中的电感仿真特点
|        | Magnetostatic     | Eddy Current        | Transient            |
|--------|-------------------|---------------------|----------------------|
| 网格划分   | 可自适应              | 可自适应                | 不可自适应<br/>可导入前两个场的网格 |
| 激励方式   | 直流电压、电流           | 正弦电压、电流             | 任意激励波形、外电路           |
| 电感仿真特点 | 直流激励下的电感值，不包含高频效应 | 包含高频效应，可以反映电感随频率的变化 | 不包含高频效应              |

## 3.2 磁芯材料磁导率设置
|               | 固定磁导率      | BH曲线                       |
|---------------|------------|----------------------------|
| 特点            | 磁导率固定      | 磁导率随激励大小变化                 |
| 对电感的影响        | 电感不随激励大小变化 | 电感会受到激励大小的影响               |
| 对开气隙高磁导率电感的影响 |电感不随激励大小变化| 磁芯未饱和时，电感几乎不受到激励大小影响，如下图所示 |

[<img src="imgs/img_03.png" width="400">](imgs/img_03.png)

所以为了保证Maxwell中电感、激励和电路仿真中电感、激励一致，将磁芯材料的磁导率设置为恒定磁导率（初始磁导率）：

[<img src="imgs/img_04.png" width="400">](imgs/img_04.png)

## 3.3 变压器电感计算
经过不断调整气隙长度，使励磁电感接近目标电感值，涡流场中仿真结果：
[<img src="imgs/img_05.png" width="400">](imgs/img_05.png)

**由电感矩阵到变压器T型等效电路的变换：**

[<img src="imgs/img_06.png" width="400">](imgs/img_06.png)

故仿真中变压器的励磁电感：

Lm=(41.421/1.1361)^0.5*6.8041=41.084uH

Lr=L11-Lm=0.337uH

待出一个电感仿真的详细讨论

# 四、将maxwell电感仿真结果反带回电路仿真中求解激励波形
将Lm=41.084uH, Lr=0.337uH带入PSIM仿真中：

[<img src="imgs/img_07.png" width="400">](imgs/img_07.png)

## 4.1 PSIM与maxwell中电流方向统一方法

PSIM中电流表与变压器、电感**同名端方向一致**，例如：在变压器原边电流都同时流入电流表、电感、变压器原边的同名端，在变压器副边电流都同时流出同名端。

Maxwell中施加激励的方向为**正耦合**，即当原副边激励都为正时，磁芯中磁通是叠加的。

[<img src="imgs/img_08.png" width="400">](imgs/img_08.png)

## 4.2 导出PSIM中变压器原副边的电流波形
### 1、保存PSIM的波形为.csv文件
[<img src="imgs/img_09.png" width="400">](imgs/img_09.png)

[<img src="imgs/img_10.png" width="400">](imgs/img_10.png)

### 2、只保留原边电流波形Ipri_tank，删除其他波形，并另存为.txt格式：
[<img src="imgs/img_11.png" width="400">](imgs/img_11.png)

[<img src="imgs/img_12.png" width="400">](imgs/img_12.png)

### 3、将.txt文件后缀名改为.tab

[<img src="imgs/img_13.png" width="400">](imgs/img_13.png)

# 五、在Maxwell瞬态场中仿真变压器损耗

**幅值前面的涡流场仿真，粘贴一个新的design，把求解器改成瞬态场。**

[<img src="imgs/img_14.png" width="400">](imgs/img_14.png)

## 5.1 导入PSIM的激励波形
### 1、Maxwell 3D ——>Design Datasets...
[<img src="imgs/img_15.png" width="400">](imgs/img_15.png)

[<img src="imgs/img_16.png" width="400">](imgs/img_16.png)

[<img src="imgs/img_17.png" width="400">](imgs/img_17.png)

### 2、添加绕组激励
[<img src="imgs/img_18.png" width="400">](imgs/img_18.png)

**Set Eddy Effect:**
[<img src="imgs/img_19.png" width="400">](imgs/img_19.png)

**Set core loss**
[<img src="imgs/img_20.png" width="400">](imgs/img_20.png)

### 3、添加 SETUP

[<img src="imgs/img_21.png" width="400">](imgs/img_21.png)

[<img src="imgs/img_22.png" width="400">](imgs/img_22.png)

**导入涡流场的mesh** 注意这一步千万不能遗漏

[<img src="imgs/img_23.png" width="400">](imgs/img_23.png)

[<img src="imgs/img_24.png" width="400">](imgs/img_24.png)

### 4、启动仿真

### 5、查看损耗

一定要plot稳定后的曲线：
