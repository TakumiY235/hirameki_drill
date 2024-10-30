# story_app.py
import streamlit as st
import random

# ランダム選択肢データの設定
CHARACTER_AGE_CHOICES = [
    ('0-12', '0-12歳'),
    ('13-22', '13-22歳'),
    ('23-35', '23-35歳'),
    ('36-49', '36-49歳'),
    ('50-60', '50-60歳'),
    ('61+', '61歳以上~∞'),
]

CHARACTER_ROLE_CHOICES = [
    ('保育園児', '保育園児、幼稚園児'),
    ('小学生', '小学生'),
    ('中学生', '中学生'),
    ('高校生', '高校生'),
    ('大学生・専門学校生', '大学生・専門学校生'),
    ('専門的学校の学生', '専門的学校の学生'),
    ('専業主婦', '専業主婦'),
    ('警察官', '警察官（刑事、鑑識員、警視総監なども含む）'),
    ('消防士・救急隊員', '消防士・救急隊員（レスキュー隊含む）'),
    ('軍人', '軍人（自衛官、傭兵、架空の軍隊含む）'),
    ('教師', '教師（幼稚園教諭や家庭教師、大学教授、インストラクターなども含む）'),
    ('医師', '医師（レジデント、開業医、大学病院院長まで含む）'),
    ('看護師・ホームヘルパー', '看護師・ホームヘルパーなど'),
    ('政治家', '政治家（区議会議員から内閣総理大臣まで含む）'),
    ('秘書', '秘書（新人からベテランまで含む）'),
    ('マスコミ関係者', 'マスコミ関係者・組織人（新聞社記者、テレビ局報道局長なども含む）'),
    ('フリーランサー', 'フリーランサー（フリージャーナリスト、フリーアナウンサー、フリーライター、小説家、画家など）'),
    ('テレビ局・映画会社関係者', 'テレビ局・映画会社関係者（受付嬢から宣伝マン、社長まで含む）'),
    ('モデル・役者・タレント', 'モデル、役者、タレントなど（売れっ子、元売れっ子、修行中まで含む）'),
    ('マネージャー', 'マネージャー（タレントマネージャーから運動部マネージャーまで含む）'),
    ('プロデューサー', 'プロデューサー（音楽、イベント、映画、WEBなど含む）'),
    ('ディレクター・監督', 'ディレクターor監督（映画、音楽、アート、スポーツなども含む）'),
    ('スポーツ選手', 'スポーツ選手（部活動レベルからオリンピック選手まで含む）'),
    ('スポーツトレーナー', 'スポーツトレーナー（部活動レベルからオリンピック選手まで含む）'),
    ('アルバイト・フリーター', 'アルバイト、フリーター、家事手伝い'),
    ('店員・店主', '本屋、ビデオ屋、音楽ショップなどの店員、店主'),
    ('物販業', '物販業（ショッピングセンター、百貨店、スーパー、コンビニ、ホームセンターなど）'),
    ('飲食サービス業', '飲食サービス業（レストラン、ファミレス、喫茶店、居酒屋など）'),
    ('旅行・観光業', '旅行・観光業、リゾート、レジャー産業（ホテル、民宿、ツアー会社など）'),
    ('アミューズメント関連', 'アミューズメント関連（カラオケ、遊園地、ゲームセンターなど）'),
    ('ファッション関係者', 'ファッション関係者（和装、洋装、理容、美容、エステなど）'),
    ('運輸・配送業者', '運輸、配送業者（タクシー、トラック、地下鉄、漁船、飛行機など）'),
    ('犯罪者', '犯罪者（万引きから殺し屋、テロリストなど）'),
    ('聖職者', '聖職者（役職、宗派問わず）'),
]


