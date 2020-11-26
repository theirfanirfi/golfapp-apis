from golfrica_app.Models.models import Country, CountrySchema
from datetime import datetime
from golfrica_app.Models.models import Country
from golfrica_app import db

class CountryBL:
    cs = CountrySchema(many=True)

    def getCountries(self):
        countries= Country.query.all()
        return self.cs.dump(countries)

    def getCountryById(self, id):
        country = Country.query.filter_by(country_id=id)
        if country.count() > 0:
            self.cs.many = False
            return self.cs.dump(country.first())
        return False

    def getCountryByName(self, name):
        country = Country.query.filter_by(country_name=name)
        if country.count() > 0:
            self.cs.many = False
            return self.cs.dump(country.first())
        return False

    def addCountry(self, form):
        country_name = form['country_name']
        country = Country.query.filter_by(country_name=country_name)
        if country.count() > 0:
            return False, 'Country already exists'
        country = Country()

        country.country_name = country_name
        country.created_at = str(datetime.now())
        country.updated_at = str(datetime.now())
        try:
            db.session.add(country)
            db.session.commit()
            self.cs.many=False
            return True, self.cs.dump(country)
        except Exception as ex:
            return False, str(ex)


