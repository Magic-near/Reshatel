import config
import telebot
import math

bot = telebot.TeleBot(config.access_token)


def convert_to_bergman(data):
    for ch in data:
        if ch not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ','}:
            return 'Неверный формат данных'
    data_1 = ''
    for i in range(len(data)):    
        if data[i] == ',':
            data_1 += '.'
        else:
            data_1 += data[i]
    Phi = (1 + 5 ** 0.5) / 2
    power = 1
    result = ''
    data = float(data_1)
    while power <= data:
        power *= Phi
    while data > 0:
        if power == 1:
            result += '.'
        power /= Phi
        if abs(power - data) < 0.000001 or power < data:
            data -= power
            result += '1'
        else:
            result += '0'
    return result


def convert_from_bergman(data):
    for ch in data:
        if ch not in {'0', '1', '.', ','}:
            return 'Неверный формат данных'
    data_1 = ''
    for i in range(len(data)):    
        if data[i] == ',':
            data_1 += '.'
        else:
            data_1 += data[i]
    Phi = (1 + 5 ** 0.5) / 2
    result = 0
    data = data_1
    c = False
    for ch in data:
        if ch == '.':
            c = True
    if c == False:
        data = data + '.'
    dot = data.index('.')
    data1 = data[:dot]
    data2 = data[dot+1:]
    power1 = len(data1) - 1
    power2 = -1
    for ch in data1:
        if ch == '1':
            result += Phi ** power1
        power1 -= 1
    for ch in data2:
        if ch == '1':
            result += Phi ** power2
        power2 -= 1
    result = float(result)
    return str(result)


def convert_to_zeckendorf(data):
    for ch in data:
        if ch not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            return 'Неверный формат данных'
    data = int(data)
    f0, f1 = 0, 1
    resnum = []
    num = -1
    result = ''
    while data != 0:
        while f1 <= data:
            f0, f1 = f1, f0 + f1
            num += 1
            if f1 > data:
                data -= f0
                resnum.append(num)
                f0, f1 = 0, 1
                num = -1
    i = resnum[0]
    while i > 0:
        k = 0
        check = False
        while k < len(resnum):
            if i == resnum[k]:
                result += '1'
                check = True
            k += 1
        if check is False:
            result += '0'
        i -= 1
    return result


def convert_from_zeckendorf(data):
    for ch in data:
        if ch not in {'0', '1'}:
            return 'Неверный формат данных'
    f0, f1 = 0, 1
    i = 0
    data = data[::-1]
    result = 0
    while i < len(data):
        f0, f1 = f1, f0 + f1
        if data[i] == '1':
            result += f1
        i += 1
    return str(result)


def convert_to_factorial(data):
    for ch in data:
        if ch not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            return 'Неверный формат данных'
    data = int(data)
    i = 2
    result = ''
    while data > 0:
        result += str(data % i)
        data = data // i
        i += 1
    result = result[::-1]
    return result


def convert_from_factorial(data):
    result = 0
    data = data[::-1]
    for i in range(len(data)):
        if int(data[i]) >= i + 2:
            return 'Неверный формат данных'
        result += int(data[i]) * math.factorial(i+1)
    return str(result)


def convert_to_negative(data, target):
    for ch in data:
        if ch not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-'}:
            return 'Неверный формат данных'
    for ch in target:
        if ch not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-'}:
            return 'Неверный формат данных'
    result = ''
    data = int(data)
    target = int(target)
    if target < -10:
        return "Основание СС должно быть больше -10"
    while data != 0:
        remainder = data % target
        data = data // target
        if remainder < 0:
            remainder += abs(target)
            data += 1
        result = str(remainder) + result
    return result


def convert_from_negative(data, source):
    valid_symbols = []
    for i in range(abs(int(source))):
        valid_symbols.append(str(i))
    for ch in data:
        if ch not in valid_symbols:
            return 'Неверный формат данных'
    for ch in source:
        if ch not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-'}:
            return 'Неверный формат данных'
    if int(source) < -10:
        return "Основание СС должно быть больше -10"
    result = 0
    power = len(data) - 1
    for digit in data:
        result += int(digit) * (int(source) ** power)
        power -= 1
    return result


