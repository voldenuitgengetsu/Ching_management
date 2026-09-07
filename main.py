from telegram import Update
from telegram.ext import *

PW, REPS = 1
CHOICE = str(10)  # Definition for the password state
# Definition for the points modification step state
INPUT_POINTS = 2

TOKEN = '8915397953:AAEUxx-NJtqM7bVbUwn9q5NKiDktUzJ8bbw'
ching_status = [10]
mission_status = [[["影片請安", 0, 1], ["對鏡Edge", 0, 1], ["IG Po 相", 0, 1]],
                  [["户外露出相", 0, 1], ["姿勢訓練", 0, 3], ["Edging", 0, 10], ["Thread Update", 0, 1]]]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("歡迎使用本機器人，請輸入指令:\n1. 更改積分\n2. 查詢積分\n3. 查詢任務\n 4. 任務更新")


async def check_mission_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "每日任務(+1pt): \n" + str(mission_status[0][0][0]) + " (" + str(
            mission_status[0][0][1]) + "/" + str(mission_status[0][0][2]) + ") "
        "\n" + str(mission_status[0][1][0]) + " (" + str(mission_status[0]
                                                         [1][1]) + "/" + str(mission_status[0][1][2]) + ")"
        "\n" + str(mission_status[0][2][0]) + " (" + str(mission_status[0]
                                                         [2][1]) + "/" + str(mission_status[0][2][2]) + ") "
        "\n \n"
        "每週任務(+5pt):  \n"
        + str(mission_status[1][0][0]) + " (" + str(mission_status[1]
                                                    [0][1]) + "/" + str(mission_status[1][0][2]) + ") "
        "\n" + str(mission_status[1][1][0]) + " (" + str(mission_status[1]
                                                         [1][1]) + "/" + str(mission_status[1][1][2]) + ") "
        "\n" + str(mission_status[1][2][0]) + " (" + str(mission_status[1]
                                                         [2][1]) + "/" + str(mission_status[1][2][2]) + ") "
        "\nThread Update (" + str(mission_status[1][3][1]) +
        "/" + str(mission_status[1][3][2]) + ")"
    )


async def pt_check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ching_status[0] is not None:
        await update.message.reply_text(f"目前積分為: {ching_status[0]}")
    else:
        await update.message.reply_text("目前尚未有積分。")


async def update_mission_intake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("請選擇要更新的任務。")
    return CHOICE


async def update_mission_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    flag = False
    for i in range(len(mission_status[0])+len(mission_status[1])):
        if choice in mission_status[0][i][0]:
            flag = True
        elif choice in mission_status[1][i][0]:
            flag = True

    if flag:
        await update.message.reply_text("請輸入完成次數:")
        return REPS, choice
    else:
        await update.message.reply_text("請輸入有效的任務名稱。")
        return CHOICE


async def update_mission_reps_command(update: Update, context: ContextTypes.DEFAULT_TYPE, choice: str):
    reps = update.message.text
    flag = False
    for i in range(len(mission_status[0])+len(mission_status[1])):
        if choice in mission_status[0][i][0]:
            flag = True
            mission_status[0][i][1] += int(reps)
        elif choice in mission_status[1][i][0]:
            flag = True
            mission_status[1][i][1] += int(reps)

    if flag:
        await update.message.reply_text("任務完成次數已更新。")
        await check_mission_command(update, context)
        await start_command(update, context)
        return ConversationHandler.END
    else:
        await update.message.reply_text("請輸入有效的任務名稱。")
        return CHOICE

# ----------------- Conversation State Machine Flow Start -----------------

# Step 1: Triggered when the user enters "1"


async def password_intake(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("請輸入密碼:")
    return PW  # Switch to PW state and wait for the password input


# Step 2: Validate the password input
async def password_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    password = update.message.text

    # Validation Guard: If the text is "1" (the initial entry trigger), ignore it and keep waiting for the actual password
    if password == "1":
        return PW

    if password == "1234":  # Assuming the password is "1234"
        await update.message.reply_text("密碼正確！請輸入新的積分分數:")
        # Password matches, move to the next state to let the user input the points
        return INPUT_POINTS
    else:
        await update.message.reply_text("密碼錯誤，無法更改積分。對話結束。")
        await start_command(update, context)
        return ConversationHandler.END


# Step 3: Receive and update the score integer
async def pt_change_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message_text = update.message.text
    try:
        new_points = int(message_text)
        ching_status[0] = new_points
        await update.message.reply_text(f"積分已更改為: {new_points}")
    except ValueError:
        await update.message.reply_text("請輸入有效的數字。")
        # If the input is not a number, keep the user in this state to try again
        return INPUT_POINTS

    await start_command(update, context)
    return ConversationHandler.END

# ----------------- Conversation State Machine Flow End -----------------


# Handle generic text messages (Handles options 2 and 3; option 1 is omitted)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    print(f'User ({update.message.from_user.username}) sent: {message}')

    if message == "2":
        await pt_check_command(update, context)
        await start_command(update, context)
    elif message == "3":  # 查詢任務
        await check_mission_command(update, context)
        await start_command(update, context)
    elif message == "1":
        # Start the password intake flow
        await password_intake(update, context)
        # Immediately call the password command to handle the input
        await password_command(update, context)
        # Immediately call the points change command to handle the input
        await pt_change_command(update, context)
        pass
    elif message == "4":  # 任務更新
        await check_mission_command(update, context)
        await update_mission_intake(update, context)

    else:
        await update.message.reply_text("請輸入有效的指令。")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    # 1. Define the ConversationHandler for managing password and points modification states
    conversation_handler_pt_change = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^1$"), password_intake)],
        states={
            PW: [MessageHandler(filters.TEXT & ~filters.COMMAND, password_command)],
            INPUT_POINTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, pt_change_command)],
        },
        fallbacks=[CommandHandler("start", start_command)]
    )

    conversation_handler_mission_update = ConversationHandler(
        entry_points=[MessageHandler(
            filters.Regex("^4$"), update_mission_intake)],
        states={
            CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_mission_command)],
            REPS: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_mission_reps_command)],
        },
        fallbacks=[CommandHandler("start", start_command)]
    )

    # ⚠️ [CRITICAL] The ConversationHandler must be added BEFORE the regular MessageHandler!
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("pt_check", pt_check_command))
    app.add_handler(CommandHandler("check_mission", check_mission_command))

    # Registers the state machine
    app.add_handler(conversation_handler_pt_change)
    # Registers the state machine
    app.add_handler(conversation_handler_mission_update)

    # ⚠️ The generic text MessageHandler must be added last and must explicitly filter out "1" to avoid intercepting state entries
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.Regex("^1$"), handle_message))

    app.add_error_handler(error)

    print("Bot started...")
    app.run_polling(poll_interval=2)
