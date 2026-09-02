
from multiprocessing import context
from turtle import update

from telegram import Update
from telegram.ext import ConversationHandler, Updater, CommandHandler, CallbackContext, MessageHandler, Application, filters

TOKEN = '8915397953:AAF0t86yYYjw20i0fmJfGkabRI87V7HUwfQ'
ching_status = [10]
mission_status = [["影片請安", "對鏡Edge", "IG Po 相"],
                  ["户外露出相", "姿勢訓練", "Edging", "Thread Update"]]


async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text("歡迎使用本機器人，請輸入指令:\n1. 更改積分\n2. 積分相關\n3. 任務相關")


async def check_mission_command(update: Update, context: CallbackContext) -> str:
    await update.message.reply_text("每日任務(+1pt): \n影片請安 (0/1) \n對鏡Edge (0/1)\nIG Po 相 (0/1) \n \n每週任務(+5pt):  \n户外露出相 (0/1) \n姿勢訓練 (0/3) \nEdging (0/10) \nThread Update (0/1)")


async def update_mission_command(update: Update, context: CallbackContext):
    await update.message.reply_text("請輸入任務內容:")
    message = update.message.text
    await update.message.reply_text(f"任務已新增: {message}")


async def pt_check_command(update: Update, context: CallbackContext):
    if ching_status[0] is not None:
        await update.message.reply_text(f"目前積分為: {ching_status[0]}")
    else:
        await update.message.reply_text("目前尚未有積分。")


# async def status_command(update: Update, context: CallbackContext):
#     flag = False
#     message = update.message.text
#     await update.message.reply_text("請輸入新的積分:")
#     if type(message) == int:
#         ching_status.append(message)
#         await update.message.reply_text(f"積分已更改為: {message}")
#         flag = True
#     else:
#         await update.message.reply_text("請輸入數字")
#     return ching_status

# async def mission_command(update: Update, context: CallbackContext):
#     await update.message.reply_text("請輸入任務內容:")
#     message = update.message.text
#     await update.message.reply_text(f"任務已新增: {message}")

async def handle_response(update: Update, context: CallbackContext, text: str) -> str:
    if "1" in text:
        return "歡迎使用本機器人，請輸入指令:\n1. 更改積分\n2. 積分相關\n3. 任務相關"
    elif "2" in text:
        return "Will develope later"
    elif "3" in text:
        await check_mission_command(update, context)
        await start_command(update, context)
    else:
        return "我不明白你的意思，請輸入有效的指令。"


async def handle_message(update: Update, context: CallbackContext):
    message: str = update.message.text
    print(f'User ({update.message.from_user.username}) sent: {message}')

    response: str = await handle_response(update, context, message)
    print(f'Bot response: {response}')
    await update.message.reply_text(response)

    # if message == "/command1":
    #     await update.message.reply_text("請選擇要執行的指令:\n1. 更改積分\n2. 查詢積分\n3. 其他指令")
    #     #message = update.message.text
    #     if message == "/command1":
    #         await update.message.reply_text("after")
    #         status_amend(update, context, ching_status)
    #         print("積分已更改")
    # elif message == "/command2":
    #     await update.message.reply_text("Who the hell are you?")
    # elif message == "/command3":
    #     await update.message.reply_text("What are you saying?")


async def error(update: Update, context: CallbackContext):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("pt_check", pt_check_command))
    app.add_handler(CommandHandler("check_mission", check_mission_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Start the bot.
    app.run_polling(poll_interval=1.0)
