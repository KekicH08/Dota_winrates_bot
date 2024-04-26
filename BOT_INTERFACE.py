import asyncio
import logging
import sqlite3

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler

import HERO_MAP
from INFO_SEARCHER import most_popular_characters_for_pos, best_worst_pos_winrate
from TOKEN import bot_token

heroes = [i.lower() for i in HERO_MAP.hero_names_default.keys()]

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

sqlite_connection = sqlite3.connect('DB.db')
cursor = sqlite_connection.cursor()


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("")


async def start(update, context):
    global markup

    context.user_data.clear()
    markup = ReplyKeyboardMarkup([['Рекрут', 'Страж'],
                                  ['Рыцарь', 'Герой'],
                                  ['Легенда', 'Властелин'],
                                  ['Божество', 'Титан'],
                                  ['/stop']], one_time_keyboard=True)
    await update.message.reply_text(
        "Бот предоставляет вам информацию о доли побед и количестве матчей "
        "за героев Доты на разных рангах и позициях. Информация с сайта Stratz. Выберите название своего ранга",
        reply_markup=markup)
    return 1


async def first_response(update, context):
    global markup

    markup = ReplyKeyboardMarkup([['Лучшие герои на позицию'],
                                  ['Лучшая позиция для героя'],
                                  ['Изменить ранг'],
                                  ['Создать сборку предметов'],
                                  ['Найти сборку предметов'],
                                  ['/stop']], one_time_keyboard=True)
    context.user_data['rank'] = update.message.text
    rank = update.message.text
    await update.message.reply_text(
        f"Ваш ранг {HERO_MAP.brackets[rank.lower()]}, что вас интересует?", reply_markup=markup)
    return 2


async def search(update, context):
    global markup

    if update.message.text == 'Лучшие герои на позицию':
        markup = ReplyKeyboardMarkup([['1', '2'],
                                      ['3', '4'],
                                      ['5', 'Изменить ранг'],
                                      ['/stop']], one_time_keyboard=True)
        await update.message.reply_text(
            f"{context.user_data['rank']}, какая позиция вас интересует?", reply_markup=markup)
        return 3

    elif update.message.text == 'Лучшая позиция для героя':
        markup = ReplyKeyboardMarkup([['Изменить ранг'],
                                      ['/stop']], one_time_keyboard=True)
        await update.message.reply_text(
            f"{context.user_data['rank']}, какой герой вас интересует? Напишите точное имя на английском",
            reply_markup=markup)
        return 4

    elif update.message.text == 'Изменить ранг':
        markup = ReplyKeyboardMarkup([['Рекрут', 'Страж'],
                                      ['Рыцарь', 'Герой'],
                                      ['Легенда', 'Властелин'],
                                      ['Божество', 'Титан'],
                                      ['/stop']], one_time_keyboard=True)
        await update.message.reply_text("Выберите название своего ранга", reply_markup=markup)
        return 1

    elif update.message.text == 'Создать сборку предметов':
        markup = ReplyKeyboardMarkup([['Изменить ранг'],
                                      ['/stop']], one_time_keyboard=True)
        await update.message.reply_text("Введите имя героя", reply_markup=markup)
        return 5

    elif update.message.text == 'Найти сборку предметов':
        query = f"""SELECT guide_name, rank, hero, position, likes
                    FROM Items_guides"""
        cursor = sqlite_connection.cursor()
        response = cursor.execute(query).fetchall()
        sqlite_connection.commit()
        cursor.close()
        markup = ReplyKeyboardMarkup([['/stop']], one_time_keyboard=True)
        answer = ''
        for i in response:
            answer += f'Сборка: {i[0]}; Ранг: {i[1]}; Герой: {i[2]}; Позиция: {i[3]}; Понравилось: {i[4]}\n\n'
        await update.message.reply_text(f'{answer}Введите название, заинтересовавшей вас сборки',
                                        reply_markup=markup)
        return 9


async def guide_hero(update, context):
    global markup

    if update.message.text == 'Изменить ранг':
        markup = ReplyKeyboardMarkup([['Рекрут', 'Страж'],
                                      ['Рыцарь', 'Герой'],
                                      ['Легенда', 'Властелин'],
                                      ['Божество', 'Титан'],
                                      ['/stop']], one_time_keyboard=True)
        await update.message.reply_text("Выберите название своего ранга", reply_markup=markup)
        return 1

    context.user_data['hero'] = update.message.text
    hero = update.message.text
    markup = ReplyKeyboardMarkup([['1', '2'],
                                  ['3', '4'],
                                  ['5', 'Изменить ранг'],
                                  ['/stop']], one_time_keyboard=True)
    await update.message.reply_text(
        f"{context.user_data['rank']}, на какой позиции будет {hero}?", reply_markup=markup)
    return 6


