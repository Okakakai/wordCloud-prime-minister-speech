import os
import re
import unicodedata
from collections import Counter
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime

# フォルダパスの設定
input_folder = '/content/drive/MyDrive/R5-テキストマイニング/内閣総理大臣所信表明演説s'
font_path = "/content/drive/MyDrive/R5-テキストマイニング/NotoSansJP-SemiBold.ttf"

# 日本語フォントの設定
jp_font = fm.FontProperties(fname=font_path)

# 現在の日付と時刻を取得し、フォルダ名を生成
current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M")
output_folder = f'/content/drive/MyDrive/R5-テキストマイニング/{current_datetime}-result'

# 除外すべきワードを登録する
stopwords = set(['下','方々','具体','皆さん', '我が国','の', 'に', 'は', 'を', 'た', 'が', 'で', 'て', 'と', 'し', 'れ', 'さ', 'ある', 'いる', 'も', 'する', 'から', 'な', 'こと', 'として', 'い', 'や', 'ない', 'など', 'なる', 'へ', 'か', 'だ', 'この', 'によって', 'により', 'おり', 'より', 'による', 'ため', 'その', 'あっ', 'よう', 'また', 'もの', 'という', 'あり', 'まで', 'られ', 'なっ', 'せ', 'させ', 'して'])

# 出力フォルダが存在しない場合は作成
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 形態素解析用の関数
def analyze_text(text):
    tokenizer = Tokenizer()
    tokenized_text = tokenizer.tokenize(text)
    words_list = [token.surface for token in tokenized_text if token.part_of_speech.startswith('名詞,一般') and token.surface not in stopwords]
    return words_list

# ワードクラウド生成と保存の関数
def generate_wordcloud(words, output_image_path, output_text_path, output_bar_graph_path):
    wordcloud = WordCloud(font_path=font_path, font_step=1, max_font_size=100, stopwords=stopwords, width=800, height=400, background_color='white', collocations=False).generate(" ".join(words))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    wordcloud.to_file(output_image_path)

    # 解析後のテキストをテキストファイルとして保存
    with open(output_text_path, 'w', encoding='utf-8') as f:
        f.write(" ".join(words))

    # 単語の出現回数に基づく棒グラフの作成
    word_counts = Counter(words)
    most_common_words = word_counts.most_common(20)  # トップ20の単語を取得
    words, counts = zip(*most_common_words)
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts)
    plt.xticks(rotation=45, fontproperties=jp_font)
    plt.xlabel('Words', fontproperties=jp_font)
    plt.ylabel('Counts', fontproperties=jp_font)
    plt.title('Top 20 Most Common Words', fontproperties=jp_font)
    plt.savefig(output_bar_graph_path, bbox_inches='tight')
    plt.show()

# 指定フォルダ内のファイルを読み込み、ワードクラウドと棒グラフを生成
for file in os.listdir(input_folder):
    if file.endswith('.txt'):
        file_path = os.path.join(input_folder, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().replace('\n', '').replace(' ', '')
        text = re.sub('[\u3000・「」（）]', '', text)
        text = unicodedata.normalize('NFKC', text)
        words = analyze_text(text)
        output_image_path = os.path.join(output_folder, 'Word_Cloud_' + file.split('.')[0] + '.png')
        output_text_path = os.path.join(output_folder, 'Analyzed_Text_' + file.split('.')[0] + '.txt')
        output_bar_graph_path = os.path.join(output_folder, 'Bar_Graph_' + file.split('.')[0] + '.png')
        generate_wordcloud(words, output_image_path, output_text_path, output_bar_graph_path)
