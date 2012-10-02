import datetime, re

from lxml import etree, html

PATTERN_DATE_EN = re.compile(r'(\w+)\s+(\d+),\s+(\d+)$')
PATTERN_DATE_SI = re.compile(r'(\d+).\s+(\w+):\s+$')

def get_horoscope_sign(day, month):
    """
    Based on date, returns horoscope sign key.
    """

    if month == 3:
        if day > 20:
            return 'aries'
        else:
            return 'pisces'
    elif month == 4:
        if day > 20:
            return 'taurus'
        else:
            return 'aries'
    elif month == 5:
        if day > 21:
            return 'gemini'
        else:
            return 'taurus'
    elif month == 6:
        if day > 21:
            return 'cancer'
        else:
            return 'gemini'
    elif month == 7:
        if day > 23:
            return 'leo'
        else:
            return 'cancer'
    elif month == 8:
        if day > 23:
            return 'virgo'
        else:
            return 'leo'
    elif month == 9:
        if day > 23:
            return 'libra'
        else:
            return 'virgo'
    elif month == 10:
        if day > 23:
            return 'scorpio'
        else:
            return 'libra'
    elif month == 11:
        if day > 22:
            return 'sagittarius'
        else:
            return 'scorpio'
    elif month == 12:
        if day > 22:
            return 'capricorn'
        else:
            return 'sagittarius'
    elif month == 1:
        if day < 20:
            return 'aquarius'
        else:
            return 'capricorn'
    elif month == 2:
        if day > 19:
            return 'pisces'
        else:
            return 'aquarius'

def get_all_providers():
    """
    Returns all available horoscope providers.
    """

    return HOROSCOPE_PROVIDERS

def get_provider(language):
    """
    Returns an instance of the horoscope provider for requested language, or raises ``KeyError`` if it does not exist.
    """

    for horoscope in get_all_providers():
        if horoscope.get_language() == language:
            return horoscope

    raise KeyError("Unsupported language: '%s'" % language)

def get_supported_languages():
    """
    Returns a list of supported languages (their language codes).

    That is, a list of languages provided by defined horoscope providers.
    """

    languages = []
    for horoscope in get_all_providers():
        language = horoscope.get_language()
        assert language not in languages, language
        languages.append(language)
    return languages

class HoroscopeProviderBase(object):
    """
    Base class for horoscope providers.
    """

    language = None
    source_name = None
    source_url = None

    def get_language(self):
        """
        Returns provider's language.
        """

        return self.language

    def get_source_name(self):
        """
        Returns provider's source name.
        """

        return self.source_name

    def get_source_url(self):
        """
        Returns provider's source URL.
        """

        return self.source_url

    def fetch_data(self, sign):
        return NotImplementedError

class EnglishHoroscope(HoroscopeProviderBase):
    """
    Daily English horoscope from http://findyourfate.com/.
    """

    language = 'en'
    source_name = 'Find your fate'
    source_url = 'http://findyourfate.com/'

    provider_sign_names = {
        'aries': 'Aries',
        'pisces': 'Pisces',
        'taurus': 'Taurus',
        'gemini': 'Gemini',
        'cancer': 'Cancer',
        'leo': 'Leo',
        'virgo': 'Virgo',
        'libra': 'Libra',
        'scorpio': 'Scorpio',
        'sagittarius': 'Sagittarius',
        'capricorn': 'Capricorn',
        'aquarius': 'Aquarius',
    }
    
    provider_month_names = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12,
    }

    def fetch_data(self, sign):
        horoscope_url = '%srss/dailyhoroscope-feed.asp?sign=%s' % (self.source_url, self.provider_sign_names[sign])
        horoscope_tree = etree.parse(horoscope_url)

        date_string = PATTERN_DATE_EN.search(horoscope_tree.findtext('.//item/title'))

        return {
            # TODO: date should be stored in correct timezone (currently it is in UTC which probably is not correct)
            'date': datetime.date(int(date_string.group(3)), self.provider_month_names[date_string.group(1)], int(date_string.group(2))),
            'forecast': horoscope_tree.findtext('.//item/description'),
        }

class SlovenianHoroscope(HoroscopeProviderBase):
    """
    Daily Slovenian horoscope from http://slovenskenovice.si/.
    """

    language = 'sl'
    source_name = 'Slovenske novice'
    source_url = 'http://www.slovenskenovice.si/'

    provider_sign_names = {
        'aries': 'oven',
        'pisces': 'ribi',
        'taurus': 'bik',
        'gemini': 'dvojcka',
        'cancer': 'rak',
        'leo': 'lev',
        'virgo': 'devica',
        'libra': 'tehtnica',
        'scorpio': 'skorpijon',
        'sagittarius': 'strelec',
        'capricorn': 'kozorog',
        'aquarius': 'vodnar',
    }

    provider_month_names = {
        'januar': 1,
        'februar': 2,
        'marec': 3,
        'april': 4,
        'maj': 5,
        'junij': 6,
        'julij': 7,
        'avgust': 8,
        'september': 9,
        'oktober': 10,
        'november': 11,
        'december': 12,
    }

    def fetch_data(self, sign):
        horoscope_url = '%slifestyle/astro/%s' % (self.source_url, self.provider_sign_names[sign])
        html_parser = html.HTMLParser(encoding='utf-8')
        horoscope_tree = html.parse(horoscope_url, html_parser)

        date_parsed = PATTERN_DATE_SI.search(horoscope_tree.findtext('.//div[@id="horoscope-sign-right"]//div[@class="view-content"]//span'))

        return {
            # TODO: .year could be the wrong value around new year
            # TODO: date should be stored in correct timezone (currently it is in UTC which probably is not correct)
            'date': datetime.date(datetime.datetime.now().year, self.provider_month_names[date_parsed.group(2)], int(date_parsed.group(1))),
            'forecast': horoscope_tree.findtext('.//div[@id="horoscope-sign-right"]//div[@class="view-content"]//strong'),
        }

HOROSCOPE_PROVIDERS = (
    EnglishHoroscope(),
    SlovenianHoroscope(),
)
