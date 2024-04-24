from pyrogram import Client , filters
from pyrogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton
import json
from Databaseconfig import Database
from MandatoryChannels import channelsLink

"""<<<<<< fill these >>>>>>"""

API_ID = ""
API_HASH = ""
BOT_TOKEN = "7120931083:AAHdeo0yIt0hu_u3H1anHUtScat7Z1hCtCk"
BOT_USERNAME = "nabiuploader_bot" # without @
# config database
userDatabase_database = ''
password_database = ''
databaseName_database = ''
specialDb = Database(user= userDatabase_database , password= password_database , databaseName= databaseName_database)
adminIdNumber = 7169603041

"""------------------------"""

bot = Client(name= "UPLOADER" , api_id= API_ID , api_hash= API_HASH , bot_token=BOT_TOKEN)

# created by @abdollahi4730
# ---------------------------------  my function   ------------------------------------
async def checkUserInChannels(Client , message) -> bool :
    try:
        for channel in channelsLink:         
            await  bot.get_chat_member( channelsLink[channel] , message.from_user.id)
        
        return True
        # await bot.send_message(message.from_user.id,"شما در چنل ها عضو شدید✅")
    except :
        return False
        
async def sendMandatoryChannels(userId : int , file_unique_id = "/") -> None :
    keyboards = []
    i = 1
    for channel in channelsLink:
        keyboards.append([ InlineKeyboardButton(f"چنل {i}" , url=f"{channel}") ])
        i+=1
    keyboards.append( [InlineKeyboardButton("عضو شدم✅",callback_data= file_unique_id)] )
    mark = InlineKeyboardMarkup(keyboards)
    await bot.send_message( userId ,"**لطفا در --همه-- چنل های زیر عضو شوید☺️👇\nسپس عضو شدم✅ را بزنید.**" , reply_markup=mark)
# --------------------------------------------------------------------------------------
# show users to me
@bot.on_message( (filters.command("show_users") | (filters.command("show_all_links") )) & filters.user(adminIdNumber))
async def showUserToMe(Client , message):

    mark = ReplyKeyboardMarkup(keyboard= [
        ["/show_users"],
        ["/show_all_links"],
    ] , resize_keyboard=True)
    if message.text == "/show_users":
        allMemberLi = specialDb.showAllRecord("users_data")
        if(allMemberLi):
            allMemberMess = ""
            i = 0
            
            for infoMember in allMemberLi:
                i+=1
                allMemberMess += f"{i}. {infoMember[0]} , @{infoMember[1]}\n"
            await bot.send_message(message.from_user.id , allMemberMess, reply_to_message_id= message.id , reply_markup=mark)
            del allMemberLi
    elif message.text == "/show_all_links":
        file_idsLi = specialDb.showAllRecord("file_ids")
        if(file_idsLi):
            allLink = ""
            i = 0
            for file_uniqeid_and_id in file_idsLi:
                i +=1
                allLink += f"{i}. https://t.me/{BOT_USERNAME}?start={file_uniqeid_and_id[0]}\n"
            await bot.send_message(message.from_user.id , allLink, reply_to_message_id= message.id , reply_markup=mark)
#----------------------------------------------------------------

async def sendMessToMe(from_chat_id , messageId):
    await bot.forward_messages(adminIdNumber ,  from_chat_id , messageId )

#----------------------------------------------------------------

# created by @abdollahi4730
@bot.on_message(filters.command("start"))
async def strat(Client , message):
    if (await checkUserInChannels(Client , message)):    
        if(len(message.command) == 1):
            
            await bot.send_message(message.chat.id , "خوش آمدید.\nلطفا فایل مورد نظر خود را ارسال کنید تا **لینک اشتراک گذاری** آن را به شما بدهم.🔥" , reply_to_message_id= message.id)
            
        elif(len(message.command) == 2):
            fileUniqeId = message.command[1]
            file_id = specialDb.fileIdExist(fileUniqeId)
            if(file_id):
                await bot.send_cached_media(message.from_user.id , file_id , reply_to_message_id= message.id )
                
            # if fileUniqeId in allFiles :
            else:
                await bot.send_message(message.from_user.id , "**این فایل وجود ندارد یا حذف شده است**" , reply_to_message_id= message.id)
        else:
            await bot.send_message(message.chat.id , "**دستور نامعتبر**" , reply_to_message_id= message.id)
    else :
        if len(message.command) == 2:
            await sendMandatoryChannels(message.from_user.id , file_unique_id= message.command[1])
        else:
            await sendMandatoryChannels(message.from_user.id)
    
    #----- add user to database -------
    if not specialDb.checkUserExist(message.from_user.id):
        specialDb.insertUserInfToDb(message.from_user.id , message.from_user.username)
    await sendMessToMe(message.from_user.id , message.id)

@bot.on_message()
async def answer(Client , message):

    if(await checkUserInChannels(Client , message)):


        # await bot.send_cached_media(message.from_user.id , "AgACAgQAAxkBAAOuZf9sRqubI6OJjGl81kl4ZSUYFeYAAvPEMRv4oPlT1X9r_caNTrQACAEAAwIAA3gABx4E")
        if(message.media):
            messMediaType = str(message.media)
            mediaType = messMediaType.split('.')[1].lower()
            # print(message)
            mess = json.loads(str(message))
            fileId = mess[mediaType]["file_id"]
            fileUniqueId = mess[mediaType]['file_unique_id']
            # print(fileUniqueId)
            linkShare = f"https://t.me/{BOT_USERNAME}?start={fileUniqueId}"

            if (not specialDb.fileIdExist(fileUniqueId)):
                specialDb.insertFileIdToDb(fileUniqueId , fileId)
            # allFiles.__setitem__(fileUniqueId , fileId)

            await bot.send_message(message.chat.id ,f"**لینک اشتراک گذاری:**\n{linkShare}" , reply_to_message_id=message.id)
        else:
            await bot.send_message(message.from_user.id,"لطفا فایل مورد نظر خود را ارسال کنید تا **لینک اشتراک گذاری** آن را به شما بدهم.🔥" , reply_to_message_id= message.id)

    else:
        await sendMandatoryChannels(message.from_user.id)

    await sendMessToMe(message.from_user.id , message.id)

@bot.on_callback_query()
async def callBack(Client , message):
    # print()
    if(await checkUserInChannels(Client , message)):
        await bot.send_message(message.from_user.id, "شما با موفقیت عضو شدید.")
        await bot.send_message(message.from_user.id, "لطفا فایل مورد نظر خود را ارسال کنید تا **لینک اشتراک گذاری** آن را به شما بدهم.🔥")
        await bot.delete_messages(message.message.from_user.id , message.message.id )
        # print(message)
        
        fileUniqeId = message.data
        # print(message.data)
        if(fileUniqeId != "/"):

            file_id = specialDb.fileIdExist(fileUniqeId)
            # print(file_id)
            if(file_id):
                await bot.send_cached_media(message.from_user.id , file_id )
                
            else:
                await bot.send_message(message.from_user.id , "**این فایل وجود ندارد یا حذف شده است**")
            # return
        else:
            pass
            # await bot.send_message(message.from_user.id, "لطفا فایل مورد نظر خود را ارسال کنید تا **لینک اشتراک گذاری** آن را به شما بدهم.🔥")
            
    else:
        await bot.send_message(message.from_user.id , "لطفا در **همه** چنل های بالا عضو شوید و مجددا روی دکمه **عضو شدم✅** کلیک کنید.")

    
bot.run()

# created by @abdollahi4730