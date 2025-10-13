# handlers.py
import os
from dotenv import load_dotenv
load_dotenv()

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import json
from langchain_together import ChatTogether

# Загружаем API-ключ
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("❌ TOGETHER_API_KEY не найден в .env")

# Инициализируем LLM
llm = ChatTogether(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    api_key=TOGETHER_API_KEY,
    temperature=0.7,
    max_tokens=1024,
)

router = Router()

# Загружаем вопросы
with open("questions.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Главное меню
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да, очень хочу")],
        [KeyboardButton(text="Нет настроения")],
        [KeyboardButton(text="Узнать про книги")],
        [KeyboardButton(text="Просто поболтать")]
    ],
    resize_keyboard=True
)

class Menu(StatesGroup):
    waiting_for_answer = State()
    chatting = State()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Добро пожаловать в Магическую библиотеку, {message.chat.first_name}! Давай с тобой познакомимся. Я задам тебе несколько вопросиков, а ты будешь отвечать. Играем?",
        reply_markup=start_keyboard
    )

@router.message(F.text.lower() == 'да, очень хочу')
async def start_quiz(message: Message, state: FSMContext):
    question_data = data["questions"][0]
    question = question_data["question"]
    options = question_data["options"]
    correct_answer = question_data["correct_answer"]

    await state.update_data(correct_answer=correct_answer, current_question_index=0)

    answer_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=option)] for option in options],
        resize_keyboard=True
    )

    await message.answer(f"Вот твой вопрос: {question}", reply_markup=answer_keyboard)
    await message.answer("Выбери правильный ответ:")
    await state.set_state(Menu.waiting_for_answer)

@router.message(F.text.lower() == 'просто поболтать')
async def start_chatting(message: Message, state: FSMContext):
    await message.answer(
        "Отлично! Давай просто поболтаем. Задавай любой вопрос или расскажи что-нибудь интересное.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Вернуться в меню")]],
            resize_keyboard=True
        )
    )
    await state.set_state(Menu.chatting)

@router.message(Menu.chatting, F.text.lower() == 'вернуться в меню')
async def return_to_menu(message: Message, state: FSMContext):
    await message.answer("Возвращаемся в главное меню.", reply_markup=start_keyboard)
    await state.clear()

@router.message(Menu.chatting, F.text)
async def handle_chat(message: Message):
    try:
        response = llm.invoke(message.text)
        await message.answer(response.content if hasattr(response, 'content') else str(response))
    except Exception as e:
        await message.answer("Произошла ошибка при генерации ответа. Попробуйте позже.")

async def generate_praise():
    try:
        response = llm.invoke("Придумай уникальный и вдохновляющий комплимент для человека, который правильно ответил на вопрос. Будь креативным и используй магический стиль.")
        return response.content if hasattr(response, 'content') else "Правильно! Ты настоящий знаток!"
    except:
        return "Правильно! Ты настоящий знаток!"

@router.message(Menu.waiting_for_answer, F.text)
async def handle_answer(message: Message, state: FSMContext):
    user_answer = message.text
    state_data = await state.get_data()
    correct_answer = state_data["correct_answer"]
    current_question_index = state_data["current_question_index"]

    if user_answer == correct_answer:
        praise = await generate_praise()
        await message.answer(praise)
        await message.answer("Продолжим?")

        next_question_index = current_question_index + 1
        if next_question_index < len(data["questions"]):
            next_question_data = data["questions"][next_question_index]
            question = next_question_data["question"]
            options = next_question_data["options"]
            correct_answer = next_question_data["correct_answer"]

            await state.update_data(correct_answer=correct_answer, current_question_index=next_question_index)

            answer_keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=option)] for option in options],
                resize_keyboard=True
            )

            await message.answer(f"Вот твой следующий вопрос: {question}", reply_markup=answer_keyboard)
            await message.answer("Выбери правильный ответ:")
        else:
            await message.answer("Ты ответил на все вопросы! Молодец!")
            await state.clear()
    else:
        await message.answer("Неправильно. Тебе нужно больше читать и узнавать новое. Могу порекомендовать тебе книгу.")
        await message.answer("Я рекомендую тебе прочитать 'Мастер и Маргарита' Михаила Булгакова. Это произведение полное загадок и глубоких смыслов.")
        await state.clear()

