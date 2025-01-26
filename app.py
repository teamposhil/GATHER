import discord
from discord.ext import commands
from discord import app_commands
import datetime
import pytz
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import random
load_dotenv()  # .env 파일 로드
token = os.getenv("DISCORD_BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
# MongoDB 클라이언트 설정
client = MongoClient(MONGO_URI)
userdb = client["user"]  # 데이터베이스 이름
user_collection = userdb["user"]

stockdb = client["stocks"]
stock_domestic_collection = stockdb["domestic"]
stock_international_collection = stockdb["international"]
rate_collection = stockdb["rate"]
start_time = datetime.datetime.utcnow()  # 봇 시작 시간 기록

sasungin1 = 0
sasungin2 = stock_international_collection.find_one({"company_name": "SASUNG"})["price"]
pear1 = 0
pear2 = stock_international_collection.find_one({"company_name": "PEAR"})["price"]
envidia1 = 0
envidia2 = stock_international_collection.find_one({"company_name": "ENVIDIA"})["price"]
hiot1 = 0
hiot2 = stock_international_collection.find_one({"company_name": "HIOTGAMES"})["price"]
qalmart1 = 0
qalmart2 = stock_international_collection.find_one({"company_name": "QALMART"})["price"]
ppizer1 = 0
ppizer2 = stock_international_collection.find_one({"company_name": "PPIZER"})["price"]
sasungdo1 = 0
sasungdo2 = stock_domestic_collection.find_one({"company_name": "SASUNG"})["price"]
og1 = 0
og2 = stock_domestic_collection.find_one({"company_name": "OG"})["price"]
jongshim1 = 0
jongshim2 = stock_domestic_collection.find_one({"company_name": "jongshim"})["price"]
lyundai1 = 0
lyundai2 = stock_domestic_collection.find_one({"company_name": "lyundai"})["price"]
rate = rate_collection.find_one({"codecheck": "code"})["rate"]

# 봇 초대 URL 생성 함수
def get_invite_url(bot_id):
    return f"https://discord.com/api/oauth2/authorize?client_id={bot_id}&permissions=8&scope=bot%20applications.commands"


bot = commands.Bot(command_prefix='/ ', intents=discord.Intents.all(), help_command=None)


@bot.event
async def on_ready():
    print(f'{bot.user.name} 봇, 서버에 출격 준비 완료!')
    game = discord.Game("서버에서 일")
    await bot.change_presence(status=discord.Status.online, activity=game)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands with Discord.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.tree.command(name='공지하기', description="공지할 내용을 입력해주세요!")
@app_commands.describe(title='공지할 내용의 제목을 입력해주세요!', inputs='공지할 내용을 입력해주세요!', code='관리자인지 확인하는 절차입니다!')
async def 공지하기(interaction: discord.Interaction, title: str, inputs: str, code: int):
    if code == 110010011:
        embed = discord.Embed(title=title, description=inputs, color=0x62c1cc)
        await interaction.response.send_message(content="@everyone", embed=embed, ephemeral=False)
    else:
        await interaction.response.send_message(content="당신은 관리자임을 인증하기 못하셨어요! 이 명령어는 관리자만 사용할 수 있습니다!", ephemeral=True)


@bot.tree.command(name="내통장", description="통장을 확인합니다!")
async def 내통장(interaction: discord.Interaction):
    user = interaction.user  # 명령을 호출한 유저
    db_user = user_collection.find_one({"user_id": user.id})
    embed = discord.Embed(
        title=f"{user.name}님의 통장",  # 제목에 유저의 닉네임 넣기
        description="고객님의 잔액을 보여드립니다.",  # 설명 부분에 유저 ID
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    if db_user:
        balance = db_user.get("balancegm", 0)
        balancedt = db_user.get("balancedt", 0)
        rank = ""
        master = 0
        if balance >= 1000000 and balance < 3000000:
            rank = "Bronze"
            tier = int(balance / 500000) - 1
        elif balance >= 3000000 and balance < 5000000:
            rank = "Silver"
            tier = int(balance / 500000) - 5
        elif balance >= 5000000 and balance < 7000000:
            rank = "Gold"
            tier = int(balance / 500000) - 9
        elif balance >= 7000000 and balance < 9000000:
            rank = "Platinum"
            tier = int(balance / 500000) - 13
        elif balance >= 9000000 and balance < 110000000:
            rank = "Diamond"
            tier = int(balance / 500000) - 17
        elif balance >= 110000000:
            rank = "Master"
            tier = 999
            master = 1
        embed.add_field(name="현재 잔액(Game Money): ", value=f"{balance}GM, {balancedt}DT", inline=False)
        embed.add_field(name="현재 랭크: ", value=f"{rank} {tier}", inline=False)
        if master == 1:
            embed.add_field(name="마스터 랭크: ", value="당신은 1억 1천만GM 이상을 보유하고 있으므로 마스터등급입니다! 축하합니다!!", inline=False)
    else:
        embed.add_field(name="게더 주식에 가입되어 있지 않습니다!", value="게더 주식에 가입하시려면 /유저등록 명령어를 사용해주세요!", inline=False)
    embed.set_thumbnail(url=user.avatar.url)  # 프로필 사진을 썸네일로 설정
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name='심심하다', description='심심해')
async def 심심하다(interaction: discord.Interaction):
    await interaction.response.send_message("어?쩔?", ephemeral=False)


@bot.tree.command(name='세계주식소개', description='세계 주식 중 게더 주식에 업로드 되어있는 주식들의 이름을 표시합니다!')
async def 세계주식소개(interaction: discord.Interaction):
    embed = discord.Embed(
        title="게더 주식-NYSE(뉴욕증권거래소)",
        description="게더 주식에 상장된 주식들 중 세계주식에 해당되는 주식입니다.",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="사성전자인터내셔널(SASUNG ELECTRONIC)", value="분류코드: 001, 대한민국의 최대 전자제품 제조사입니다! 주로 은하수폰을 판매합니다!",
                    inline=False)
    embed.add_field(name="배(PEAR)", value="분류코드: 002, 미국 최대의 스마트폰 제조사입니다. 주로 페어폰을 판매합니다!", inline=False)
    embed.add_field(name="은비디아(ENVIDIA)", value="분류코드: 018, 세계적인 전자제품 생산업체이며, 주로 ETX 그래픽카드를 판매합니다!", inline=False)
    embed.add_field(name="하이엇게임즈(HIOTGAMES)", value="분류코드:097, 세계 1등 게임인 랭킹 오브 레전드와 FPS 게임 잘로란트를 제작한 회사입니다!",
                    inline=False)
    embed.add_field(name="월마트(QALMART)", value="분류코드:356, 미국 최대의 대형 마트 프렌차이즈며, 우리나라에서는 기마트라는 이름으로 운영됩니다!", inline=False)
    embed.add_field(name="파이자(PPIZER)", value="분류코드:890, 세계적으로 유명한 의약품 회사로, 제일 믿을만한 의약품 기업 1위라는 타이틀을 가지고 있습니다!",
                    inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name='국내주식소개', description='국내 주식 중 게더 주식에 업로드 되어있는 주식들의 이름을 표시합니다!')
async def 국내주식소개(interaction: discord.Interaction):
    embed = discord.Embed(
        title="게더 주식-KOSPI(유가증권시장)",
        description="게더 주식에 상장된 주식들 중 국내주식에 해당되는 주식입니다.",
        color=discord.Color.yellow(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="사성전자(SASUNG ELECTRONIC)", value="분류코드: A-1, 대한민국의 최대 전자제품 제조사입니다! 주로 은하수폰을 판매합니다!",
                    inline=False)
    embed.add_field(name="오지전자(OG ELECTRONICS)", value="분류코드: A-3, 세계에서 가장 모니터를 잘 만드는 회사입니다. 주로 WLED TV를 판매합니다!",
                    inline=False)
    embed.add_field(name="종심(JONGSHIM)", value="분류코드: E-7, 대한민국의 최대 가공식품 판매사입니다! 주로 라면과 과자를 판매합니다!", inline=False)
    embed.add_field(name="련대(LYUNDAI)", value="분류코드:097, 세계 최고 기술력의 중공업 회사로, 요즘엔 아파트도 건설합니다!", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='주식', description='주식을 구매하거나 판매합니다!')
@app_commands.choices(sellorbuy=[
    app_commands.Choice(name="판매", value="판매"),
    app_commands.Choice(name="구매", value="구매"), ])
@app_commands.choices(intordom=[
    app_commands.Choice(name="세계", value="세계"),
    app_commands.Choice(name="국내", value="국내"), ])
async def 주식(interaction: discord.Interaction, sellorbuy: app_commands.Choice[str], intordom: app_commands.Choice[str]):
    user_id = interaction.user.id
    if sellorbuy.value == '판매':
        if intordom.value == '세계':
            print("world")
    else:
        if intordom.value == '국내':
            print("domestic")


    await interaction.response.send_message("개발중...", ephemeral=True)



@bot.tree.command(name='가위바위보하기', description='가위,바위,보자기 중 하나를 입력해주세요!')
@app_commands.describe(입력창='가위? 바위? 보자기?')
async def 가위바위보하기(interaction: discord.Interaction, 입력창: str):
    rsp = random.choice(["가위", "바위", "보자기"])
    if 입력창 == rsp:
        result = f"가위바위보! 비겼어요! 저도 {rsp}를 냈거든요! 다시 한판 하실래요?"
    elif (입력창 == "가위" and rsp == "보자기") or (입력창 == "바위" and rsp == "가위") or (입력창 == "보자기" and rsp == "바위"):
        result = f"가위바위보! 당신이 이겼어요! 저는 {rsp}를 냈거든요... 축하해요!"
    elif (입력창 == "가위" and rsp == "바위") or (입력창 == "바위" and rsp == "보자기") or (입력창 == "보자기" and rsp == "가위"):
        result = f"가위바위보! 제가 이겼어요!저는 {rsp}를 냈거든요! 가위바위보 못하시네 ㅋㅋㅋㅋ"
    else:
        result = "가위바위보! 어라..? 손이 안움직여져요! 가위,바위,보자기중에서 입력했는지 확인해보세요! 그래도 안되면 @부서버장 에게 도움을 요청해주세요!"
    await interaction.response.send_message(result, ephemeral=True)


@bot.tree.command(name='초대하기', description="서버에 게더를 추가하는 버튼을 출력해드려요!")
async def 추가(interaction: discord.Interaction):
    view = discord.ui.View()
    button1 = discord.ui.Button(
        label="게더봇 내 서버에 추가하기",
        url="https://discord.com/oauth2/authorize?client_id=1316915541709029467&permissions=0&integration_type=0&scope=bot",
        style=discord.ButtonStyle.link
    )
    view.add_item(button1)
    await interaction.response.send_message(view=view)


@bot.tree.command(name='도움말', description="게더의 명령어를 알려드려요!")
async def 도움말(interaction: discord.Interaction):
    embed = discord.Embed(
        title="도움말",
        description="게더의 명령어를 알려드립니다!",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="/도움말", value="명령어 도움말을 알려드려요!", inline=False)
    embed.add_field(name="/정보", value="게더의 작동시간, 제작자, 나이, 게더초대링크를 알려드려요!", inline=False)
    embed.add_field(name="/공지하기", value="관리자코드를 사용하여 모든 서버원에게 공지를 해드려요!", inline=False)
    embed.add_field(name="/초대하기", value="게더를 서버에 초대할 수 있는 링크를 드려요!", inline=False)
    embed.add_field(name="/심심하다", value="???를 말해드려요!", inline=False)
    embed.add_field(name="/유저등록", value="게더 주식서비스에 가입해요!", inline=False)
    embed.add_field(name="/유저탈퇴", value="게더 주식서비스에서 탈퇴해요!", inline=False)
    embed.add_field(name="/내통장", value="게더 주식의 통장을 확인해요!", inline=False)
    embed.add_field(name="/주식시장", value="게더 주식에 상장된 주식들을 확인해요!", inline=False)
    embed.add_field(name="/가위바위보하기", value="저와 가위바위보 한판을 진행하요!", inline=False)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='ㅗ', description="for 욕쟁이들")
async def ㅗ(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"온세상사람들! {interaction.user.name}가 저한테 뻐큐를 날려요! 이런 인성  파탄난 놈을 어떻게 할까요~~~~~~?:어쩌라고", ephemeral=False)


@bot.tree.command(name='정보', description="게더의 정보를 알려드려요!")
async def 정보(interaction: discord.Interaction):
    # 봇 작동 시간 계산
    uptime = datetime.datetime.utcnow() - start_time
    uptime_str = str(uptime).split('.')[0]  # 초 단위로 표시
    # 임베드 생성
    embed = discord.Embed(
        title="게더의 정보",
        description="게더의 정보입니다!",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="봇 이름", value=f"{bot.user.name}", inline=False)
    embed.add_field(name="작동 시간", value=uptime_str, inline=False)
    embed.add_field(name="나이", value="약 4개월", inline=False)
    embed.add_field(name="제작자", value="devloggerkr", inline=False)  # 제작자 정보
    embed.set_footer(text="GATHER")
    # 봇 추가 버튼 생성
    view = discord.ui.View()
    button = discord.ui.Button(
        label="게더봇 내 서버에 초대하기",
        url="https://discord.com/oauth2/authorize?client_id=1316915541709029467&permissions=0&integration_type=0&scope=bot",
        style=discord.ButtonStyle.link
    )
    view.add_item(button)
    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(name='유저등록', description='유저를 게더 주식에 등록합니다.')
async def 유저등록(interaction: discord.Interaction):
    user_id = interaction.user.id  # 유저 ID 가져오기
    user_data = user_collection.find_one({"user_id": user_id})  # DB에서 유저 검색
    user_name = interaction.user.name
    channel = bot.get_channel(1330453187634663487)
    utc_now = datetime.datetime.now(pytz.utc)

    # 한국 시간대(KST)로 변환
    kst = pytz.timezone('Asia/Seoul')
    kst_now = utc_now.astimezone(kst)

    if user_data:
        await interaction.response.send_message("이미 등록된 유저입니다!", ephemeral=True)
    else:
        # 초기 데이터 설정
        new_user = {
            "user_id": user_id,
            "user_name": user_name,
            "balancegm": 1000000,  # 초기 자본
            "balancedt": 0,
            "registered_at": datetime.datetime.utcnow()
        }
        user_collection.insert_one(new_user)  # DB에 유저 데이터 삽입
        await interaction.response.send_message(f"{user_name}님! 게더 주식에 등록하신것을 축하드립니다! 초기 자본금은 1,000,000GM입니다!",
                                                ephemeral=True)
        await channel.send(f"{user_name}님이{kst_now.strftime('%Y-%m-%d %H:%M:%S')}에 게더 주식에 등록되었습니다!")


@bot.tree.command(name='유저탈퇴', description='데이터베이스에서 유저를 삭제합니다.')
async def 유저탈퇴(interaction: discord.Interaction):
    user_id = interaction.user.id  # 유저 ID 가져오기
    user_name = interaction.user.name
    user_data = user_collection.find_one({"user_id": user_id})  # DB에서 유저 검색
    channel = bot.get_channel(1330453187634663487)
    utc_now = datetime.datetime.now(pytz.utc)
    kst = pytz.timezone('Asia/Seoul')
    kst_now = utc_now.astimezone(kst)
    if user_data:
        user_collection.delete_one({"user_id": user_id})  # 유저 데이터 삭제
        await interaction.response.send_message("게더 주식에서 성공적으로 탈퇴되었습니다! 그동안 이용해주셔서 감사합니다!", ephemeral=True)
        await channel.send(f"{user_name}님이{kst_now.strftime('%Y-%m-%d %H:%M:%S')}에 게더 주식에서 탈퇴되었습니다!")
    else:
        await interaction.response.send_message("등록되지 않은 유저입니다.", ephemeral=True)
bot.run(token)
