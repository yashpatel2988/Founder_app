import re

def extract_user_id(user_id):
        if user_id:
            numbers = re.findall(r'\d+', user_id)
            try:
                return int(''.join(numbers))
            except ValueError:
                pass
        return None
