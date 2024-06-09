import cgi
import http.cookies
import os

def get_cookie_value(cookie, key):
    cookies = http.cookies.SimpleCookie(cookie)
    return cookies.get(key)

def set_cookie(key, value):
    cookie = http.cookies.SimpleCookie()
    cookie[key] = value
    print(cookie)

def delete_cookie(key):
    cookie = http.cookies.SimpleCookie()
    cookie[key] = ""
    cookie[key]['expires'] = 0
    print(cookie)

cookie_string = os.environ.get('HTTP_COOKIE', '')
form_counter_cookie = get_cookie_value(cookie_string, 'form_counter')

form_counter = int(form_counter_cookie.value) if form_counter_cookie else 0
form_counter += 1

set_cookie('form_counter', form_counter)
print("Content-type: text/html\n")

form = cgi.FieldStorage()
name = form.getvalue("name")
gender = form.getvalue("gender")
favorite_music = form.getlist("game")
favorite_kind = form.getvalue("kind")

if form.getvalue('delete_cookies'):
    delete_cookie('form_counter')
    form_counter = 0

print("<html>")
print("<head>")
print("<title>Results</title>")
print("</head>")
print("<body>")
print("<h1>Results:</h1>")
print(f"<p>Name: {name}</p>")
print(f"<p>Gender: {gender} </p>")
print("<p>Favorite game: " + ", ".join(favorite_music) + "</p>")
print(f"<p>Favorite style of games: {favorite_kind} </p>")
print(f"<p>Forms filled out by user: {form_counter}</p>")
print("<form action='process_form.py' method='post'>")
print("<input type='submit' value='Delete Cookies' name='delete_cookies'>")
print("</form>")
print("</body>")
print("</html>")