def convert_to_symmetric(data, target):
    for ch in data:
        if ch not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-'}:
            return 'Неверный формат данных'
    data = int(data)
    if data < 0:
        negative = 1
    else:
        negative = 0
    data = abs(data)
    target = int(target)
    if target > 20:
        return "Основание СС должно быть меньше 20"
    result = ''
    mod = ''
    for i in range(target // 2 + 1):
        mod += str(i)
    mod += mod[::-1]
    while data > 0:
        result += mod[data % target]
        if data % target <= target // 2:
            data = data // target
        else:
            result += "'"
            data = data // target + 1
    result_1 = ''
    if negative == 1:
        for i in range(len(result)):
            if i < (len(result) - 1):
                if result[i] != "'":
                    result_1 += result[i]
                    if result[i+1] != "'":
                        result_1 += "'"
            else:
                if result[i] != "'":
                    result_1 = result_1 + result[i] + "'"
        result = result_1
    result = result[::-1]
    return result


def convert_from_symmetric(data, source):
    valid_symbols = ["'", "‘"]
    for i in range(-int(source) // 2 + 1, int(source) // 2 + 1):
        valid_symbols.append(str(i))
    for ch in data:
        if ch not in valid_symbols:
            return 'Неверный формат данных'
    if data[-1] == "'" or data[-1] == "‘":
        return 'Апостроф ставится перед числом'
    if int(source) > 20:
        return "Основание СС должно быть меньше 20"
    data = data[::-1]
    result = 0
    power = 0
    for i in range(len(data)):
        if data[i] != "'" and data[i] != "‘":
            if i < len(data) - 1:
                if data[i+1] == "'" or data[i+1] == "‘":
                    result -= int(data[i]) * int(source) ** power
                else:
                    result += int(data[i]) * int(source) ** power
            else:
                result += int(data[i]) * int(source) ** power
            power += 1
    return str(result)


@bot.message_handler(commands=['to'])
def convert_to(message):
    msg = message.text.split()
    if len(msg) < 3:
        resp = 'Недостаточно данных'
    elif len(msg) > 3:
        resp = 'Слишком много данных'
    else:
        _, target, data = msg
        target = target.lower()
        if target == 'berg':
            resp = convert_to_bergman(data)
        elif target == 'zecken':
            resp = convert_to_zeckendorf(data)
        elif target == 'fact':
            resp = convert_to_factorial(data)
        elif '-' in target:
            resp = convert_to_negative(data, target)
        elif target[-1] in {'c', 'с'}:  
            target = target[:-1]
            for ch in target:
                if ch not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    resp = 'Неверный формат данных'
                    break
            if int(target) % 2 == 0:
                resp = 'Симметричные СС определены только для нечётных оснований!'
            else:
                resp = convert_to_symmetric(data, target)
        else:
            resp = 'Данная СС недоступна'

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['from'])
def convert_from(message):
    msg = message.text.split()
    if len(msg) < 3:
        resp = 'Недостаточно данных'
    elif len(msg) > 3:
        resp = 'Слишком много данных'
    else:
        _, source, data = msg
        source = source.lower()
        if source == 'berg':
            resp = convert_from_bergman(data)
        elif source == 'zecken':
            resp = convert_from_zeckendorf(data)
        elif source == 'fact':
            resp = convert_from_factorial(data)
        elif '-' in source:
            resp = convert_from_negative(data, source)
        elif source[-1] in {'c', 'с'}: 
            source = source[:-1]
            for ch in source:
                if ch not in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    resp = 'Неверный формат данных'
                    break
            if int(source) % 2 == 0:
                resp = 'Симметричные СС определены только для нечётных оснований!'
            else:
                resp = convert_from_symmetric(data, source)
        else:
            resp = 'Данная СС недоступна'

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['help'])
def help(message):
    resp = "Если у вас возникли проблемы с чат-ботом, пожалуйста, сообщите нам об этом:\nreshatel-itmo@yandex.ru"
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(content_types=['text'])
def info(message):
    resp = "<b>Вот что я могу:</b>\n/to target data - перевод в нетрадиционную СС\n/from" + \
    " source data - перевод из нетрадиционной СС\n\ntarget - результирующая СС\nsourсe - исходная СС\ndata - исходное число" + \
    " СС\n\n<b>Доступные СС:</b>\nberg - Бергмана\nzecken - Цекендорфа\nfact -" + \
    " факториальная\n-n - n-ая нега-позиционная\nnC - n-ая симметричная (для обозначения отрицательного числа перед ним ставится апостроф)\nn - основание СС\n\n<b>Пример:</b>\n/to berg 5 - перевод числа 5 в СС Бергмана\n/from 5c '12'1 - перевод числа '12'1 из симметричной СС с основанием 5\n/to -7 5 - перевод числа 5 в СС с основанием -7"
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
