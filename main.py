from bot import *
from algorithms import *
from secret import *


if __name__ == '__main__':  # Чтоб это всё не загнулось при ошибке
    executor.start_polling(dp, skip_updates=True)