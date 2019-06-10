##############################################
#                                            #
# Discord 봇 Base 스크리트                      #
# SideWinderk(sidewinderkr@gmail.com)        #
#                                            #
##############################################
 
import discord
import asyncio
import time
import ast
import os
import random
import requests
from io import BytesIO
import os
import msgcut
import re

import config
import defaultNotiParser

# Baseline
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Base DIR
client = discord.Client()                             # Discord client
notepad = dict()                                      # Dictionary for note

# Initializing
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    # 봇 이름을 봇을 켤 때마다 config.botname을 기준으로 수정해줍니다.
    await client.edit_profile(username=config.bot_name) 

    # Discord 유저 상태창(봇의 상태)에 나타나는 문구입니다.
    g = discord.Game(name=config.bot_status_msg,type=1)

    # 봇 상태변경.(online,away,dnd,invisible, 기본값 = dnd)
    await client.change_presence(status=discord.Status(config.bot_status),game=g)

    # 'save.txt' 파일로부터 유저 사전데이터를 notepad 라는 dict() 변수로 로드합니다.
    # 사전 파일이 없을 때의 예외처리를 해줘야할지? -> 나중에 하자.
    with open(os.path.join(BASE_DIR, config.dict_file), 'r+') as f_read:
        if os.path.getsize(config.dict_file) != 0:
            savefile = ast.literal_eval(f_read.read())
            notepad.update(savefile)
        f_read.close()

    # 정상 가동 알림 채팅
    await client.send_message(client.get_channel(config.bot_channel),config.wakeup_text)
    
    # 봇이 켜져있는동안 계속 도는 루프(아래 명령어 처리와 별개.)
    # 기본 루프 반복 주기: 120초 
    # 1. Notiparser 를 실행, 특정 사이트에 새로운 글이 있는지 확인
    # 2. 유저사전을 파일에 저장(백업)
    while(1):
       try:
          # Notification parser
          post = defaultNotiParser.get_latest()
          if post != 0: # 변경사항이 있을 때만,
             post = post.split(",") # 타이틀,링크 -> [ 타이틀, 링크 ]
             text = "새로운 공지사항: %s %s" % (post[0], post[1]) # post[0]: 타이틀, post[1]: 링크
             await client.send_message(client.get_channel(config.bot_noti_channel),text)

          # 유저 사전 파일 저장
          with open(os.path.join(BASE_DIR, config.dict_file), 'w') as f_write:
             f_write.write(str(notepad))
             f_write.close()

          # 지정한 시간만큼 sleep 
          await asyncio.sleep(config.bot_refresh_interval)
       except: # 예외
          # 보통은 공지를 너무 자주 긁어서 에러가 나는 경우가 있음
          await client.send_message(client.get_channel(config.bot_channel),config.noti_refresh_fail)

