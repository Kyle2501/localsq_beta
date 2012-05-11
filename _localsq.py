import cgi
import os
import urllib
import logging
import pywapi

from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from datetime import datetime, timedelta
from pytz import timezone
import pytz

# - run Pages

class IndexPage(webapp.RequestHandler):
    def get(self):
    	# - clock
    	mst = timezone('US/Mountain')
    	ms_time = datetime.now(mst)
    	clock = ms_time.strftime('%I:%M %p')
    	day = ms_time.strftime("%a")
    	Day = ms_time.strftime("%A")
    	date = ms_time.strftime('%d')
    	month = ms_time.strftime("%B")
    	# - weather
    	google_result = pywapi.get_weather_from_google('83353')
    	weather = google_result['current_conditions']['temp_f']
    	# - user
    	user = users.get_current_user()
    	if users.get_current_user():
    		gate = users.create_logout_url(self.request.uri)
    		door = 'Exit'
    		hello = user.nickname()
    	else:
    		gate = users.create_login_url(self.request.uri)
    		door = 'Enter'
    		hello = 'LocalSq'
            
        template_values = {
            'gate': gate,
            'door': door,
            'hello': hello,
            'clock': clock,
            'day': day,
            'date': date,
            'month': month,
            'weather': weather,
        }

        path = os.path.join(os.path.dirname(__file__), 'pages/index.html')
        self.response.out.write(template.render(path, template_values))

class AboutPage(webapp.RequestHandler):
    def get(self):
    	# - clock
    	mst = timezone('US/Mountain')
    	ms_time = datetime.now(mst)
    	clock = ms_time.strftime('%I:%M %p')
    	day = ms_time.strftime("%a")
    	Day = ms_time.strftime("%A")
    	date = ms_time.strftime('%d')
    	month = ms_time.strftime("%B")   	
    	# - weather
    	google_result = pywapi.get_weather_from_google('83353')
    	weather = google_result['current_conditions']['temp_f']
    	# - user
    	user = users.get_current_user()
    	if users.get_current_user():
    		gate = users.create_logout_url(self.request.uri)
    		door = 'Exit'
    		hello = user.nickname()
    	else:
    		gate = users.create_login_url(self.request.uri)
    		door = 'Enter'
    		hello = 'LocalSq'
            
        template_values = {
            'gate': gate,
            'door': door,
            'hello': hello,
            'clock': clock,
            'day': day,
            'date': date,
            'month': month,
            'weather': weather,
        }

        path = os.path.join(os.path.dirname(__file__), 'pages/about.html')
        self.response.out.write(template.render(path, template_values))

class SignUps(db.Model):
    addTime = db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty()
    spam_bot = db.StringProperty()
    name = db.StringProperty()
    contact = db.StringProperty()

def signupsbook_key(add_signup=None):
    return db.Key.from_path('SignUpsbook', add_signup or 'default_signupsbook')

class SignUp(webapp.RequestHandler):
    def post(self):
        # - database
        add_signup = self.request.get('add_signup')
        signup = SignUps(parent=signupsbook_key(add_signup))

        if users.get_current_user():
            signup.user = users.get_current_user()
        
        signup.name = self.request.get('name')
        signup.contact = self.request.get('contact')
        signup.spam_bot = self.request.get('spam_bot')
        signup.put()
        # - mail
        newsignup = mail.EmailMessage(sender = self.request.get('name') + "<system@elkhornlabs.com>",
                                    subject = 'joined localsq')
        newsignup.to = "Kyle <kyle2501@gmail.com>"
        newsignup.body = ' Name: ' + self.request.get('name') + ' Contact: ' + self.request.get('contact')
        newsignup.send()
       
        self.redirect('ticket')

