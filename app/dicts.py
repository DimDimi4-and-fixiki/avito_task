
# Dictionary to translate russian letters to english


class LanguageParser(object):
    def __init__(self):
        self.rus_to_eng = {
            'а': 'a',
            'б': 'b',
            'в': 'v',
            'г': 'g',
            'д': 'd',
            'е': 'e',
            'ё': 'e',
            'ж': 'zh',
            'з': 'z',
            'и': 'i',
            'й': 'i',
            'к': 'k',
            'л': 'l',
            'м': 'm',
            'н': 'n',
            'о': 'o',
            'п': 'p',
            'р': 'r',
            'с': 's',
            'т': 't',
            'у': 'u',
            'ф': 'f',
            'х': 'h',
            'ц': 'c',
            'ч': 'ch',
            'ш': 'sh',
            'щ': 'scz',
            'ъ': '',
            'ы': 'y',
            'ь': 'b',
            'э': 'e',
            'ю': 'u',
            'я': 'ya',
            'А': 'A',
            'Б': 'B',
            'В': 'V',
            'Г': 'G',
            'Д': 'D',
            'Е': 'E',
            'Ё': 'E',
            'Ж': 'ZH',
            'З': 'Z',
            'И': 'I',
            'Й': 'I',
            'К': 'K',
            'Л': 'L',
            'М': 'M',
            'Н': 'N',
            'О': 'O',
            'П': 'P',
            'Р': 'R',
            'С': 'S',
            'Т': 'T',
            'У': 'U',
            'Ф': 'F',
            'Х': 'H',
            'Ц': 'C',
            'Ч': 'CH',
            'Ш': 'SH',
            'Щ': 'SCH',
            'Ъ': '',
            'Ы': 'y',
            'Ь': 'b',
            'Э': 'E',
            'Ю': 'U',
            'Я': 'YA',
            ',': ',',
            '?': '?',
            ' ': '_',

        }

    def convert(self, s: str) -> str:
        for key in self.rus_to_eng:
            s = s.replace(key, self.rus_to_eng[key])
        return s