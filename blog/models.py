from django.db import models

class Medals(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    medalname = models.CharField(db_column='MedalName', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'medals'


class City(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'city'


class Country(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    country_team = models.CharField(db_column='Country_Team', max_length=255)  # Field name made lowercase.
    noc = models.CharField(db_column='NOC', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'country'


class Events(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    events = models.CharField(db_column='Events', max_length=255)  # Field name made lowercase.
    sport = models.ForeignKey('Sport', models.DO_NOTHING, db_column='Sport', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'events'


class Games(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.
    season = models.CharField(db_column='Season', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'games'


class GamesCity(models.Model):
    game = models.OneToOneField(Games, models.DO_NOTHING, db_column='Game_ID', primary_key=True)  # Field name made lowercase.
    city = models.ForeignKey(City, models.DO_NOTHING, db_column='City_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'games_city'
        unique_together = (('game', 'city'),)



class OlympicEvent(models.Model):
    olympics = models.OneToOneField('Olympics', models.DO_NOTHING, db_column='Olympics_ID', primary_key=True)  # Field name made lowercase.
    medal = models.ForeignKey(Medals, models.DO_NOTHING, db_column='Medal_ID')  # Field name made lowercase.
    event = models.ForeignKey(Events, models.DO_NOTHING, db_column='Event_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'olympic_event'
        unique_together = (('olympics', 'medal', 'event'),)


class Olympics(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    age = models.IntegerField(db_column='Age', blank=True, null=True)  # Field name made lowercase.
    game = models.ForeignKey(Games, models.DO_NOTHING, db_column='Game_Id', blank=True, null=True)  # Field name made lowercase.
    player = models.ForeignKey('Person', models.DO_NOTHING, blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING, db_column='Country_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'olympics'


class Person(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=5)  # Field name made lowercase.
    height = models.CharField(db_column='Height', max_length=10, blank=True, null=True)  # Field name made lowercase.
    weight = models.CharField(db_column='Weight', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'person'


class PersonCountry(models.Model):
    country = models.OneToOneField(Country, models.DO_NOTHING, db_column='Country_ID', primary_key=True)  # Field name made lowercase.
    person = models.ForeignKey(Person, models.DO_NOTHING, db_column='Person_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'person_country'
        unique_together = (('country', 'person'),)


class Sport(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=255)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sport'
