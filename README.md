# coral
  
まだ、バグまみれ＆機能不十分なのでザクザク改変していきます。  
coralタグの書き方については、機能追加はあれど、必ず後方互換を保ちます。  
  
【そのうちkutinawaに統合予定】アルゴリズム開発時にコードに記述した変遷記録メモを、mermaidを用いた時系列順のフローチャートに変換するためのスクリプト。  
[Will be integrated into kutinawa in due course]Script to describe the transition record memo described in the code during algorithm development in chronological order in flowchart with mermaid notation.  

  
アルゴリズムを作成する際に様々なコードやドキュメントに記述されたメモ(coralタグ、後述)を拾って、開発の変遷をフローチャート化するためのツールです。  

アルゴリズムを作成する際のコードやドキュメントの何処かに下記のcoralタグを記述してください。  
!coral|【親】|【メモ】|【ノードの色】  
  
各内容は以下のようになります。  
!coral　　　　　：この行にタグが書かれていることを示す(必須)  
【親】　　　　　：アルゴリズムの元となった、コード・ドキュメント等のファイル名(省略可)  
【メモ】　　　　：メモ(省略可)  
【ノードの色】　：フローチャートでのこのノードの色(省略可)  
  
例1：  
!coral|昨日考えたアルゴリズム.py|昨日考えた～～～処理部を＠＠＠に変更|red  
例2：  
!coral||ふと思いついた処理をお試し、結果はいまいち|  
  
上記のように省略の際も「|」で示している区切り文字は消さないでください。  


