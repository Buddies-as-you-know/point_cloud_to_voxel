[1] H. Yuan and R. C. Veltkamp, "PreSim: A 3D Photo-Realistic Environment Simulator for Visual AI," in IEEE Robotics and Automation Letters, vol. 6, no. 2, pp. 2501-2508, April 2021, doi: 10.1109/LRA.2021.3061994.


### 論文リンク
https://ieeexplore.ieee.org/abstract/document/9362238
### 著者/所属機関
H. Yuan and R. C. Veltkamp
### 投稿年
April 2021
## 概要：

この研究では、拡張現実（AR）を使用してロボットのプログラミングを助けるための堅牢な把持手法について提案されています。著者たちは、人間のデモンストレーションを通じてロボットに把持を学習させるための新しいアプローチを開発しました。

## 研究背景

ロボットの把持技術は、製造業から医療まで多くの分野での応用が期待されています。しかし、従来の手法では、環境の変化に対応するための柔軟性や適応性が不足していました。この問題を解決するため、拡張現実を利用した新しい学習手法が必要とされていました。

## 提案手法
(i) 仮想世界で多感覚モデルをシームレスに統合し、シーンを認識してナビゲートできるようにするフォトリアリスティックな 3D 環境を提供します。

(ii) 内部ビュー合成モジュールを備えており、シミュレーションで開発およびテストされたアルゴリズムを、ドメイン適応を行わずに物理プラットフォームに変換します。

(iii) 深度推定やオブジェクト姿勢推定などのビジョンベースのアプリケーション用に大量のデータを生成できます。

## 実験

実験では、提案手法の有効性を検証するため、ロボットが様々な物体を把持するタスクが行われました。結果として、ARを使用した手法は、従来の手法に比べて高い精度と効率性を示しました。

## 感想

この研究は、ロボットの把持技術の進展に対する重要な一歩と言えます。拡張現実を利用することで、ロボットはより複雑なタスクに適応できるようになり、多くの産業分野での応用が期待されます。

## 参考

## どんなもの？

ビュー合成のモジュールを使用して任意の位置からの膨大な量のフォトリアリスティックな仮想RGB-Dビューを提供することでシミュレーションと現実の間の現実ギャップを縮めることを目的としている。