class FeedbackPage(webapp.RequestHandler):
    def get(self):
    	# - clock
    	mst = timezone('US/Mountain')
    	ms_time = datetime.now(mst)
    	clock = ms_time.strftime('%I:%M %p')
    	day = ms_time.strftime("%a")
    	Day = ms_time.strftime("%A")
    	date = ms_time.strftime('%d')
    	month = ms_time.strftime("%B")    	
    	# - weather
    	google_result = pywapi.get_weather_from_google('83353')
    	weather = google_result['current_conditions']['temp_f']    	
    	# - user
    	user = users.get_current_user()
    	if users.get_current_user():
    		gate = users.create_logout_url(self.request.uri)
    		door = 'Exit'
    		hello = user.nickname()
    	else:
    		gate = users.create_login_url(self.request.uri)
    		door = 'Enter'
    		hello = 'LocalSq'
            
        template_values = {
            'gate': gate,
            'door': door,
            'hello': hello,
            'clock': clock,
            'day': day,
            'date': date,
            'month': month,
            'weather': weather,
        }

        path = os.path.join(os.path.dirname(__file__), 'apps/feedback.html')
        self.response.out.write(template.render(path, template_values))

class Feedback(db.Model):
    addTime = db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty()
    spam_bot = db.StringProperty()
    name = db.StringProperty()
    contact = db.StringProperty()
    feedback = db.StringProperty()

def feedbackbook_key(add_feedback=None):
    return db.Key.from_path('Feedbackbook', add_feedback or 'default_feedbackbook')

class addFeedback(webapp.RequestHandler):
    def post(self):
        # - database
        add_feedback = self.request.get('add_feedback')
        feedback = Feedback(parent=feedbackbook_key(add_feedback))
        if users.get_current_user():
            feedback.user = users.get_current_user()
        feedback.name = self.request.get('name')
        feedback.contact = self.request.get('contact')
        feedback.feedback = self.request.get('feedback')
        feedback.spam_bot = self.request.get('spam_bot')
        feedback.put()
        # - mail
        feedback = mail.EmailMessage()
        feedback.to = "Kyle <kyle2501@gmail.com>"
        feedback.subject = 'LocalSq Feedback'
        feedback.sender = self.request.get('name') + "<system@elkhornlabs.com>"
        feedback.body = ' Name: ' + self.request.get('name') + ' Contact: ' + self.request.get('contact') + ' Feedback: ' + self.request.get('feedback')
        feedback.send()
        self.redirect('/')
       
class DirectoryPage(webapp.RequestHandler):
    def get(self):
    	# - clock
    	mst = timezone('US/Mountain')
    	ms_time = datetime.now(mst)
    	clock = ms_time.strftime('%I:%M %p')
    	day = ms_time.strftime("%a")
    	Day = ms_time.strftime("%A")
    	date = ms_time.strftime('%d')
    	month = ms_time.strftime("%B")    	
    	# - weather
    	google_result = pywapi.get_weather_from_google('83353')
    	weather = google_result['current_conditions']['temp_f']
    	# - user
    	user = users.get_current_user()
    	if users.get_current_user():
    		gate = users.create_logout_url(self.request.uri)
    		door = 'Exit'
    		hello = user.nickname()
    	else:
    		gate = users.create_login_url(self.request.uri)
    		door = 'Enter'
    		hello = 'LocalSq'
            
        template_values = {
            'gate': gate,
            'door': door,
            'hello': hello,
            'clock': clock,
            'day': day,
            'date': date,
            'month': month,
            'weather': weather,
        }

        path = os.path.join(os.path.dirname(__file__), 'pages/directory.html')
        self.response.out.write(template.render(path, template_values))


class MarketPage(webapp.RequestHandler):
    def get(self):
    	# - clock
    	mst = timezone('US/Mountain')
    	ms_time = datetime.now(mst)
    	clock = ms_time.strftime('%I:%M %p')
    	day = ms_time.strftime("%a")
    	Day = ms_time.strftime("%A")
    	date = ms_time.strftime('%d')
    	month = ms_time.strftime("%B")    	
    	# - weather
    	google_result = pywapi.get_weather_from_google('83353')
    	weather = google_result['current_conditions']['temp_f']
    	# - user
    	user = users.get_current_user()
    	if users.get_current_user():
    		gate = users.create_logout_url(self.request.uri)
    		door = 'Exit'
    		hello = user.nickname()
    	else:
    		gate = users.create_login_url(self.request.uri)
    		door = 'Enter'
    		hello = 'LocalSq'
            
        template_values = {
            'gate': gate,
            'door': door,
            'hello': hello,
            'clock': clock,
            'day': day,
            'date': date,
            'month': month,
            'weather': weather,
        }

        path = os.path.join(os.path.dirname(__file__), 'pages/market.html')
        self.response.out.write(template.render(path, template_values)) 