async def guide_pos(update, context):
    if update.message.text == 'Изменить ранг':
        markup = ReplyKeyboardMarkup([['Рекрут', 'Страж'],
                                      ['Рыцарь', 'Герой'],
                                      ['Легенда', 'Властелин'],
                                      ['Божество', 'Титан'],
                                      ['/stop']], one_time_keyboard=True)
        await update.message.reply_text("Выберите название своего ранга", reply_markup=markup)
        return 1

    context.user_data['pos'] = update.message.text
    pos = update.message.text
    await update.message.reply_text(
        f"Введите название сборки предметов на {context.user_data['hero']} {pos}-ой позиции\n"
        f"Должно быть не более 30 символов")
    return 7


async def guide_name(update, context):
    if update.message.text == 'Изменить ранг':
        markup = ReplyKeyboardMarkup([['Рекрут', 'Страж'],
                                      ['Рыцарь', 'Герой'],
                                      ['Легенда', 'Властелин'],
                                      ['Божество', 'Титан'],
                                      ['/stop']], one_time_keyboard=True)
        await update.message.reply_text("Выберите название своего ранга", reply_markup=markup)
        return 1

    context.user_data['name'] = update.message.text
    name = update.message.text

    try:
        query = f"""SELECT guide_name
                    FROM Items_guides
                    WHERE guide_name = '{name}'"""
        cursor = sqlite_connection.cursor()
        response = cursor.execute(query).fetchall()
        sqlite_connection.commit()
        cursor.close()
        if response != []:
            await update.message.reply_text("Сборка с таким названием уже существует, введите другое")
            return 7
    except Exception:
        pass

    if len(name) > 30:
        await update.message.reply_text("Название слишком длинное, попробуйте другое")
        return 7
    markup = ReplyKeyboardMarkup([['/stop']], one_time_keyboard=True)
    await update.message.reply_text(
        f"Введите названия шести предметов в сборке через , на {context.user_data['hero']} {context.user_data['pos']}"
        f"-ой позиции (так чтобы вас потом поняли)", reply_markup=markup)
    return 8


async def guide_items(update, context):
    if update.message.text == 'Изменить ранг':
        markup = ReplyKeyboardMarkup([['Рекрут', 'Страж'],
                                      ['Рыцарь', 'Герой'],
                                      ['Легенда', 'Властелин'],
                                      ['Божество', 'Титан'],
                                      ['/stop']], one_time_keyboard=True)
        await update.message.reply_text("Выберите название своего ранга", reply_markup=markup)
        return 1

    items = update.message.text
    query = f"""INSERT INTO Items_guides
                (guide_name, rank, hero, position, items, likes)
                VALUES
                ('{context.user_data['name']}', '{context.user_data['rank']}', '{context.user_data['hero']}', 
                {context.user_data['pos']}, '{items}', {0})"""
    cursor = sqlite_connection.cursor()
    cursor.execute(query)
    sqlite_connection.commit()
    cursor.close()

    markup = ReplyKeyboardMarkup([['Лучшие герои на позицию'],
                                  ['Лучшая позиция для героя'],
                                  ['Изменить ранг'],
                                  ['Создать сборку предметов'],
                                  ['Найти сборку предметов'],
                                  ['/stop']], one_time_keyboard=True)
    await update.message.reply_text("Что дальше?", reply_markup=markup)
    return 2


async def searcher_by_pos(update, context):
    global markup

    if update.message.text == 'Изменить ранг':
        markup = ReplyKeyboardMarkup([['Рекрут', 'Страж'],
                                      ['Рыцарь', 'Герой'],
                                      ['Легенда', 'Властелин'],
                                      ['Божество', 'Титан'],
                                      ['/stop']], one_time_keyboard=True)
        await update.message.reply_text("Выберите название своего ранга", reply_markup=markup)
        return 1

    markup = ReplyKeyboardMarkup([])
    context.user_data['pos'] = update.message.text
    pos = update.message.text
    rank = HERO_MAP.brackets[context.user_data['rank'].lower()]
    await update.message.reply_text(
        f"Скоро ответим")
    answer = await most_popular_characters_for_pos(pos, rank)
    url = "_".join(f'https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/'
                   f'{answer[1][0].lower()}.png'.split())
    print(url)
    await update.message.reply_text(
                                    f"Самая популярные герои за последнюю неделю на {pos} pos, ранг {rank}:\n\n"
                                    f"1 - {answer[1][0]}, кол-во игр: {answer[1][1]}, доля побед: {answer[1][2]}%\n\n"
                                    f"2 - {answer[2][0]}, кол-во игр: {answer[2][1]}, доля побед: {answer[2][2]}%\n\n"
                                    f"3 - {answer[3][0]}, кол-во игр: {answer[3][1]}, доля побед: {answer[3][2]}%",
                                    await send_picture(update, context, url))

    markup = ReplyKeyboardMarkup([['Лучшие герои на позицию'],
                                  ['Лучшая позиция для героя'],
                                  ['Изменить ранг'],
                                  ['Создать сборку предметов'],
                                  ['Найти сборку предметов'],
                                  ['/stop']], one_time_keyboard=True)
    await update.message.reply_text("Что дальше?", reply_markup=markup)
    return 2


