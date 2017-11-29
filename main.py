#!/usr/bin/env python
import os
import random

import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class Capital:
    def __init__(self, capital, country, image, link):
        self.capital = capital
        self.country = country
        self.image = image
        self.link = link


def setup_data():

    par = Capital(capital="Paris", country="France", image="/assets/img/par.jpeg", link="https://de.wikipedia.org/wiki/Paris")
    mad = Capital(capital="Madrid", country="Spain", image="/assets/img/mad.jpg", link="https://de.wikipedia.org/wiki/Madrid")
    lon = Capital(capital="London", country="Great Britain", image="/assets/img/lon.jpeg", link="https://de.wikipedia.org/wiki/London")
    lbj = Capital(capital="Ljubljana", country="Slovenia", image="/assets/img/lbj.jpg", link="https://de.wikipedia.org/wiki/Ljubljana")
    bel = Capital(capital="Berlin", country="Germany", image="/assets/img/bel.jpeg", link="https://de.wikipedia.org/wiki/Berlin")
    zag = Capital(capital="Zagreb", country="Croatia", image="/assets/img/zag.jpg", link="https://de.wikipedia.org/wiki/Zagreb")
    vie = Capital(capital="Vienna", country="Austria", image="/assets/img/vie.jpg", link="https://de.wikipedia.org/wiki/Vienna")
    rom = Capital(capital="Rome", country="Italy", image="/assets/img/rom.jpeg", link="https://de.wikipedia.org/wiki/Rome")
    ber = Capital(capital="Bern", country="Switzerland", image="/assets/img/ber.jpg", link="https://de.wikipedia.org/wiki/Bern")


    return [lbj, bel, zag, vie, rom, ber, par, mad, lon]


class MainHandler(BaseHandler):
    def get(self):
        capital = setup_data()[random.randint(0, 8)]  # get random capital from the list

        params = {"capital": capital}

        return self.render_template("capital.html", params=params)


class ResultHandler(BaseHandler):
    def post(self):
        answer = self.request.get("guess")
        country = self.request.get("country")

        capitals = setup_data()
        for item in capitals:
            if item.country == country:
                if item.capital.lower() == answer.lower():
                    result = True
                else:
                    result = False

                params = {"result": result, "item": item}

                return self.render_template("result.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/result', ResultHandler),
], debug=True)