class TicketPage(webapp.RequestHandler):
    def get(self):
    	# - clock
    	mst = timezone('US/Mountain')
    	ms_time = datetime.now(mst)
    	time = ms_time.strftime('%I:%M %p')
    	day = ms_time.strftime("%a")
    	Day = ms_time.strftime("%A")
    	date = ms_time.strftime('%d')
    	month = ms_time.strftime("%B")    	
    	# - weather
    	google_result = pywapi.get_weather_from_google('83353')
    	weather = google_result['current_conditions']['temp_f']
    	# - user
    	user = users.get_current_user()
    	if users.get_current_user():
    		gate = users.create_logout_url(self.request.uri)
    		door = 'Exit'
    		hello = user.nickname()
    	else:
    		gate = users.create_login_url(self.request.uri)
    		door = 'Enter'
    		hello = 'LocalSq'
            
        template_values = {
            'gate': gate,
            'door': door,
            'hello': hello,
            'time': time,
            'day': day,
            'date': date,
            'month': month,
            'weather': weather,
        }

        path = os.path.join(os.path.dirname(__file__), 'pages/tickets/summer_season.html')
        self.response.out.write(template.render(path, template_values)) 

# - Pages fin

# - run Apps

class WeatherApp(webapp.RequestHandler):
    def get(self):
    	# - clock
    	mst = timezone('US/Mountain')
    	ms_time = datetime.now(mst)
    	clock = ms_time.strftime('%I:%M %p')
    	day = ms_time.strftime("%a")
    	Day = ms_time.strftime("%A")
    	date = ms_time.strftime('%d')
    	month = ms_time.strftime("%B")    	
    	# - weather
    	google_result = pywapi.get_weather_from_google('83353')
    	weather = google_result['current_conditions']['temp_f']
    	# - user
    	user = users.get_current_user()
    	if users.get_current_user():
    		gate = users.create_logout_url(self.request.uri)
    		door = 'Exit'
    		hello = user.nickname()
    	else:
    		gate = users.create_login_url(self.request.uri)
    		door = 'Enter'
    		hello = 'LocalSq'
        # - data
        name = 'localsq'     
        
        template_values = {
            'gate': gate,
            'door': door,
            'hello': hello,
            'clock': clock,
            'day': day,
            'date': date,
            'month': month,
            'weather': weather,
            'name': name,
        }

        path = os.path.join(os.path.dirname(__file__), 'apps/weather.html')
        self.response.out.write(template.render(path, template_values))


class Event(db.Model):
    addTime = db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty()
    spam_bot = db.StringProperty()
    mute = db.StringProperty()
    trash = db.StringProperty()
    flag = db.StringProperty()
    rsvp = db.StringProperty()
    what = db.StringProperty()
    when = db.StringProperty()
    where = db.StringProperty()

def eventbook_key(add_event=None):
    return db.Key.from_path('Eventbook', add_event or 'default_eventbook')

class addEvent(webapp.RequestHandler):
    def post(self):
        add_event = self.request.get('add_event')
        event = Event(parent=eventbook_key(add_event))

        if users.get_current_user():
            event.user = users.get_current_user()
        
        event.what = self.request.get('what')
        event.when = self.request.get('when')
        event.where = self.request.get('where')
        event.spam_bot = self.request.get('spam_bot')
        event.put()
        self.redirect('events')

class EventsApp(webapp.RequestHandler):
    def get(self):
    	# - database
    	add_event = self.request.get('add_event')
    	events_query = Event.all().ancestor(
    	    eventbook_key(add_event)).order('-addTime')
    	events = events_query.fetch(100)
    	# - clock
    	mst = timezone('US/Mountain')
    	ms_time = datetime.now(mst)
    	clock = ms_time.strftime('%I:%M %p')
    	day = ms_time.strftime("%a")
    	Day = ms_time.strftime("%A")
    	date = ms_time.strftime('%d')
    	month = ms_time.strftime("%B")
    	# - weather
    	google_result = pywapi.get_weather_from_google('83353')
    	weather = google_result['current_conditions']['temp_f']
    	# - user
    	user = users.get_current_user()
    	if users.get_current_user():
    		gate = users.create_logout_url(self.request.uri)
    		door = 'Exit'
    		hello = user.nickname()
    	else:
    		gate = users.create_login_url(self.request.uri)
    		door = 'Enter'
    		hello = 'LocalSq'
    		
        template_values = {
            'gate': gate,
            'door': door,
            'hello': hello,
            'clock': clock,
            'day': day,
            'date': date,
            'month': month,
            'weather': weather,
            'events': events,
        }

        path = os.path.join(os.path.dirname(__file__), 'apps/events.html')
        self.response.out.write(template.render(path, template_values))


