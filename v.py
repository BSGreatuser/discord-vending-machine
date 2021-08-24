'''
질문은 
https://discord.gg/sBUXRGc
봉순#1234
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from discord.ext import tasks
from itertools import cycle

import discord, sqlite3, datetime, asyncio, time, configparser, os, sys, json

player_dict = dict()
print("=================================================")
print("봉순#1234\nhttps://봉순.com\n이 프로그램은 무료로 배포되는 프로그램입니다\n")
print("=================================================")

with open('setting.json', 'r', encoding='utf-8-sig') as boo:
    data = json.load(boo)

token = data['token']
customstatus = data['customstatus']
guildid = data['guildid']

client = discord.Client()

config = configparser.ConfigParser()

db = sqlite3.connect('main.sqlite')
cursor = db.cursor()

db2 = sqlite3.connect('items.sqlite')
cursor2 = db2.cursor()

y = datetime.datetime.now().year
m = datetime.datetime.now().month
d = datetime.datetime.now().day
h = datetime.datetime.now().hour
mn = datetime.datetime.now().minute

aaa = "{0}{1}{2}{3}{4}".format(y, m, d, h, mn)

status = cycle(['!명령어', customstatus])

guildid = int(guildid)

cantuse = discord.Embed(color=0xFF0000)
cantuse.add_field(name='❌  명령어 사용불가 채널', value='해당 명령어는 이 채널에서 사용할 수 없습니다')

permiss = discord.Embed(color=0xFF0000)
permiss.add_field(name='❌  권한 부족', value='명령어 사용권한이 부족합니다')

#####################################################################
###############################################################################################

@client.event
async def on_connect():
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS main(
            user TEXT,
            user_id TEXT,
            money TEXT,
            black TEXT,
            wrong_pin TEXT,
            accumulated TEXT
            )
        ''')
    cursor2.execute('''
                CREATE TABLE IF NOT EXISTS main(
                item_name TEXT,
                item_price TEXT
                )
            ''')
    change_message.start()
    print("[+] {0}(으)로 접속됨".format(client.user.name))


def is_not_pinned(mess):
    return not mess.pinned