INCITING_EVENT_CHOICES = [
    ('予想外の再会', '思わぬ人（モノ）と再会する'),
    ('予想外の出会い', '思わぬ人（モノ）と出会う'),
    ('会いたかった再会', '会いたかった人（モノ）と出会う or 再会する'),
    ('会いたくなかった再会', '会いたくなかった人（モノ）と出会う or 再会する'),
    ('望んでいたモノ', '望んでいたモノ（物質、情報、立場など）が届く（手に入れる）'),
    ('望んでいなかったモノ', '望んでいなかったモノ（物質、情報、立場など）が届く（手に入れる）'),
    ('予期していなかったモノ', '予期していなかったモノ（物質、情報、立場など）が届く（手に入れる）'),
    ('事件を起こす', '自分が事件 or 事故を起こしてしまう'),
    ('事故に巻き込まれる', '自分が事件 or 事故に巻き込まれてしまう'),
    ('身近な人が事件を起こす', '身近な人が事件 or 事故を起こしてしまう'),
    ('身近な人が事故に巻き込まれる', '身近な人が事件 or 事故に巻き込まれてしまう'),
    ('事件を目撃する(意図的)', '見ようとして事件 or 事故を目撃する'),
    ('事件を目撃する(偶然)', '見るつもりはなかったのに、事件 or 事故を目撃する'),
    ('立場に関連する指令', '立場や職業に関連した理由で指令を受ける'),
    ('立場と無関係の指令', '立場や職業に無関係な理由で指令を受ける'),
    ('プライベートに関連する指令', 'プライベートに関連した理由で指令を受ける'),
    ('プライベートと無関係の指令', 'プライベートに無関係な理由で指令を受ける'),
    ('見知らぬ場所', '見知らぬ場所で目覚める or 見知らぬ場所に到着する'),
    ('予定外の場所', '予定外の場所で目覚める or 予定外の場所に到着する'),
    ('記憶喪失', '気がつくと、すべての記憶がなくなっている'),
    ('記憶喪失(部分的)', '気がつくと、部分的に記憶がなくなっている'),
    ('身近な人の記憶喪失', '気がつくと、身近な人のすべての記憶がなくなっている'),
    ('身近な人の記憶喪失(部分的)', '気がつくと、身近な人の部分的な記憶がなくなっている'),
    ('世の中の良い変化', '知らないうちに、世の中がすっかり良い状況に変わっている'),
    ('世の中の悪い変化', '知らないうちに、世の中がすっかり悪い状況に変わっている'),
    ('肉体の良い変化', '知らないうちに、自分の肉体が良く変化している'),
    ('肉体の悪い変化', '知らないうちに、自分の肉体が悪く変化している'),
    ('信頼を裏切られる', '信じていた人に裏切られる or 騙される'),
    ('信頼を裏切る', '信じてくれていた人を裏切る or 騙す'),
    ('人違いされて迷惑', '人違いされて、迷惑する or 迷惑を掛ける'),
    ('人違いされて好都合', '人違いされて、自分にとって好都合 or 他人にとって好都合'),
    ('人違いして迷惑', '人違いして、迷惑する or 迷惑を掛ける'),
    ('人違いして好都合', '人違いして、自分にとって好都合 or 他人にとって好都合'),
    ('大切なものを失う', '大切なもの（物質、人、情報、地位、名誉など）を失う'),
    ('自分が困る秘密を抱える', '知られると自分が困る、という秘密を抱えてしまう'),
    ('他人が困る秘密を抱える', '知られると誰か他人が困る、という秘密を抱えてしまう'),
]

MAIN_STAGE_CHOICES = [
    ('個室', '個室'),
    ('建物', '建物'),
    ('街', '街'),
    ('国', '国'),
    ('世界', '世界'),
    ('その他', 'その他'),
]

GENRE_CHOICES = [
    ('ヒューマンドラマ', 'ヒューマンドラマ or コメディ'),
    ('アクション', 'アクション'),
    ('ラブストーリー', 'ラブストーリー'),
    ('サスペンス', 'サスペンス or ミステリー'),
    ('SF', 'SF or ファンタジー'),
    ('ホラー', 'ホラー'),
]

# ランダム選択のための関数
def random_choice_label(choices):
    return random.choice(choices)[1]

