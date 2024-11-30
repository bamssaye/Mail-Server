import json,time,logging,re,string,secrets,uuid,random
import utils as ut
from email.header import Header 

#//////////////////////////////// class EmailHeaderManager
class EmailHeaderManager:
    def __init__(self, headers_file='info/header.json'):
        self.headers_file = headers_file
        self.headers_template = self._load_headers()
        self.generator = RandomGenerator() 
    def _load_headers(self):
        try:
            with open(self.headers_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load headers file: {e}")
            return {"headers": {}, "dkim_headers": []}
    def add_headers_to_message(self, msg):
        msg = ut.set_content_encode(msg)
        headers_items = list(self.headers_template['headers'].items())
        random.shuffle(headers_items)
        for header, value in headers_items:
            value = ut.replace_placeholders_in_text(value)
            if header in ['Content-Type', 'MIME-Version'] and header in msg:
                del msg[header]
            msg[header] = value
        return msg
    def get_dkim_headers(self):
        return [h.encode() for h in self.headers_template.get('dkim_headers', [])]

#//////////////////////////////// class RandomGenerator
class RandomGenerator:
    def __init__(self, PlaceHole='Msg/placehold.txt', fname='Msg/fname.txt', subject='Msg/subject.txt'):
        self.PlaceHole,self.fname, self.subject = PlaceHole, fname, subject
        self.patterns = {
            'N': string.digits,                    # Numbers
            'A': string.ascii_letters,             # Any letters
            'LA': string.ascii_lowercase,          # Lowercase
            'UA': string.ascii_uppercase,          # Uppercase
            'AN': string.ascii_letters + string.digits,  # Alphanumeri
            'FNAME':  str(Header(self.red_(self.fname)[:-1],'utf-8').encode()),
            'SUBJECT' :str(Header(self.red_(self.subject)[:-1],'utf-8').encode()),
            'DATE': time.strftime("%a, %d %b %Y %H:%M:%S.000 +0000 (UTC)", time.gmtime()),
            'TEXT': self.red_(self.PlaceHole),
            'EID': str(uuid.uuid4())
        }
        self.html_codes = {
            '’': '&#39;',
            '•': '&#8226;',
            '■': '&#9632;',
            '«': '&laquo;',
            'à': '&agrave;',
            'è': '&egrave;',
            'é': '&eacute;',
            'î': '&icirc;',
        }
        pattern_types = '|'.join(self.patterns.keys())
        self.pattern_regex = re.compile(f'\\[(?P<length>\\d+)?(?P<type>{pattern_types})\\]')
    def red_(self, file): return open(file, 'r').read()
    def generate_single(self, pattern: str) -> str:
        try:
            match = self.pattern_regex.match(pattern)
            if not match: return pattern
            type_code = match.group('type')
            length_str = match.group('length')
            length = int(length_str) if length_str else 0
            charset = self.patterns.get(type_code)
            if not length: return charset
            return ''.join(secrets.choice(charset) for _ in range(length))
        except:
            return pattern  
    def replace_hexcaracter(self, htmlcontent):
        try:
            converted = htmlcontent
            for char, code in self.html_codes.items():
                converted = converted.replace(char, code)
            return converted
        except Exception as e:
            print(f"An error occurred: {str(e)}")    
    