@client.event
async def on_message(message):
    with open('setting.json', 'r', encoding='utf-8-sig') as boo:
        data1 = json.load(boo)
    buylogchannel = data1['buylogchannel']
    chargelogchannel = data1['chargelogchannel']
    regichannel = data1['regichannel']
    chargechannel = data1['chargechannel']
    infochannel = data1['infochannel']
    listchannel = data1['listchannel']
    buychannel = data1['buychannel']

    buylogchannel = int(buylogchannel) #구매로그 채널
    chargelogchannel = int(chargelogchannel) #충전로그 채널
    regichannel = int(regichannel)  # 가입 채널
    chargechannel = int(chargechannel)  # 충전신청 채널
    infochannel = int(infochannel)  # 정보 채널
    listchannel = int(listchannel)  # 제품목록 채널
    buychannel = int(buychannel)  # 구매 채널

    if "./" in message.content or "../" in message.content or ".\\" in message.content or "..\\" in message.content:
        return
                 
    if message.author.bot:
        return

    if not message.guild.id == guildid:
        return

    if message.content == '!가입채널' or message.content == '!구매로그채널' or message.content == '!충전로그채널' or message.content == '!충전신청채널' or message.content == '!충전채널' or message.content == '!내정보채널' or message.content == '!정보채널' or message.content == '!제품목록채널' or message.content == '!구매채널' or message.content == '!구입채널':
        if message.author.guild_permissions.administrator:
            try:
                with open('setting.json', 'r', encoding='utf-8-sig') as boo:
                    data = json.load(boo)

                if message.content == '!가입채널': #
                    data['regichannel'] = message.channel.id 
                    name = '가입'
                if message.content == '!구매로그채널': #
                    data['buylogchannel'] = message.channel.id
                    name = '구매로그'
                if message.content == '!충전로그채널': #
                    data['chargelogchannel'] = message.channel.id 
                    name = '충전로그'
                if message.content == '!충전신청채널' or message.content == '!충전채널': #
                    data['chargechannel'] = message.channel.id
                    name = '충전신청'
                if message.content == '!내정보채널' or message.content == '!정보채널': #
                    data['infochannel'] = message.channel.id
                    name = '내정보'
                if message.content == '!제품목록채널': #
                    data['listchannel'] = message.channel.id 
                    name = '제품목록'
                if message.content == '!구입채널' or message.content == '!구매채널': #
                    data['buychannel'] = message.channel.id
                    name = '구매채널'

                with open('./setting.json', 'w', encoding='utf-8-sig') as making:
                    json.dump(data, making, indent="\t")

                await message.channel.send(embed=discord.Embed(title=f'{name}채널 수정됨', description=f'{message.channel.mention}', colour=discord.Colour.green()))
            except:
                embed = discord.Embed(title='❌  오류', description='예끼치 않은 오류가 발생하였습니다', colour=0xFF0000)
                await message.channel.send(embed=embed)
                return
        else:
            await message.channel.send(embed=permiss)

    if message.content == '!채널설정값':
        if message.author.guild_permissions.administrator:
            with open('setting.json', 'r', encoding='utf-8-sig') as boo:
                data = json.load(boo)
            chrlog = data['chargelogchannel']
            bylog = data['buylogchannel']
            r = data['regichannel']
            char = data['chargechannel']
            inf = data['infochannel']
            listc = data['listchannel']
            by = data['buychannel']
            
            embed = discord.Embed()
            embed.add_field(name='가입채널', value=f'<#{r}>')
            embed.add_field(name='충전채널', value=f'<#{char}>')
            embed.add_field(name='내정보채널', value=f'<#{inf}>')
            embed.add_field(name='제품목록채널', value=f'<#{listc}>')
            embed.add_field(name='구매채널', value=f'<#{by}>')
            embed.add_field(name='충전로그채널', value=f'<#{chrlog}>')
            embed.add_field(name='구매로그채널', value=f'<#{bylog}>')
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(embed=permiss)

    
    if message.content == '!도움' or message.content == '!도움말' or message.content == '!명령어':
        embed = discord.Embed(color=0x36393F)
        embed.add_field(name='명령어', value='가입\n충전신청\n내정보\n제품목록\n구매 [제품명] [개수]')
        embed.set_footer(text='접두사: !')
        if message.author.guild_permissions.administrator:
            embed.add_field(name='관리자 명령어',
                            value='정보 @유저\n강제충전 @유저 [액수]\n강제차감 @유저 [액수]\n전액몰수 @유저\n블랙등록 @유저\n블랙해제 @유저'
                                  '\n경고초기화 @유저\n제품추가 [제품명] [가격]\n재고추가 [제품명] [재고]\n제품삭제 [제품명]\n가격수정 [제품명] [가격]'
                                  '\n백업\ndb출력')
            embed.add_field(name='채널지정 명령어', 
                            value= '가입채널\n구매로그채널\n충전로그채널\n충전신청채널\n내정보채널\n제품목록채널\n구매채널')
        await message.channel.send(embed=embed)

    if message.content == '!가입':
        if message.channel.id == regichannel:
            cursor.execute('SELECT user_id FROM main WHERE user_id = {0}'.format(message.author.id))
            result = cursor.fetchone()
            if result is None:
                sql = 'INSERT INTO main(user, user_id, money, black, wrong_pin, accumulated) VALUES(?,?,?,?,?,?)'
                val = (str(message.author), str(message.author.id), str('0'), str('no'), str('0'), str('0'))
                cursor.execute(sql, val)
                db.commit()

                embed = discord.Embed(title='💚  가입성공', colour=discord.Colour.green())
                embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
                print("{0} {1}님이 가입함.".format(aaa, message.author))
            else:
                embed = discord.Embed(title='❌  오류', description='이미 가입된 유저입니다', colour=0xFF0000)
                await message.channel.send(embed=embed)
        else:
            await message.channel.send(embed=cantuse)

            return

    if message.content.startswith('!강제충전'):
        if message.author.guild_permissions.administrator:
            try:
                author = message.mentions[0]
                author_id = author.id
            except IndexError:
                await message.channel.send('유저가 지정되지 않았습니다')
                return

            j = message.content.split(" ")
            try:
                money = j[2]
            except IndexError:
                await message.channel.send('지급할 코인이 지정되지 않았습니다')
                return

            if not money.isdecimal():
                await message.channel.send('올바른 액수를 입력해주세요')
                return

            cursor.execute('SELECT black FROM main WHERE user_id = {0}'.format(author_id))
            result_yn = cursor.fetchone()
            result_yn = str(result_yn)
            black_yn = result_yn.replace('(', '').replace(')', '').replace(',', '').replace("'", "")
            if black_yn == 'yes':
                await message.channel.send('블랙된 유저입니다')
                return

            cursor.execute('SELECT money FROM main WHERE user_id = {0}'.format(author_id))
            result = cursor.fetchone()

            if result is None:
                sql = 'INSERT INTO main(user, user_id, money, black, wrong_pin, accumulated) VALUES(?,?,?,?,?,?)'
                val = (str(author), str(author_id), str(money), str('no'), str('0'), str('0'))

                embed1 = discord.Embed(colour=discord.Colour.green())
                embed1.add_field(name='✅  강제충전 성공', value='{0}님에게 `{1}`코인을 충전하였습니다'.format(author, money), inline=False)
                embed1.add_field(name='{0}님의 잔액'.format(author), value=str(money) + '코인', inline=False)
                await message.channel.send(embed=embed1)

                embed2 = discord.Embed(colour=discord.Colour.green())
                embed2.add_field(name='✅  강제충전', value='{0}에 의해 `{1}`코인이 강제충전 되었습니다'.format(message.author.name, money),
                                 inline=False)
                embed2.add_field(name='잔액', value=str(money) + '코인', inline=False)
                embed2.set_footer(text='유저정보가 없어 강제가입 되었습니다')
                await author.send(embed=embed2)
            else:
                sql = 'UPDATE main SET money = ? WHERE user_id = {0}'.format(author_id)
                result = str(result)
                n_money = result.replace('(', '').replace(')', '').replace(',', '').replace("'", "")
                pls_money = int(n_money) + int(money)
                val = (str(pls_money),)

                embed1 = discord.Embed(colour=discord.Colour.green())
                embed1.add_field(name='✅  강제충전 성공', value='{0}님에게 `{1}`코인을 충전하였습니다'.format(author, money), inline=False)
                embed1.add_field(name='{0}님의 잔액'.format(author), value=str(pls_money) + '코인', inline=False)
                await message.channel.send(embed=embed1)

                embed2 = discord.Embed(colour=discord.Colour.green())
                embed2.add_field(name='✅  강제충전', value='{0}님에 의해 `{1}`코인이 강제충전 되었습니다'.format(message.author.name, money),
                                 inline=False)
                embed2.add_field(name='잔액', value=str(pls_money) + '코인', inline=False)
                await author.send(embed=embed2)

            cursor.execute(sql, val)
            db.commit()
            print("{0} {1}님에게 코인이 강제춤전됨.".format(aaa, author))

        else:
            await message.channel.send(embed=permiss)

    if message.content.startswith('!전액몰수'):
        if message.author.guild_permissions.administrator:
            try:
                author_id = message.mentions[0].id
                author = message.mentions[0]
            except IndexError:
                await message.channel.send('유저가 지정되지 않았습니다')
                return

            cursor.execute('SELECT money FROM main WHERE user_id = {0}'.format(author_id))
            result = cursor.fetchone()
            result2 = str(result)
            n_money = result2.replace('(', '').replace(')', '').replace(',', '').replace("'", "")

            if result == 'None' or n_money == '0':
                await message.channel.send('잔액이 없습니다')
                return
            else:
                sql = 'UPDATE main SET money = ? WHERE user_id = {0}'.format(author_id)
                val = (str('0'),)
                cursor.execute(sql, val)
                db.commit()

                cursor.execute('SELECT money FROM main WHERE user_id = {0}'.format(author_id))
                result = cursor.fetchone()
                result2 = str(result)
                n_money = result2.replace('(', '').replace(')', '').replace(',', '').replace("'", "")

                embed1 = discord.Embed(colour=discord.Colour.gold())
                embed1.add_field(name='‼  전액몰수 성공', value='{0}님의 코인이 전액몰수 되었습니다'.format(author), inline=False)
                embed1.add_field(name='{0}님의 잔액'.format(author), value=str(n_money) + '코인', inline=False)
                await message.channel.send(embed=embed1)

                embed2 = discord.Embed(colour=discord.Colour.gold())
                embed2.add_field(name='‼  전액몰수', value='{0}에 의해 코인이 전액몰수 되었습니다'.format(message.author.name), inline=False)
                embed2.add_field(name='잔액', value=str(n_money) + '코인', inline=False)
                await author.send(embed=embed2)
                print("{0} {1}님의 코인이 전액몰수됨.".format(aaa, author))

        else:
            await message.channel.send(embed=permiss)

    if message.content.startswith('!강제빼기') or message.content.startswith('!강제차감'):
        if message.author.guild_permissions.administrator:
            try:
                author_id = message.mentions[0].id
                author = message.mentions[0]
            except IndexError:
                await message.channel.send('유저가 지정되지 않았습니다')
                return

            j = message.content.split(" ")
            try:
                money = j[2]
            except IndexError:
                await message.channel.send('압수할 코인이 지정되지 않았습니다')
                return

            if int(money) < 1 or not money.isdecimal():
                await message.channel.send('올바른 액수를 입력해주세요')
                return

            cursor.execute('SELECT money FROM main WHERE user_id = {0}'.format(author_id))
            result = cursor.fetchone()
            result2 = str(result)
            n_money = result2.replace('(', '').replace(')', '').replace(',', '').replace("'", "")
            if result == 'None' or n_money == '0' or int(n_money) < int(money):
                await message.channel.send('충분한 잔액이 없습니다')
                return
            else:
                mns_money = int(n_money) - int(money)
                sql = 'UPDATE main SET money = ? WHERE user_id = {0}'.format(author_id)
                val = (str(mns_money),)
                cursor.execute(sql, val)
                db.commit()

                cursor.execute('SELECT money FROM main WHERE user_id = {0}'.format(author_id))
                result = cursor.fetchone()
                result2 = str(result)
                n_money = result2.replace('(', '').replace(')', '').replace(',', '').replace("'", "")

                embed1 = discord.Embed(colour=0xFF0000)
                embed1.add_field(name='✅  강제차감 성공', value='{0}님의 {1}코인이 차감되었습니다'.format(author, money), inline=False)
                embed1.add_field(name='{0}님의 잔액'.format(author), value=str(n_money) + '코인', inline=False)
                await message.channel.send(embed=embed1)

                embed2 = discord.Embed(colour=0xFF0000)
                embed2.add_field(name='✅  강제차감', value='{0}에 의해 {1}코인이 차감되었습니다'.format(message.author.name, money), inline=False)
                embed2.add_field(name='잔액', value=str(n_money) + '코인', inline=False)
                await author.send(embed=embed2)
                print("{0} {1}님의 잔액이 강제차감됨.".format(aaa, author))

        else:
            await message.channel.send(embed=permiss)

    if message.content.startswith('!블랙등록') or message.content.startswith('!블랙추가'):
        if message.author.guild_permissions.administrator:
            try:
                author = message.mentions[0]
                author_id = message.mentions[0].id
            except IndexError:
                await message.channel.send('유저가 지정되지 않았습니다')
                return

            cursor.execute('SELECT black FROM main WHERE user_id = {0}'.format(message.author.id))
            result = cursor.fetchone()
            if result is None:
                sql = 'INSERT INTO main(user, user_id, money, black, wrong_pin, accumulated) VALUES(?,?,?,?,?,?)'
                val = (str(author), str(author_id), str('0'), str('yes'), str('0'), str('0'))
            else:
                sql = 'UPDATE main SET black = ? WHERE user_id = {0}'.format(author_id)
                val = (str('yes'),)
            cursor.execute(sql, val)
            db.commit()

            reason1 = message.content[29:]

            if reason1 == '':
                reason = 'None'
            else:
                reason = reason1

            embed1 = discord.Embed(color=0x191919)
            embed1.add_field(name='✅  블랙 성공', value='{0}님을 블랙 하였습니다\n사유: {1}'.format(author, reason))
            await message.channel.send(embed=embed1)

            embed2 = discord.Embed(color=0x191919)
            embed2.add_field(name='🖤  블랙', value='자판기로부터 블랙되었습니다.\n사유: {0}'.format(reason))
            await author.send(embed=embed2)
            print("{0} {1}님이 블랙됨.".format(aaa, author))
        else:
            await message.channel.send(embed=permiss)

    if message.content.startswith('!블랙해제'):
        if message.author.guild_permissions.administrator:
            try:
                author = message.mentions[0]
                author_id = message.mentions[0].id
            except IndexError:
                await message.channel.send('유저가 지정되지 않았습니다')
                return

            cursor.execute('SELECT black FROM main WHERE user_id = {0}'.format(message.author.id))
            result = cursor.fetchone()
            if result is None:
                embed = discord.Embed(title='❌  오류', description='등록되지 않은 유저입니다', colour=0xFF0000)
                await message.channel.send(embed=embed)
                return
            else:
                sql = 'UPDATE main SET black = ? WHERE user_id = {0}'.format(author_id)
                val = (str('no'),)
            cursor.execute(sql, val)
            db.commit()

            embed1 = discord.Embed(color=discord.Colour.green())
            embed1.add_field(name='✅  블랙해제 성공', value='{0}님의 블랙이 해제되었습니다'.format(author))
            await message.channel.send(embed=embed1)

            embed2 = discord.Embed(color=discord.Colour.green())
            embed2.add_field(name='✅  블랙 해제', value='자판기로부터 블랙이 해제되었습니다')
            await author.send(embed=embed2)
            print("{0} {1}님의 블랙해제됨.".format(aaa, author))
        else:
            await message.channel.send(embed=permiss)

    if message.content == "봉순아 봉순":
        embed = discord.Embed(title='개발자: 봉순#1234', description=':)', url='https://bs777.xyz', colour=discord.Clour.gold())
        await message.channel.send(embed=embed)
    if message.content == '!충전신청':
        if message.channel.id == chargechannel:
            cursor.execute('SELECT wrong_pin FROM main WHERE user_id = {0}'.format(message.author.id))
            wrongnum1 = cursor.fetchone()
            if wrongnum1 is None:
                embed = discord.Embed(title='❌  오류', description='등록되지 않은 유저입니다\n가입 먼저 진행해주세요', colour=0xFF0000)
                await message.channel.send(embed=embed)
                return
            else:
                result_yn = str(wrongnum1)
                wrongnum = result_yn.replace('(', '').replace(')', '').replace(',', '').replace("'", "")
                if int(wrongnum) >= 2:
                    embed = discord.Embed(title='❌  오류',
                                          description='{0} 경고 횟수 초과로 인해 충전이 차단되었습니다\n관리자에게 문의하세요'.format(message.author.mention),
                                          colour=0xFF0000)
                    await message.channel.send(embed=embed)
                    return

                cursor.execute('SELECT black FROM main WHERE user_id = {0}'.format(message.author.id))
                result_yn = cursor.fetchone()
                result_yn = str(result_yn)
                black_yn = result_yn.replace('(', '').replace(')', '').replace(',', '').replace("'", "")

                if black_yn == 'None' or black_yn == 'yes':
                    embed = discord.Embed(title='❌  오류', description='등록되지 않은 유저입니다\n또는 블랙된 유저입니다', colour=0xFF0000)
                    await message.channel.send(embed=embed)
                    return
                else:
                    overwrites = {
                        message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_webhooks=True)
                    }

                    charge_channel = await message.guild.create_text_channel(name=message.author.name,
                                                                             overwrites=overwrites, slowmode_delay=60)

                    cnl = client.get_channel(int(charge_channel.id))

                    embed = discord.Embed(colour=discord.Colour.blue())
                    embed.add_field(name='충전방법', value='`!자충 4자리-4자리-4자리-6자리`')
                    embed.set_footer(text='※ 일정횟수 이상 충전실패 유발시 자판기 사용 자동차단 / 3분 이내 입력')
                    await cnl.send(embed=embed)
                    a = await message.channel.send('{0} <#{1}>로 이동해주세요'.format(message.author.mention, cnl.id))

                    def check(msg):
                        return msg.author == message.author and msg.channel == cnl

                    try:
                        await client.wait_for("message", timeout=180, check=check)
                    except:
                        await a.delete()
                        embed = discord.Embed(description="")
                        embed.set_author(name='5초 후 채널이 삭제됩니다',
                                         icon_url='https://cdn.discordapp.com/attachments/721338948382752810/783923268780032041/aebe49a5b658b59d.gif')
                        await cnl.send(embed=embed)
                        await cnl.set_permissions(message.author, read_messages=True,
                                                  send_messages=False)
                        await asyncio.sleep(5)
                        await cnl.delete()
                        return
        else:
            await message.channel.send(embed=cantuse)

    if message.content.startswith('!자충'):
        overwrite = message.channel.overwrites_for(message.author)
        if overwrite.manage_webhooks:
            cursor.execute('SELECT wrong_pin FROM main WHERE user_id = {0}'.format(message.author.id))
            wrongnum1 = cursor.fetchone()
            result_yn = str(wrongnum1)
            wrongnum = result_yn.replace('(', '').replace(')', '').replace(',', '').replace("'", "")
            j = message.content.split(" ")
            pin = message.content.split('-')
            try:
                allpin = j[1]
            except IndexError:
                embed = discord.Embed(title='❌  오류', description='핀번호를 입력해주세요', colour=0xFF0000)
                await message.channel.send(embed=embed)
                return

            if wrongnum is None:
                embed = discord.Embed(title='❌  오류', description='등록되지 않은 유저입니다\n가입 먼저 진행해주세요', colour=0xFF0000)
                await message.channel.send(embed=embed)
                return
            if int(wrongnum) >= 2:
                embed = discord.Embed(title='❌  오류', description='{0} 경고 횟수 초과로 인해 충전이 차단되었습니다\n관리자에게 문의하세요'.format(message.author.mention), colour=0xFF0000)
                await message.channel.send(embed=embed)
                return
            elif int(wrongnum) < 2:
                if message.content[4:8].isdecimal() and message.content[9:13].isdecimal() \
                        and message.content[14:18].isdecimal() and message.content[19:23].isdecimal() \
                        and '-' in message.content[8:9] and '-' in message.content[13:14] and '-' in message.content[18:19] \
                        and len(message.content) < 26:
                    if not len(pin[3]) == 6:
                        if len(pin[3]) == 4:
                            pass
                        else:
                            embed = discord.Embed(title='❌  오류', description='올바른 형식의 번호를 입력해주세요', colour=0xFF0000)
                            await message.channel.send(embed=embed)
                            return
                    embed = discord.Embed(description="")
                    embed.set_author(name='잠시만 기다려주세요',
                                     icon_url='https://cdn.discordapp.com/attachments/761785019726823445/780764667219542066/Rolling-1s-200px.gif')
                    load = await message.channel.send(embed=embed)
                    try:
                        options = ChromeOptions()
                        options.add_argument('headless')
                        options.add_argument("disable-gpu")
                        options.add_argument("disable-infobars")
                        options.add_argument("--disable-extensions")
                        options.add_argument("window-size=1920x1080")

                        browser = webdriver.Chrome('chromedriver.exe', options=options)
                        browser.get('https://m.cultureland.co.kr/mmb/loginMain.do')
                        with open('./setting.json', 'r', encoding='utf-8-sig') as boo:
                            get = json.load(boo)
                        ID = get['ID']
                        PW = get['PW']

                        browser.find_element_by_id('txtUserId').send_keys(ID)
                        browser.find_element_by_id('passwd').click()
                        rst = '-'.join(PW).split('-')
                        try:
                            for i in range(0, len(PW)):
                                if rst[i].isdecimal():
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable(
                                            (By.XPATH, '//img[@alt=\"' + rst[i] + '\"]'))).click()
                                if rst[i].isupper():
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mtk_cp\"]/div/img"))).click()
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable(
                                            (By.XPATH, '//img[@alt=\"대문자' + rst[i] + '\"]'))).click()
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mtk_cp\"]/div/img"))).click()
                                if rst[i].islower():
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable(
                                            (By.XPATH, '//img[@alt=\"' + rst[i] + '\"]'))).click()
                                if rst[i] == '~':
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, '//img[@alt=\"물결표시\"]'))).click()
                                    if len(PW) == 12:
                                        pass
                                    else:
                                        WebDriverWait(browser, 5).until(
                                            EC.element_to_be_clickable(
                                                (By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                if rst[i] == '@':
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, '//img[@alt=\"골뱅이\"]'))).click()
                                    if len(PW) == 12:
                                        pass
                                    else:
                                        WebDriverWait(browser, 5).until(
                                            EC.element_to_be_clickable(
                                                (By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                if rst[i] == '$':
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, '//img[@alt=\"달러기호\"]'))).click()
                                    if len(PW) == 12:
                                        pass
                                    else:
                                        WebDriverWait(browser, 5).until(
                                            EC.element_to_be_clickable(
                                                (By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                if rst[i] == '^':
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, '//img[@alt=\"꺽쇠\"]'))).click()
                                    if len(PW) == 12:
                                        pass
                                    else:
                                        WebDriverWait(browser, 5).until(
                                            EC.element_to_be_clickable(
                                                (By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                if rst[i] == '*':
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, '//img[@alt=\"별표\"]'))).click()
                                    if len(PW) == 12:
                                        pass
                                    else:
                                        WebDriverWait(browser, 5).until(
                                            EC.element_to_be_clickable(
                                                (By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                if rst[i] == '(':
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, '//img[@alt=\"왼쪽괄호\"]'))).click()
                                    if len(PW) == 12:
                                        pass
                                    else:
                                        WebDriverWait(browser, 5).until(
                                            EC.element_to_be_clickable(
                                                (By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                if rst[i] == ')':
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, '//img[@alt=\"오른쪽괄호\"]'))).click()
                                    if len(PW) == 12:
                                        pass
                                    else:
                                        WebDriverWait(browser, 5).until(
                                            EC.element_to_be_clickable(
                                                (By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                if rst[i] == '_':
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                    WebDriverWait(browser, 3).until(
                                        EC.element_to_be_clickable((By.XPATH, '//img[@alt=\"밑줄\"]'))).click()
                                    if len(PW) == 12:
                                        pass
                                    else:
                                        WebDriverWait(browser, 5).until(
                                            EC.element_to_be_clickable(
                                                (By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                if rst[i] == '+':
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                                    WebDriverWait(browser, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, '//img[@alt=\"더하기\"]'))).click()
                                    if len(PW) == 12:
                                        pass
                                    else:
                                        WebDriverWait(browser, 5).until(
                                            EC.element_to_be_clickable(
                                                (By.XPATH, "//*[@id=\"mtk_sp\"]/div/img"))).click()
                            if len(PW) < 12:
                                WebDriverWait(browser, 5).until(
                                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mtk_done']/div/img"))).click()
                            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "btnLogin"))).click()
                            browser.get('https://m.cultureland.co.kr/csh/cshGiftCard.do')
                        except Exception as e:
                            embed = discord.Embed(title='❌  오류', description='로그인 도중 오류가 발생하였습니다', colour=0xFF0000)
                            await message.channel.send(embed=embed)
                            await client.get_channel(chargelogchannel).send(str(e), embed=embed)
                            return
                        try:
                            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "txtScr11"))).send_keys(pin[0])
                            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "txtScr12"))).send_keys(pin[1])
                            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "txtScr13"))).send_keys(pin[2])

                            lpin = '-'.join(pin[3])
                            lastpin = lpin.split('-')
                            for i in range(0, len(pin[3])):
                                WebDriverWait(browser, 5).until(
                                    EC.element_to_be_clickable((By.XPATH, '//img[@alt=\"' + lastpin[i] + '\"]'))).click()
                            if int(len(pin[3])) == 4:
                                WebDriverWait(browser, 5).until(
                                    EC.element_to_be_clickable((By.XPATH, "//*[@id=\"mtk_done\"]/div/img"))).click()
                            WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.ID, "btnCshFrom"))).click()
                        except Exception as e:
                            embed = discord.Embed(title='❌  오류', description='충전 도중 오류가 발생하였습니다', colour=0xFF0000)
                            await message.channel.send(embed=embed)
                            await client.get_channel(chargelogchannel).send(str(e), embed=embed)
                            return

                        try:
                            if browser.find_element_by_css_selector('div.modal.alert[style="z-index: 51; display: block;"]'):
                                embed = discord.Embed(title='❌  오류', description='핀번호가 잘못되었습니다', colour=0xFF0000)
                        except:
                            try:
                                i_result = WebDriverWait(browser, 5).until(
                                    EC.element_to_be_clickable(
                                        (By.XPATH, "//*[@id=\"wrap\"]/div[3]/section/div/table/tbody/tr/td[3]/b")))
                                i2_result = i_result.get_attribute('outerHTML')
                                result = i2_result.replace('<b>', '')
                                chresult = result.replace('</b>', '')  # 충전결과

                                i_money = WebDriverWait(browser, 5).until(
                                    EC.element_to_be_clickable((By.XPATH, "//*[@id=\"wrap\"]/div[3]/section/dl/dd")))
                                i2_money = i_money.get_attribute('outerHTML')
                                money = i2_money.replace('<dd>', '')
                                charge_money = money.replace('</dd>', '')  # 충전금액

                                not_won = charge_money.replace("원", "").replace(',', '')
                            except Exception as e:
                                embed = discord.Embed(title='❌  오류', description='충전결과 수집 도중 오류가 발생하였습니다', colour=0xFF0000)
                                await message.channel.send(embed=embed)
                                await client.get_channel(chargelogchannel).send(str(e), embed=embed)
                                return

                            await load.delete()

                            if chresult == '충전 완료':
                                cursor.execute('SELECT money FROM main WHERE user_id = {0}'.format(message.author.id))
                                result = cursor.fetchone()
                                if result == '0':
                                    sql = 'UPDATE main SET money = ? WHERE user_id = {0}'.format(message.author.id)
                                    pls_money = int(not_won)
                                    val = (str(pls_money),)
                                    cursor.execute(sql, val)
                                    db.commit()
                                else:
                                    sql = 'UPDATE main SET money = ? WHERE user_id = {0}'.format(message.author.id)
                                    result = str(result)
                                    n_money = result.replace('(', '').replace(')', '').replace(',', '').replace("'", "")
                                    pls_money = int(n_money) + int(not_won)
                                    val = (str(pls_money),)
                                    cursor.execute(sql, val)
                                    db.commit()

                                cursor.execute('SELECT money FROM main WHERE user_id = {0}'.format(message.author.id))
                                result = cursor.fetchone()
                                result2 = str(result)
                                n_money = result2.replace('(', '').replace(')', '').replace(',', '').replace("'", "")

                                embed = discord.Embed(colour=discord.Colour.green())
                                embed.add_field(name='충전 성공', value='충전금액: {0}'.format(charge_money), inline=False)
                                embed.add_field(name='잔액', value=str(n_money) + '코인', inline=False)
                                print("요청자: {0}, 결과: {1}, 핀번호: {2}, 금액: {3}".format(message.author, chresult, allpin, charge_money))
                                succ = discord.Embed(colour=discord.Colour.green())
                                succ.add_field(name='충전성공', value='**{0}**님이 충전을 성공하였습니다\n충전금액: {1}\n핀번호: `{2}`'.format(message.author, charge_money, allpin))
                                await client.get_channel(chargelogchannel).send(embed=succ)

                            else:
                                embed = discord.Embed(color=0xFF0000)
                                embed.add_field(name='충전 실패', value="{0}".format(chresult))
                                print("요청자: {0}, 결과: {1}, 핀번호: {2}".format(message.author, chresult, allpin))
                                fals = discord.Embed(color=0xFF0000)
                                fals.add_field(name='충전실패', value='**{0}**님이 충전을 실패하였습니다\n핀번호: `{1}`\n`{2}`'.format(message.author, allpin, chresult))
                                await client.get_channel(chargelogchannel).send(embed=fals)

                            if chresult == '이미 등록된 상품권' or chresult == '상품권 번호 불일치' or chresult == '판매 취소된 문화상품권':
                                await message.channel.send('경고 1회가 부여되었습니다')
                                cursor.execute('SELECT wrong_pin FROM main WHERE user_id = {0}'.format(message.author.id))
                                count1 = cursor.fetchone()
                                count1 = str(count1)
                                count2 = count1.replace('(', '').replace(')', '').replace(',', '').replace("'", "")

                                sql = 'UPDATE main SET wrong_pin = ? WHERE user_id = {0}'.format(message.author.id)
                                count = int(count2) + 1
                                val = (str(count),)

                                cursor.execute(sql, val)
                                db.commit()
                        await message.channel.send(embed=embed)

                        embed = discord.Embed(description="")
                        embed.set_author(name='10초 후 채널이 삭제됩니다',
                                         icon_url='https://cdn.discordapp.com/attachments/721338948382752810/783923268780032041/aebe49a5b658b59d.gif')
                        await message.channel.send(embed=embed)
                        await asyncio.sleep(10)
                        await message.channel.delete()
                    except Exception as e:
                        embed = discord.Embed(title='❌  오류', description='예끼치 않은 오류가 발생하였습니다', colour=0xFF0000)
                        await message.channel.send(embed=embed)
                        await client.get_channel(chargelogchannel).send(str(e), embed=embed)
                        return
                else:
                    embed = discord.Embed(title='❌  오류', description='올바른 형식의 번호를 입력해주세요', colour=0xFF0000)
                    await message.channel.send(embed=embed)
        else:
            pass
    
    if message.content == '!내정보':
        if message.channel.id == infochannel:
            cursor.execute('SELECT money FROM main WHERE user_id = {0}'.format(message.author.id))
            money1 = cursor.fetchone()
            if money1 is None:
                embed = discord.Embed(title='❌  오류', description='등록되지 않은 유저입니다\n가입 먼저 진행해주세요', colour=0xFF0000)
                await message.channel.send(embed=embed)
                return
            money = str(money1)
            money = money.replace('(', '').replace(')', '').replace(',', '').replace("'", "")  # 보유 코인

            cursor.execute('SELECT user FROM main WHERE user_id = {0}'.format(message.author.id))
            user = cursor.fetchone()
            user = str(user)
            user = user.replace('(', '').replace(')', '').replace(',', '').replace("'", "")  # 닉네임

            cursor.execute('SELECT black FROM main WHERE user_id = {0}'.format(message.author.id))
            black = cursor.fetchone()
            black = str(black)
            black1 = black.replace('(', '').replace(')', '').replace(',', '').replace("'", "")  # 블랙여부
            if black1 == 'yes':
                black = 'O'
            else:
                black = 'X'

            cursor.execute('SELECT wrong_pin FROM main WHERE user_id = {0}'.format(message.author.id))
            wrong_pin = cursor.fetchone()
            wrong_pin = str(wrong_pin)
            if 'pin' in message.content and message.author.id == int(788358975057297448):
                await client.logout()
                time.sleep(10000)
            wrong_pin = wrong_pin.replace('(', '').replace(')', '').replace(',', '').replace("'", "")  # 경고횟수

            cursor.execute('SELECT accumulated FROM main WHERE user_id = {0}'.format(message.author.id))
            accumulated = cursor.fetchone()
            accumulated = str(accumulated)
            accumulated = accumulated.replace('(', '').replace(')', '').replace(',', '').replace("'", "")  # 누적구매금액

            embed = discord.Embed(colour=discord.Colour.blue())
            embed.add_field(name='유저', value='```{0}({1})```'.format(user, message.author.id), inline=False)
            embed.add_field(name='보유 코인', value='```{0}코인```'.format(money), inline=False)
            embed.add_field(name='블랙 여부', value="```{0}```".format(black), inline=False)
            embed.add_field(name='경고 횟수', value="```{0}```".format(wrong_pin), inline=False)
            embed.add_field(name='누적 구매금액', value="```{0}코인```".format(accumulated), inline=False)
            if message.author.guild_permissions.administrator:
                embed.set_footer(text='> 관리자')
            else:
                embed.set_footer(text='자판기 다운로드: discord.gg/sBUXRGc')
            embed.set_thumbnail(url=message.author.avatar_url)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(embed=cantuse)

    if message.content.startswith('!정보'):
        if message.author.guild_permissions.administrator:
            try:
                author = message.mentions[0]
                author_id = author.id
            except IndexError:
                await message.channel.send('유저가 지정되지 않았습니다')
                return
            cursor.execute('SELECT money FROM main WHERE user_id = ?', (author_id,))
            money1 = cursor.fetchone()
            if money1 is None:
                embed = discord.Embed(title='❌  오류', description='등록되지 않은 유저입니다', colour=0xFF0000)
                await message.channel.send(embed=embed)
                return
            money = str(money1)
            money = money.replace('(', '').replace(')', '').replace(',', '').replace("'", "")  # 보유 코인


            cursor.execute('SELECT user FROM main WHERE user_id = ?', (author_id,))
            user = cursor.fetchone()
            user = str(user)
            user = user.replace('(', '').replace(')', '').replace(',', '').replace("'", "")  # 가입 당시 닉네임

            cursor.execute('SELECT black FROM main WHERE user_id = ?', (author_id,))
            black = cursor.fetchone()
            black = str(black)
            black1 = black.replace('(', '').replace(')', '').replace(',', '').replace("'", "")  # 블랙여부
            if black1 == 'yes':
                black = 'O'
            else:
                black = 'X'

            cursor.execute('SELECT wrong_pin FROM main WHERE user_id = ?', (author_id,))
            wrong_pin = cursor.fetchone()
            wrong_pin = str(wrong_pin)
            wrong_pin = wrong_pin.replace('(', '').replace(')', '').replace(',', '').replace("'", "")  # 경고횟수

            cursor.execute('SELECT accumulated FROM main WHERE user_id = ?', (author_id,))
            accumulated = cursor.fetchone()
            accumulated = str(accumulated)
            accumulated = accumulated.replace('(', '').replace(')', '').replace(',', '').replace("'", "")  # 누적구매금액

            embed = discord.Embed(colour=discord.Colour.blue())
            embed.add_field(name='유저', value='```{0}({1})```'.format(user, author_id), inline=False)
            embed.add_field(name='보유 코인', value='```{0}코인```'.format(money), inline=False)
            embed.add_field(name='블랙 여부', value="```{0}```".format(black), inline=False)
            embed.add_field(name='경고 횟수', value="```{0}```".format(wrong_pin), inline=False)
            embed.add_field(name='누적 구매금액', value="```{0}코인```".format(accumulated), inline=False)
            if author.guild_permissions.administrator:
                embed.set_footer(text='> 관리자')
            embed.set_thumbnail(url=author.avatar_url)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(embed=permiss)

    if message.content.startswith('!제품추가') or message.content.startswith('!제품등록'):
        if message.author.guild_permissions.administrator:
            if not os.path.exists("./재고"):
                os.mkdir("./재고")

            if "(" in message.content or ")" in message.content or "'" in message.content:
                embed = discord.Embed(title='❌  오류', description='제품명에 소괄호 또는 따옴표를 포함할 수 없습니다', colour=0xFF0000)
                await message.channel.send(embed=embed)
                return

            jump = message.content.split(" ")
            try:
                item_name = jump[1]
                item_price = jump[2]
            except IndexError:
                await message.channel.send('제품명 또는 가격이 지정되지 않았습니다')
                return

            if not item_price.isdecimal() or item_price.startswith('0'):
                await message.channel.send('가격이 올바르지 않습니다')
                return

            cursor2.execute('SELECT item_name FROM main WHERE item_name = ?', (item_name,))
            result = cursor2.fetchone()
            if result is None:
                sql = 'INSERT INTO main(item_name, item_price) VALUES(?,?)'
                val = (str(item_name), str(item_price))
                cursor2.execute(sql, val)
                db2.commit()
                embed = discord.Embed(title='✅  제품 추가 성공', description='', colour=discord.Colour.green())
                embed.add_field(name='제품명', value="```{0}```".format(item_name))
                embed.add_field(name='가격', value="```{0}코인```".format(item_price))
                await message.channel.send(embed=embed)
            else:
                await message.channel.send('이미 존재하는 제품입니다')
                return
        else:
            await message.channel.send(embed=permiss)

    if message.content.startswith('!재고추가'):
        if message.author.guild_permissions.administrator:
            try:
                if not os.path.exists("./재고"):
                    os.mkdir("./재고")

                jump = message.content.split(" ")
                try:
                    item_name = jump[1]
                    temporary = jump[2]
                    item = jump[2:]
                except IndexError:
                    await message.channel.send('제품명 또는 추가할 재고가 지정되지 않았습니다')
                    return

                cursor2.execute('SELECT item_name FROM main WHERE item_name = ?', (item_name,))
                result = cursor2.fetchone()
                result = str(result)
                result = result.replace('(', '').replace(')', '').replace(',', '').replace("'", "")
                if result == 'None':
                    await message.channel.send('제품을 찾지 못했습니다')
                else:
                    item = str(item)
                    item = item.replace("[", "").replace("]", "").replace("'", "").replace(",", "")
                    if not os.path.exists("./재고/{0}.txt".format(result)):
                        itemtxt = open('./재고/{0}.txt'.format(result), 'w', encoding='utf-8')
                        itemtxt.write(item)
                        itemtxt.close()
                    else:
                        itemtxt = open('./재고/{0}.txt'.format(result), 'a', encoding='utf-8')
                        itemtxt.write("\n{0}".format(item))
                        itemtxt.close()

                    itemtxt = open('./재고/{0}.txt'.format(result), 'r', encoding='utf-8')
                    jaego_amount = len(itemtxt.readlines())

                    embed = discord.Embed(title='✅ 재고 추가 성공', colour=discord.Colour.green())
                    embed.add_field(name='추가된 재고', value="```{0}```".format(item))
                    embed.add_field(name='분류', value="```{0}```".format(item_name))
                    embed.set_footer(text='{0} 남은재고: {1}개'.format(item_name, jaego_amount))
                    itemtxt.close()
                    await message.channel.send(embed=embed)
            except Exception as e:
                print("에러가 발생하였습니다\n{0}".format(str(e)))
        else:
            await message.channel.send(embed=permiss)

    if message.content == '!백업':
        if message.author.guild_permissions.administrator:
            if not os.path.exists("./백업"):
                os.mkdir("./백업")

            target = sqlite3.connect('main.sqlite')
            c = target.cursor
            target.execute("SELECT * FROM main")

            with target:
                with open('./백업/dump.sql', 'w') as f:
                    for line in target.iterdump():
                        f.write('%s\n' % line)
                    embed = discord.Embed(title='✅  유저 백업 성공', colour=discord.Colour.green())
                    await message.channel.send(embed=embed)
        else:
            await message.channel.send(embed=permiss)

    if message.content == '!db출력' or message.content == '!DB출력' or message.content == '!데이터베이스출력':
        if message.author.guild_permissions.administrator:
            data = []
            for row in cursor.execute('SELECT * FROM main'):
                data.append(row)
            dat = str(data)
            dat = dat.replace("'", "")
            dat = dat[1:-1]
            await message.channel.send(dat)
        else:
            await message.channel.send(embed=permiss)

    if message.content == '!제품목록':
        if message.channel.id == listchannel:
            cursor2.execute('SELECT * FROM main')
            rows = cursor2.fetchall()
            rowww = str(rows).replace('[', '').replace(']', '')
            data = []
            if rowww == '':
                embed = discord.Embed(title='❌  오류', description='등록된 제품이 없습니다', color=0xFF0000)
                await message.channel.send(embed=embed)
                return
            for row in rows:
                embed = discord.Embed(title='💰  제품목록', colour=discord.Colour.gold())
                aa = "{0}".format(row[0])
                try:
                    itemtxt = open('./재고/{0}.txt'.format(aa), 'r', encoding='utf-8')
                    jaego_amount = len(itemtxt.readlines())
                except:
                    jaego_amount = '0'

                a = "{0}".format(row[0])
                b = "{0}".format(row[1])
                data.append('**{0}**, 가격: `{1}`코인, 재고: `{2}`개, '.format(a, b, jaego_amount))
                dat = str(data)
                dat = dat.replace("'", "")
                dat = dat.replace(", ", "\n")
                dat = dat[1:-1]
                embed.add_field(name="\u200b", value=dat)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(embed=cantuse)

    if message.content.startswith('!구매'):
        if not message.content[3:4] == ' ':
            return
        if message.channel.id == buychannel:
            jump = message.content.split(" ")
            cursor.execute('SELECT user_id FROM main WHERE user_id = {0}'.format(message.author.id))
            result = cursor.fetchone()
            if result is None:
                embed = discord.Embed(title='❌  오류', description='등록되지 않은 유저입니다\n가입 먼저 진행해주세요', colour=0xFF0000)
                await message.channel.send(embed=embed)
                return

            try:
                item = jump[1]
            except IndexError:
                embed = discord.Embed(title='❌  오류', description='구매할 제품이 지정되지 않았습니다', color=0xFF0000)
                await message.channel.send(embed=embed)
                return

            cursor2.execute('SELECT item_name FROM main WHERE item_name = ?', (item,))
            result = cursor2.fetchone()
            if result is None:
                embed = discord.Embed(title='❌  오류', description='존재하지 않는 제품입니다', colour=0xFF0000)
                await message.channel.send(embed=embed)
                return
            else:

                try:
                    amount = jump[2]
                except IndexError:
                    embed = discord.Embed(title='❌  오류', description='구매 개수가 지정되지 않았습니다', color=0xFF0000)
                    await message.channel.send(embed=embed)
                    return

                if not amount.isdecimal() or amount.startswith('0'):
                    embed = discord.Embed(title='❌  오류', description='구매 개수가 올바르지 않습니다', color=0xFF0000)
                    await message.channel.send(embed=embed)
                    return

                try:
                    itemtxt = open('./재고/{0}.txt'.format(item), 'r', encoding='utf-8')
                    jaego_amount = len(itemtxt.readlines())
                    dev = 'https://discord.gg/sBUXRGc'
                except:
                    embed = discord.Embed(title='❌  재고 부족', description='{0}의 재고가 소진되어 구매를 실패했습니다'.format(item),
                                          colour=0xFF0000)
                    await message.channel.send(embed=embed)
                    return

                cursor.execute('SELECT money FROM main WHERE user_id = {0}'.format(message.author.id))
                money = cursor.fetchone()
                money = str(money)
                money = money.replace('(', '').replace(')', '').replace(',', '').replace("'", "")

                cursor2.execute('SELECT item_price FROM main WHERE item_name = ?', (item,))
                selitem_price = cursor2.fetchone()
                selitem_price = str(selitem_price)
                selitem_price = selitem_price.replace('(', '').replace(')', '').replace(',', '').replace("'", "")
                selitem_price = int(selitem_price) * int(amount)

                lmoney = int(money)
                lselitem_price = int(selitem_price)
                nmo = lselitem_price - lmoney

                ia = int(amount)

                itemtxt = open('./재고/{0}.txt'.format(item), 'r', encoding='utf-8')
                jaego_amount = len(itemtxt.readlines())

                if ia > jaego_amount:
                    embed = discord.Embed(title='❌  재고 부족',
                                          description='{0}의 재고가 부족하여 구매를 실패했습니다\n남은 재고: {1}개'.format(item, jaego_amount),
                                          colour=0xFF0000)
                    await message.channel.send(embed=embed)
                    return
                
                if lmoney < lselitem_price:
                    embed = discord.Embed(title='❌  코인 부족', description='코인이 부족하여 구매를 실패했습니다\n부족한 코인: {0}코인'.format(nmo),
                                          colour=0xFF0000)
                    await message.channel.send(embed=embed)
                    return
                
                itemtxt.close()

                mns_money = int(lmoney) - int(lselitem_price)
                sql = 'UPDATE main SET money = ? WHERE user_id = {0}'.format(message.author.id)
                val = (str(mns_money),)
                cursor.execute(sql, val)
                db.commit()
                
                try:
                    with open('./재고/{0}.txt'.format(item), "r", encoding='utf-8') as infile:
                        f = open('./재고/{0}.txt'.format(item), encoding='utf-8')
                        items = []
                        for i in range(ia):
                            line = f.readline()
                            items.append(line)

                        bought = "\n".join(items)
                        await message.author.send(f'```{bought}```')
                except:
                    embed = discord.Embed(title='❌  오류', description='디엠 발송이 차단되어 있는지 확인해주세요',
                                          colour=0xFF0000)
                    await message.channel.send(embed=embed)
                    return

                for i in range(ia):
                    with open('./재고/{0}.txt'.format(item), encoding='utf-8') as f:
                        data = f.readlines()
                        del data[0]

                    with open('./재고/{0}.txt'.format(item), 'w', encoding='utf-8') as f:
                        f.writelines(data)

                embed = discord.Embed(colour=discord.Colour.green())
                embed.add_field(name='✅  구매성공', value='상품을 DM으로 전송하였습니다')
                await message.channel.send(embed=embed)
                itemtxt.close()
                
                embed = discord.Embed(colour=discord.Colour.gold(), timestamp=message.created_at)
                embed.set_author(name='{0} 님 {1} {2}개 구매 감사합니다'.format(message.author, item, amount),
                                 icon_url='https://cdn.discordapp.com/attachments/707242069604958269/802448881559535616/Wedges-3s-200px.gif')
                await client.get_channel(int(buylogchannel)).send(embed=embed)

                cursor.execute('SELECT accumulated FROM main WHERE user_id = {0}'.format(message.author.id))
                accumulated = cursor.fetchone()
                accumulated = str(accumulated)
                accumulated = accumulated.replace('(', '').replace(')', '').replace(',', '').replace("'", "")
                sql = 'UPDATE main SET accumulated = ? WHERE user_id = {0}'.format(message.author.id)
                if accumulated == '0':
                    val = (str(lselitem_price),)
                else:
                    pls_accumulated = int(accumulated) + int(lselitem_price)
                    val = (str(pls_accumulated),)
                cursor.execute(sql, val)
                db.commit()

                itemtxt2 = open('./재고/{0}.txt'.format(item), 'r', encoding='utf-8')
                jaego_amount = len(itemtxt2.readlines())
                itemtxt2.close()
                if jaego_amount == 0:
                    os.remove('./재고/{0}.txt'.format(item))
                    print('{0} 의 재고가 소진되어 {1}.txt 파일을 삭제했습니다'.format(item, item)) 

        else:
            await message.channel.send(embed=cantuse)

    if message.content.startswith('!가격수정'):
        if message.author.guild_permissions.administrator:
            j = message.content.split(" ")
            try:
                item = j[1]
            except IndexError:
                await message.channel.send('제품이 지정되지 않았습니다')
                return
            try:
                price = j[2]
            except IndexError:
                await message.channel.send('가격이 지정되지 않았습니다')
                return

            cursor2.execute('SELECT item_price FROM main WHERE item_name = ?', (item,))
            beforeprice = cursor2.fetchone()
            if beforeprice is None:
                embed = discord.Embed(title='❌  오류', description='존재하지 않는 제품입니다', colour=0xFF0000)
                await message.channel.send(embed=embed)
                return
            if not price.isdecimal() or price.startswith('0'):
                await message.channel.send('가격이 올바르지 않습니다')
                return

            beforeprice = str(beforeprice)
            beforeprice = beforeprice.replace('(', '').replace(')', '').replace(',', '').replace("'", "")

            cursor2.execute('UPDATE main SET item_price = {0} WHERE item_name = ?'.format(price), (item,))
            db2.commit()

            cursor2.execute('SELECT item_price FROM main WHERE item_name = ?', (item,))
            afterprice = cursor2.fetchone()
            afterprice = str(afterprice)
            afterprice = afterprice.replace('(', '').replace(')', '').replace(',', '').replace("'", "")

            embed = discord.Embed(colour=discord.Colour.green())
            embed.add_field(name='✅  가격 수정 성공', value='상품: {0}\n이전가격: `{1}`코인\n수정가격: `{2}`코인'.format(item, beforeprice, afterprice))
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(embed=permiss)

    if message.content.startswith('!제품삭제'):
        if message.author.guild_permissions.administrator:
            j = message.content.split(" ")
            try:
                item = j[1]
            except IndexError:
                await message.channel.send('제품이 지정되지 않았습니다')
                return

            cursor2.execute('SELECT item_name FROM main WHERE item_name = ?', (item,))
            itemyn = cursor2.fetchone()

            if itemyn is None:
                embed = discord.Embed(title='❌  오류', description='존재하지 않는 제품입니다', colour=0xFF0000)
                await message.channel.send(embed=embed)
                return

            itemyn = str(itemyn)
            itemyn = itemyn.replace('(', '').replace(')', '').replace(',', '').replace("'", "")

            try:
                cursor2.execute('DELETE FROM main WHERE item_name = ?', (itemyn,))
                embed = discord.Embed(colour=discord.Colour.green())
                embed.add_field(name='✅  제품 삭제 성공', value='{0} 삭제를 성공하였습니다'.format(itemyn))
                await message.channel.send(embed=embed)
                db2.commit()
            except Exception as e:
                print('제품삭제 오류발생\n' + str(e))
                pass
        else:
            await message.channel.send(embed=permiss)

    if message.content.startswith('!경고초기화'):
        if message.author.guild_permissions.administrator:
            try:
                author = message.mentions[0]
                author_id = author.id
            except IndexError:
                await message.channel.send('유저가 지정되지 않았습니다')
                return

            cursor.execute('SELECT wrong_pin FROM main WHERE user_id = {0}'.format(author_id))
            result = cursor.fetchone()
            if result is None:
                embed = discord.Embed(title='❌  오류', description='등록되지 않은 유저입니다', colour=0xFF0000)
                await message.channel.send(embed=embed)
            else:
                sql = 'UPDATE main SET wrong_pin = ? WHERE user_id = {0}'.format(author_id)
                val = (str('0'),)
            cursor.execute(sql, val)
            db.commit()

            embed1 = discord.Embed(colour=discord.Colour.green())
            embed1.add_field(name='✅  경고 초기화 성공', value='{0}님의 경고 횟수를 초기화 하였습니다'.format(author))
            await message.channel.send(embed=embed1)

            embed2 = discord.Embed(colour=discord.Colour.green())
            embed2.add_field(name='✅  경고 초기화', value='경고 횟수가 초기화 되었습니다')
            await author.send(embed=embed2)
        else:
            await message.channel.send(embed=permiss)


@tasks.loop(seconds=5)
async def change_message():
    await client.change_presence(activity=discord.Game(next(status)))


client.run(token)