# Streamlitアプリの内容
st.title("三宅隆太さんの「物語ひらめきドリル」「お話しづくり書き込みシート」")

st.markdown("""
            「スクリプトドクターの脚本教室　中級編」(著・三宅隆太/新書館)に収録された
            
            ・「物語ひらめきドリル」
            
            ・「お話づくりのための書き込みシート」
            
            を活用する為のWebアプリです。使用法は書籍をご覧ください。
            
            ※非公式アプリです。出版社様とは関係ございません。
            """)

# ひらめきドリルの部分
st.header("物語ひらめきドリル")


# セッション状態を使用してデータを保持
if 'character_age' not in st.session_state:
    st.session_state.character_age = CHARACTER_AGE_CHOICES[0][1]
if 'character_role' not in st.session_state:
    st.session_state.character_role = CHARACTER_ROLE_CHOICES[0][1]
if 'inciting_event' not in st.session_state:
    st.session_state.inciting_event = INCITING_EVENT_CHOICES[0][1]
if 'main_stage' not in st.session_state:
    st.session_state.main_stage = MAIN_STAGE_CHOICES[0][1]
if 'genre' not in st.session_state:
    st.session_state.genre = GENRE_CHOICES[0][1]

# ランダム選択ボタン
if st.button("ランダムに選択"):
    st.session_state.character_age = random.choice(CHARACTER_AGE_CHOICES)[1]
    st.session_state.character_role = random.choice(CHARACTER_ROLE_CHOICES)[1]
    st.session_state.inciting_event = random.choice(INCITING_EVENT_CHOICES)[1]
    st.session_state.main_stage = random.choice(MAIN_STAGE_CHOICES)[1]
    st.session_state.genre = random.choice(GENRE_CHOICES)[1]

# ドロップダウンにセッション状態を反映
character_age = st.selectbox(
    "主人公の年齢",
    options=[label for _, label in CHARACTER_AGE_CHOICES],
    index=[label for _, label in CHARACTER_AGE_CHOICES].index(st.session_state.character_age)
)

character_role = st.selectbox(
    "主人公の職業・立場",
    options=[value for value, _ in CHARACTER_ROLE_CHOICES],
    index=[label for _, label in CHARACTER_ROLE_CHOICES].index(st.session_state.character_role)
)

character_role_label = next(label for value, label in CHARACTER_ROLE_CHOICES if value == character_role)
st.write(character_role_label)

inciting_event = st.selectbox(
    "きっかけとなる出来事",
    options=[value for value, _ in INCITING_EVENT_CHOICES],
    index=[label for _, label in INCITING_EVENT_CHOICES].index(st.session_state.inciting_event)
)

inciting_event_label = next(label for value, label in INCITING_EVENT_CHOICES if value == inciting_event)
st.write(inciting_event_label)

main_stage = st.selectbox(
    "主な舞台",
    options=[label for _, label in MAIN_STAGE_CHOICES],
    index=[label for _, label in MAIN_STAGE_CHOICES].index(st.session_state.main_stage)
)

genre = st.selectbox(
    "ジャンル",
    options=[label for _, label in GENRE_CHOICES],
    index=[label for _, label in GENRE_CHOICES].index(st.session_state.genre)
)

# フォームの作成
st.header("お話づくりのための書き込みシート")

character_name = st.text_input("1.あなたの主人公の名前", "")
with st.expander("1-1 ~ 1-5 主人公の詳細"):
    character_age_input = st.text_input("1-1. 年齢", character_age)
    character_role_input = st.text_input("1-2. 職業 or 立場", character_role_label)
    character_personality = st.text_area("1-3. 性格", "")
    character_likes = st.text_area("1-4. 主人公の好きなもの or こと", "")
    character_dislikes = st.text_area("1-5. 主人公の嫌いなもの or こと", "")