## 유저용 반응형 명령어들
# 기본 적으로, if message.content.startswith("특정문구") 를 기준으로
# "특정문구"가 채팅창에 나타나면 그 if문을 실행하는 방식.
@client.event
async def on_message(message):
    
    # 이름을 불렸을 때 
    if message.content.startswith(config.bot_name):
       name_response = '살아있습니다! %s(%s)님, 명령어는 #potofgreed 채널의 핀메세지나 ! 도움 으로확인해주세요.'%(message.author.name, message.author.id)
       await client.send_message(message.channel, name_response)
    
    ### 유저 사전 관련 명령어들
    # 추가 -> 사전에 추가하기
    # 구분자 :: <- 더 좋은걸 발견하지 못함
    if "!추가" in message.content:
       note = msgcut.cutmsg(message.content)
       note = note.split('::')
       notepad[note[0]] = note[1]
       note_add_text = '%s에 %s 항목을 기록하였습니다.'%(config.botdict_name, note[0])
       await client.send_message(message.channel, note_add_text)
    
    # 검색 -> 사전 검색
    # 노트에 키워드가 있을 때 -> 그 키워드를 포함하는 모든 내용을 리턴
    # --키워드가 없을 때 -> 없다고 함(솔직)
    if "!검색" in message.content:
       keyword = msgcut.cutmsg(message.content)
       if(message.content == "!검색"): keyword = "" #물론 !검색은 제외 ^^;;
       matching = [s for s in notepad if keyword in s]
       if len(matching) != 0:
           result = ""
           for s in matching: result = result + " | "  + s # 포함하는걸 다 보여주자.
           find_text1 = '%s에서 %s에 대한 항목을 찾았습니다: %s'%(config.botdict_name,keyword,result)
           await client.send_message(message.channel, find_text1)
       else:
           find_text2 = '%s에 %s에 대한 항목이 없습니다.'%(config.botdict_name,keyword)
           await client.send_message(message.channel, find_text2)
    
    # 확인 -> 사실상 (괄호) 때문에 사장된 느낌.
    if "!확인" in message.content:
       keyword = msgcut.cutmsg(message.content)
       if keyword in notepad:
           check_text1 = '[%s] %s'%(keyword,notepad[keyword])
           await client.send_message(message.channel, check_text1)
       else:
           check_text2 = '%s에 %s에 대한 항목이 없습니다.'%(config.botdict_name, keyword)
           await client.send_message(message.channel, check_text2)

    # 삭제
    # 잘 안쓰이긴하는데, 가아끔 유용함.
    if "!삭제" in message.content:
       keyword = msgcut.cutmsg(message.content)
       if keyword in notepad:
           del notepad[keyword]
           deltext1 = '%s에서 %s에 대한 항목을 삭제했습니다.'%(config.botdict_name, keyword)
           await client.send_message(message.channel, deltext1)
       else:
           deltext2 = '%s에 %s에 대한 항목이 없습니다.'%(config.botdict_name, keyword)
           await client.send_message(message.channel, deltext2)
    
    # 단축 명령어
    # (괄호)에 뭔가 적으면 바로 확인해주는 친절한 기능
    # 짤방 소환 등에 사용
    if message.content.count("(") == 1 and message.content.count(")") == 1:
       keyword = message.content[message.content.find("(")+1:message.content.find(")")]
       if keyword in notepad:
           await client.send_message(message.channel, '%s'%(notepad[keyword]))
    ##### 유저 사전 기능 끝 #

    # 도움말 기능
    # discord embed 형식 메세지를 활용.
    if "!도움"  in message.content:
       keyword = msgcut.cutmsg(message.content)
       em = discord.Embed(title='명령어 리스트', description='명령어 리스트는 아래와 같습니다.', colour=0xDEADBF)
       em.add_field(name="!추가",value="노트에 내용을 추가합니다. 키워드::내용 순으로 입력합니다.\n`ex) !추가 마지막서프::2017년 5월 5일`",inline=True)
       em.add_field(name="!검색",value="노트 키워드를 검색합니다. 전체 이름을 입력하지 않아도 검색이 됩니다. \n아무것도 입력하지 않으면 >전체 목록을 보여줍니다. \n`ex) !검색 서프`",inline=True)
       em.add_field(name="!확인",value="노트 내용을 보여줍니다. 정확한 키워드를 입력해야합니다.\n`ex) !확인 마지막서프`",inline=True)
       em.add_field(name="!삭제",value="노트를 삭제합니다. 정확한 키워드를 입력해야합니다.\n`ex) !삭제 마지막서프`",inline=True)
       em.add_field(name="!도움",value="이 도움말을 여는 명령어입니다.",inline=True)
       em.set_author(name=config.bot_name, icon_url=client.user.default_avatar_url)
       await client.send_message(message.channel, embed=em)
    
    # 주사위 기능
    # 혹시나 해서 넣어봤는데 역시나 안쓰인다.
    if "!주사위" in message.content:
       dice = [1,2,3,4,5,6]
       roll = random.choice(dice)
       await client.send_message(message.channel, '주사위 결과: %s'%roll)
    
    # 랜덤 기능
    # 0~100 사이 랜덤 숫자를 뱉음, 역시나 안쓰이더라.
    if "!랜덤" in message.content:
       number = int(random.random() * 100)
       await client.send_message(message.channel, '%s'%number)

client.run(config.token)
