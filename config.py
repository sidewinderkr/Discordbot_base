
# 봇 설정
bot_name = "봇이름" # 표기될 봇이름.
bot_status_msg = "%s<-명령어확인"%bot_name # 봇 상태창 메세지, 기본값:봇이름<-명령어확인
bot_status = 'dnd' # 봇 상태: online,away,dnd,invisible, 기본값 = dnd
dict_file = "save.txt" # 유저 사전이 저장될 파일명
botdict_name = "사전" # 봇 사전 이름

bot_refresh_interval = 120 # 명령어 입력제외 자동 처리(parser 등)을 반복확인하는 주기, 기본값: 120 (초)

# 봇 메세지 설정
wakeup_text = "죽었다가.. 다시 살아났습니다..." # 가동될 때 봇 채널에 던지는 말
noti_refresh_fail = "공지를 긁어오는데 실패 했습니다." # 공지 긁는거 실패했을 때 

# 디스코드 특화 설정
# 채널명은 디스코드에서 해당채널 우클릭->ID복사
# (그런 메뉴가 안보이면 디스코드 설정-외관-개발자모드 켜기)
bot_channel = "332203007121031173" #봇 전용 메세지가 출력될 채널
bot_noti_channel = "329817797523931136" #봇 공지 메세지가 출력될 채널

bot_token = "봇토큰" #봇 전용 토큰 -> 외부 유출시 위험.