story_goal = st.text_area("2.あなたのお話は、主人公が何をしようとする話ですか？", "")
message = st.text_area("3.あなたのお話を通じて読み手に伝えたいことはありますか？", "")
outline = st.text_area("4.あなたのお話の「あらすじ」を二行程度で書いてみてください", "")
climax = st.text_area("5.「クライマックス」には、どんな出来事が起こりますか？", "")
pre_climax_event = st.text_area("6.「クライマックスの直前」には、どんな出来事が起きますか？", "")
inciting_event_input = st.text_area("7.あなたのお話の「きっかけとなる出来事（事件）」はどんなことですか？", inciting_event_label)
ending = st.text_area("8.あなたのお話は、どんな「ラスト」を迎えますか？", "")
conflict = st.text_area("9.お話の中間部で起きる「葛藤・衝突」はどんなことですか？", "")
antagonist_name = st.text_input("10.主人公にとっての「敵対者」の名前", "")
with st.expander("10-1 ~ 10-3 敵対者の詳細"):
    antagonist_personality = st.text_area("10-1. 敵対者の性格", "")
    antagonist_likes = st.text_area("10-2. 敵対者の好きなもの or こと", "")
    antagonist_dislikes = st.text_area("10-3. 敵対者の嫌いなもの or こと", "")
ally_name = st.text_input("11.主人公にとっての「協力者」の名前", "")
with st.expander("11-1 ~ 11-3 協力者の詳細"):
    ally_personality = st.text_area("11-1. 協力者の性格", "")
    ally_likes = st.text_area("11-2. 協力者の好きなもの or こと", "")
    ally_dislikes = st.text_area("11-3. 協力者の嫌いなもの or こと", "")
break_shell = st.text_area("12.主人公にとって破るべき「殻」は何ですか？", "")
personal_meaning = st.text_area("13.あなたにとって、あなたの物語はどんな意味を持つものですか？", "")

st.header("入力内容をコピー")
st.markdown("下のボックスの右上にある四角ボタンをクリックするとコピーできます👇")

generated_text = f"""
物語ひらめきドリル

主人公の年齢
{character_age_input}

主人公の職業・立場
{character_role_input}

きっかけとなる出来事
{inciting_event_input}

主な舞台
{main_stage}

ジャンル
{genre}

お話づくりのための書き込みシート

1.あなたの主人公の名前
{character_name}

1-1. 年齢
{character_age_input}

1-2. 職業 or 立場
{character_role_input}

1-3. 性格
{character_personality}

1-4. 主人公の好きなもの or こと
{character_likes}

1-5. 主人公の嫌いなもの or こと
{character_dislikes}

2.あなたのお話は、主人公が何をしようとする話ですか？
{story_goal}

3.あなたのお話を通じて読み手に伝えたいことはありますか？
{message}

4.あなたのお話の「あらすじ」を二行程度で書いてみてください
{outline}

5.「クライマックス」には、どんな出来事が起こりますか？
{climax}

6.「クライマックスの直前」には、どんな出来事が起きますか？
{pre_climax_event}

7.あなたのお話の「きっかけとなる出来事（事件）」はどんなことですか？
{inciting_event_input}

8.あなたのお話は、どんな「ラスト」を迎えますか？
{ending}

9.お話の中間部で起きる「葛藤・衝突」はどんなことですか？
{conflict}

10.主人公にとっての「敵対者」の名前
{antagonist_name}

10-1. 性格
{antagonist_personality}

10-2. 敵対者の好きなもの or こと
{antagonist_likes}

10-3. 敵対者の嫌いなもの or こと
{antagonist_dislikes}

11.主人公にとっての「協力者」の名前

11-1. 性格
{ally_personality}

11-2. 敵対者の好きなもの or こと
{ally_likes}

11-3. 敵対者の嫌いなもの or こと
{ally_dislikes}

12.主人公にとって破るべき「殻」は何ですか？
{break_shell}

13.あなたにとって、あなたの物語はどんな意味を持つものですか？
{personal_meaning}


"""

# コードブロックとして表示（コピーボタンが自動で付与されます）
st.code(generated_text, language="text")