class MapApp(webapp.RequestHandler):
    def get(self):
    	# - clock
    	mst = timezone('US/Mountain')
    	ms_time = datetime.now(mst)
    	clock = ms_time.strftime('%I:%M %p')
    	day = ms_time.strftime("%a")
    	Day = ms_time.strftime("%A")
    	date = ms_time.strftime('%d')
    	month = ms_time.strftime("%B")
    	# - weather
    	google_result = pywapi.get_weather_from_google('83353')
    	weather = google_result['current_conditions']['temp_f']
    	# - user
    	user = users.get_current_user()
    	if users.get_current_user():
    		gate = users.create_logout_url(self.request.uri)
    		door = 'Exit'
    		hello = user.nickname()
    	else:
    		gate = users.create_login_url(self.request.uri)
    		door = 'Enter'
    		hello = 'LocalSq'

        template_values = {
            'gate': gate,
            'door': door,
            'hello': hello,
            'clock': clock,
            'day': day,
            'date': date,
            'month': month,
            'weather': weather,
        }

        path = os.path.join(os.path.dirname(__file__), 'apps/map.html')
        self.response.out.write(template.render(path, template_values))          


class MessageApp(webapp.RequestHandler):
    def get(self):
    	# - clock
    	mst = timezone('US/Mountain')
    	ms_time = datetime.now(mst)
    	clock = ms_time.strftime('%I:%M %p')
    	day = ms_time.strftime("%a")
    	Day = ms_time.strftime("%A")
    	date = ms_time.strftime('%d')
    	month = ms_time.strftime("%B")    	
    	# - weather
    	google_result = pywapi.get_weather_from_google('83353')
    	weather = google_result['current_conditions']['temp_f']
    	# - user
    	user = users.get_current_user()
    	if users.get_current_user():
    		gate = users.create_logout_url(self.request.uri)
    		door = 'Exit'
    		hello = user.nickname()
    	else:
    		gate = users.create_login_url(self.request.uri)
    		door = 'Enter'
    		hello = 'LocalSq'
        # - data
        name = 'localsq'     
        
        template_values = {
            'gate': gate,
            'door': door,
            'hello': hello,
            'clock': clock,
            'day': day,
            'date': date,
            'month': month,
            'weather': weather,
            'name': name,
        }

        path = os.path.join(os.path.dirname(__file__), 'apps/message.html')
        self.response.out.write(template.render(path, template_values))


class SendMessage(webapp.RequestHandler):
	def post(self):
		# - mail
		message = mail.EmailMessage()
		message.to = self.request.get('to')
		message.subject = 'message via localsq'
		message.sender = self.request.get('name') + "<hello@elkhornlabs.com>"
		message.body = self.request.get('message') + ' -- This message was sent from: ' + self.request.get('name') + ' using http://beta.localsq.us/message' + ' and can be contacted at this address < ' + self.request.get('contact') + ' >'
		message.send()
		self.redirect('message')




application = webapp.WSGIApplication(

                                     [('/', IndexPage),
                                      ('/home/?', IndexPage),
                                      ('/about/?', AboutPage),
                                      ('/directory/?', DirectoryPage),
                                      ('/market/?', MarketPage),
                                      ('/signup/?', SignUp),
                                      ('/feedback/?', FeedbackPage),
                                      ('/addfeedback/?', addFeedback),
                                      ('/map/?', MapApp),
                                      ('/events/?', EventsApp),
                                      ('/addevent/?', addEvent),
                                      ('/weather/?', WeatherApp),
                                      ('/message/?', MessageApp),
                                      ('/sendmessage/?', SendMessage),
                                      ('/ticket/?', TicketPage),

                                                               
                                      ], debug=True)



def main():

  run_wsgi_app(application)

if __name__ == "__main__":

  main()