@router.message(F.text.lower() == 'нет настроения')
async def no_mood(message: Message):
    await message.answer("Жаль, что у тебя нет настроения. Возвращайся, когда захочешь узнать что-то новое!")

@router.message(F.text.lower() == 'узнать про книги')
async def recommend_books(message: Message):
    books = [
        "1. 'Мастер и Маргарита' — Михаил Булгаков",
        "2. 'Преступление и наказание' — Фёдор Достоевский",
        "3. '1984' — Джордж Оруэлл",
        "4. 'Маленький принц' — Антуан де Сент-Экзюпери",
        "5. 'Гарри Поттер и философский камень' — Дж. К. Роулинг"
    ]
    await message.answer("Вот несколько книг, которые могут тебе понравиться:")
    for book in books:
        await message.answer(book)
    await message.answer("Выбери книгу, чтобы узнать больше об авторе:")

@router.message(
    F.text & ~F.text.lower().in_(["узнать про книги", "да, очень хочу", "нет настроения", "просто поболтать"])
)
async def book_selected(message: Message):
    user_input = message.text.strip().lower()

    book_variants = {
        "мастер и маргарита": ["мастер и маргарита", "мастер", "маргарита", "булгаков"],
        "преступление и наказание": ["преступление и наказание", "преступление", "наказание", "достоевский"],
        "1984": ["1984", "оруэлл", "джордж оруэлл"],
        "маленький принц": ["маленький принц", "принц", "антуан де сент-экзюпери", "сент-экзюпери"],
        "гарри поттер и философский камень": ["гарри поттер и философский камень", "гарри поттер", "поттер", "джоан роулинг", "роулинг"]
    }

    selected_book = None
    for book, variants in book_variants.items():
        if user_input in variants:
            selected_book = book
            break

    authors_info = {
        "мастер и маргарита": "Михаил Булгаков — русский писатель, драматург и театральный режиссер. Родился в 1891 году в Киеве. Его самое известное произведение — 'Мастер и Маргарита', которое сочетает в себе элементы сатиры, фантастики и философии. Булгаков также известен своими пьесами, такими как 'Дни Турбиных' и 'Бег'.",
        "преступление и наказание": "Фёдор Достоевский — один из величайших русских писателей. Родился в 1821 году в Москве. Его роман 'Преступление и наказание' исследует темы морали, вины и искупления. Достоевский также известен своими произведениями 'Братья Карамазовы', 'Идиот' и 'Бесы'.",
        "1984": "Джордж Оруэлл — английский писатель и публицист. Родился в 1903 году в Индии. Его роман '1984' — это антиутопия, которая описывает тоталитарное общество под постоянным наблюдением. Оруэлл также известен своими произведениями 'Скотный двор' и 'Дорога на Уиган-Пирс'.",
        "маленький принц": "Антуан де Сент-Экзюпери — французский писатель и летчик. Родился в 1900 году в Лионе. Его самое известное произведение — 'Маленький принц', философская сказка для детей и взрослых. Экзюпери также известен своими книгами 'Ночной полет' и 'Планета людей'.",
        "гарри поттер и философский камень": "Джоан Роулинг — британская писательница, автор серии книг о Гарри Поттере. Родилась в 1965 году в Йейте, Англия. Ее книги о Гарри Поттере стали мировым бестселлером и были экранизированы. Роулинг также известна своими благотворительными инициативами."
    }

    if selected_book in authors_info:
        await message.answer(authors_info[selected_book])
    else:
        await message.answer("Пожалуйста, выбери одну из предложенных книг. Например, напиши 'Мастер и Маргарита'.")