async def searcher_by_hero(update, context):
    global markup

    if update.message.text == 'Изменить ранг':
        markup = ReplyKeyboardMarkup([['Рекрут', 'Страж'],
                                      ['Рыцарь', 'Герой'],
                                      ['Легенда', 'Властелин'],
                                      ['Божество', 'Титан'],
                                      ['/stop']], one_time_keyboard=True)
        await update.message.reply_text("Выберите название своего ранга", reply_markup=markup)
        return 1

    markup = ReplyKeyboardMarkup([['/stop']])
    context.user_data['hero'] = update.message.text
    hero = update.message.text
    rank = HERO_MAP.brackets[context.user_data['rank'].lower()]
    if hero.lower() in heroes:
        answer = await (best_worst_pos_winrate(hero, rank))
        await update.message.reply_text(
            f"Скоро ответим", reply_markup=markup)
        await update.message.reply_text(
            f"Самая популярная позиция на {hero}, ранг {rank}:\n\n{answer['most_popular'][0]} pos - "
            f"Кол-во игр: {answer['most_popular'][2]}, доля побед: {answer['most_popular'][1]}%\n\n"
            f"Лучшая доля побед: {answer['best'][0]} pos - {answer['best'][1]}%, кол-во игр: {answer['best'][2]}\n\n"
            f"Худшая доля побед: {answer['worst'][0]} pos - {answer['worst'][1]}%, кол-во игр: {answer['worst'][2]}",
            reply_markup=markup)
    else:
        await update.message.reply_text(
            f"Герой не найден, попробуйте заново ввести его имя", reply_markup=markup)
        return 4
    markup = ReplyKeyboardMarkup([['Лучшие герои на позицию'],
                                  ['Лучшая позиция для героя'],
                                  ['Изменить ранг'],
                                  ['Создать сборку предметов'],
                                  ['Найти сборку предметов'],
                                  ['/stop']], one_time_keyboard=True)
    await update.message.reply_text("Что дальше?", reply_markup=markup)
    return 2


async def guide(update, context):
    global markup

    try:
        name = update.message.text
        context.user_data['name'] = name
        query = f"""SELECT guide_name, rank, hero, position, items, likes
                                  FROM Items_guides
                                  WHERE guide_name = '{name}'"""
        cursor = sqlite_connection.cursor()
        response = cursor.execute(query).fetchone()
        sqlite_connection.commit()
        cursor.close()
        await update.message.reply_text(f"Название: {response[0]}\n"
                                        f"Ранг:  {response[1]}\n"
                                        f"Герой: {response[2]}\n"
                                        f"Позиции: {response[3]}\n"
                                        f"Предметы: {response[4]}\n"
                                        f"Понравилось: {response[5]}\n")

        markup = ReplyKeyboardMarkup([['Да', 'Нет'],
                                      ['/stop']], one_time_keyboard=True)
        await update.message.reply_text("Была ли вам полезна эта сборка?", reply_markup=markup)
        return 10

    except Exception:
        await update.message.reply_text("Сборка не найдена, попробуйте снова")
        return 9


async def like_guide(update, context):
    global markup
    if update.message.text == 'Да':
        try:
            await update.message.reply_text("Спасибо!")
            query = f"""SELECT likes FROM Items_guides
                        WHERE guide_name = '{context.user_data['name']}'"""
            cursor = sqlite_connection.cursor()
            likes = cursor.execute(query).fetchone()[0] + 1
            query = f"""UPDATE Items_guides
                        SET likes = {likes}
                        WHERE guide_name = '{context.user_data['name']}'"""
            cursor.execute(query)
            sqlite_connection.commit()
            cursor.close()
        except Exception:
            pass

    markup = ReplyKeyboardMarkup([['Лучшие герои на позицию'],
                                  ['Лучшая позиция для героя'],
                                  ['Изменить ранг'],
                                  ['Создать сборку предметов'],
                                  ['Найти сборку предметов'],
                                  ['/stop']], one_time_keyboard=True)
    await update.message.reply_text("Что дальше?", reply_markup=markup)
    return 2


async def send_picture(update, context, url):
    await context.bot.send_photo(update.message.chat.id, photo=url)


async def stop(update, context):
    global markup
    context.user_data.clear()
    markup = ReplyKeyboardMarkup([['/start']])
    await update.message.reply_text("Всего доброго! Чтобы начать заново, введите команду /start", reply_markup=markup)
    return ConversationHandler.END


def main():
    global markup
    # Создаём объект Application.
    application = Application.builder().token(bot_token).build()
    markup = ReplyKeyboardMarkup([['/start']], one_time_keyboard=False)
    # application.add_handler(text_handler)
    application.add_handler(CommandHandler("help", help_command))
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, search)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, searcher_by_pos)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, searcher_by_hero)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, guide_hero)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, guide_pos)],
            7: [MessageHandler(filters.TEXT & ~filters.COMMAND, guide_name)],
            8: [MessageHandler(filters.TEXT & ~filters.COMMAND, guide_items)],
            9: [MessageHandler(filters.TEXT & ~filters.COMMAND, guide)],
            10: [MessageHandler(filters.TEXT & ~filters.COMMAND, like_guide)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    asyncio.run(application.run_polling())


if __name__ == '__main__':
    main()