![image](https://github.com/Buddies-as-you-know/research_docs/assets/69001166/4e1563f7-98dc-434c-8e14-30fcd3f8b7f5)

AI 研究用のビジョンベースのアルゴリズムを開発するための 3D フォトリアリスティックな環境シミュレーターである PreSimを提案、開発をしている。

## 先行研究と比べてどこがすごい?
- gazebo
- unreal engine 4
- VRKitchen
- Habitat
エンジンへの依存度が高いため、豊富なシミュレート環境によって制限されます。対照的に、当社の環境シミュレーターを使用すると、ユーザーはデータセットを使用して独自の環境を構築できます。

![image](https://github.com/Buddies-as-you-know/research_docs/assets/69001166/3ee06526-438f-4f17-9207-561edf19cb07)

従来の手法に比べて、拡張現実を利用することで、ロボットは環境の変化に柔軟に適応し、より正確な把持が可能になります。

Gibson Envはこの論文と近いことをしている。

### Image based rendering


## 技術や手法のキモはどこ?

![image](https://github.com/Buddies-as-you-know/research_docs/assets/69001166/0a11dddb-15be-4ea8-983e-d980c2f5694c)

1. 3D 再構成から生成された実際のシーンの点群を ROS にインポートし、
2. ROS フレームワークの 3D ビジュアライザーである Rviz で入力画像のカメラポーズとともに表示します。
3. 仮想世界全体で仮想カメラの動きを制御し、ROS によってその 6D 姿勢をリアルタイムで推定します。
4. 推定された姿勢は、クエリ入力データセット内で最も類似した色と深度の画像ペアを選択するための基準として使用されます。次に、選択した色と深度の画像ペアを使用して、ビュー合成モジュールに基づいて仮想ビューを合成します。
5. 同時に、移動するカメラの軌跡全体と合成された色と深度の画像のペアが記録されます。

### ビュー合成

ビュー合成モジュールは RGB-D 画像のまばらなセットを入力として受け取り、任意の視点から新しい色と深度の画像ペアを生成します。
#### オブジェクトの境界のピクセル精度の整列と深度の精緻化
色画像と深度画像のペア間でのオブジェクトの境界のピクセル精度の整列と正確な深度値は、高品質なレンダリングのために必要です。不正確な深度値や整列のズレは、ゴーストの輪郭などの視覚的なアーチファクトを引き起こすことがよくあります。オフラインの前処理中に、この目的を達成するためのピクセル対ピクセルの多視点深度精緻化アルゴリズムを導入します。

マッチングコスト関数 C(d i) は次のように定義されます。

```math
C(d_i) = C_{pixel}(d_i) + C_{patch}(d_i)
```

ここで、\( C_{\text{pixel}}(d_i) \) と \( C_{\text{patch}}(d_i) \) は、それぞれピクセル \( i \) の深度 \( d_i \) に対する写真の一貫性とエッジの保存を強調します。

写真の一貫性 \( C_{\text{pixel}}(d_i) \) は、それを他の画像に投影することで計測されます。以下の式で示されます。
```math
C_{\text{pixel}}(d_i) = \sum _{r\in R}\lambda ||x_{i} - x_{r} ||_1 + (1-\lambda) ||\bigtriangledown x_{i} - \bigtriangledown x_{r}||_1
C_{patch}(d_i) =\textstyle \frac{1}{N} \sum _{q\in W_i } e^{ -||x_{i} -x_{q}||_1}

```
深度の精緻化過程では、一致コストが最も低い近くのものとピクセルの深度値を繰り返し置き換えます。イテレーションは左上のピクセルから始まり、行の主要な順序でピクセルを横断します。伝播は深度のフィルタリングと交互に行われます。

![image](https://github.com/Buddies-as-you-know/research_docs/assets/69001166/6c61a2f9-1853-4d2d-bf67-a5e13624ee99)


## どうやって有効だと検証した?
![image](https://github.com/Buddies-as-you-know/research_docs/assets/69001166/01753ec8-0c29-4e55-aaab-1491da9a0095)


- 3 つの独自のデータセット
- [datasets (Attic, Dorm, Playroom, Reading corner)](https://dl.acm.org/doi/pdf/10.1145/2980179.2982420)

さまざまなデータセットでレンダリングされた深度マップの定量的評価
![image](https://github.com/Buddies-as-you-know/research_docs/assets/69001166/8bbb2560-2af4-45f7-9c45-dd00ddc73c7d)
![image](https://github.com/Buddies-as-you-know/research_docs/assets/69001166/91217a1f-752f-4fbe-93c5-e01e7275f3e7)
![image](https://github.com/Buddies-as-you-know/research_docs/assets/69001166/b45bd553-e3d9-41b9-b6e0-d4036ab8e92c)



部屋全体をカバーすることを目的として、まばらにキャプチャされた画像が収集されます。ピーク信号対雑音比 (PSNR) (高いほど優れています) は、画質を評価するために使用されます。定量的評価結果を表 3にまとめます。
## 次に読むべき論文はあるか？
- [Scalable Inside-Out Image-Based Rendering](https://dl.acm.org/doi/pdf/10.1145/2980179.2982420)
- [F. Xia, A. R. Zamir, Z. He, A. Sax, J. Malik and S. Savarese, "Gibson env: Real-world perception for embodied agents", Proc. IEEE Conf. Comput. Vis. Pattern Recognit., pp. 9068-9079, 2018.](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8579043)
## 論文の主張やビジョンそのものに問題はないか？
- 自分の論文にも近い論文

制限と今後の取り組み:私たちの深度調整とビュー合成のアプローチは、最初のキャプチャの品質によって制限されます。キャプチャされた深度マップに欠落した情報が多すぎる場合、この方法では視覚的なアーティファクトが発生する可能性があります。たとえば、透明なオブジェクトの深度情報が 50% 未満しかキャプチャされていない場合、PreSim はそのオブジェクトに対して正確な合成画像を生成できません。さらに、データの合成に使用される軌道には、データを収集する人のようなさまざまな動きが含まれていますが、深度/姿勢予測ネットワークのトレーニングに使用されるデータの合成に対するさまざまな軌道生成戦略の影響を分析するには、新しいアプローチが必要です。

## 使える文章

collecting such data is time-consuming and labor-intensive. Apart from that, developing and testing visual AI algorithms for multisensory models is expensive and in some cases dangerous processes in the real world.

- ディープラーニングを使用するには大量のデータが必要になる(画像)
- しかし、現実世界でロボットを動かすのはコストも費用もかかる
- 
