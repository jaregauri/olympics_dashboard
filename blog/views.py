from django.shortcuts import render
from django.http import HttpResponse


from .models import Medals, City, Country, Events, Games, GamesCity, OlympicEvent, Olympics, Person, PersonCountry, Sport
from django.db import connection
# Create your views here.

posts = [
    {
        'author': 'john',
        'title': 'first post',
        'content': 'fdjf',
        'date_posted' :'Augusthdksj'
    },

    {
        'author': 'alicia',
        'title': 'second post',
        'content': 'fdjf',
        'date_posted' :'Augusthdksj'
    }
]

# -- query 1-- 
# -- male female participation sport wise over the years
# select final_table.sportName, final_table.year, count(if(final_table.gender = 'M', 1, null)) as male, count(if(final_table.gender = 'F', 1, null)) as female, count(if(final_table.gender != 'F' and final_table.gender !='M', 1, null)) as error from 
# (
# 	select oly_per_olyeve_eve_game.gender, (select year from games g where oly_per_olyeve_eve_game.game_id = g.ID) as year,  (select s.Name from sport s where s.ID = oly_per_olyeve_eve_game.sport) as sportName from 	
# 		(
# 			select oly_per_olyeve.Olympics_ID, oly_per_olyeve.event_id, oly_per_olyeve.player_id, oly_per_olyeve.game_id, oly_per_olyeve.gender, e.sport from events e join
# 			(
# 				select oe.Olympics_ID, oe.event_id, op.player_id, op.game_id, op.gender from olympic_event oe join 
# 				(
# 				select o.id as oid, p.id as player_id, o.game_id as game_id, p.gender as gender from Olympics o join person p on o.player_id = p.id 
# 				) as op on oe.olympics_id = op.oid
# 			) as oly_per_olyeve on oly_per_olyeve.event_id = e.id
# 		) as oly_per_olyeve_eve_game
# ) as final_table group by final_table.sportName, final_table.year having final_table.year = 2016 and final_table.sportName = 'Wrestling';



def home(request):
    cursor = connection.cursor()
    
    # cursor.execute("select * from medals, city")

    cursor.execute("select final_table.sportName, final_table.year, count(if(final_table.gender = 'M', 1, null)) as male, count(if(final_table.gender = 'F', 1, null)) as female, count(if(final_table.gender != 'F' and final_table.gender !='M', 1, null)) as error from (select oly_per_olyeve_eve_game.gender, (select year from games g where oly_per_olyeve_eve_game.game_id = g.ID) as year,  (select s.Name from sport s where s.ID = oly_per_olyeve_eve_game.sport) as sportName from" +
	"(select oly_per_olyeve.Olympics_ID, oly_per_olyeve.event_id, oly_per_olyeve.player_id, oly_per_olyeve.game_id, oly_per_olyeve.gender, e.sport from events e join"+
			"(select oe.Olympics_ID, oe.event_id, op.player_id, op.game_id, op.gender from olympic_event oe join" +
				"(select o.id as oid, p.id as player_id, o.game_id as game_id, p.gender as gender from Olympics o join person p on o.player_id = p.id"+
				") as op on oe.olympics_id = op.oid"+
			") as oly_per_olyeve on oly_per_olyeve.event_id = e.id"+
		") as oly_per_olyeve_eve_game"+
") as final_table group by final_table.sportName, final_table.year having final_table.year = 2016 and final_table.sportName = 'Wrestling'")
    solution = cursor.fetchall()
    print(solution)
    medalss = Medals.objects.all()
    medals = Medals.objects.raw("SELECT * FROM medals")
    city = City.objects.raw("SELECT * FROM city")
    for i in medals:
        print(i.id, "   " , i.medalname)
    print("88888888888888888")

    for i in city:
        print(i.id, "   " , i.city)
    # print(medalss)
    # print(connection.queries)
    context = {
        'medals' :medals,
        'city' :city
    }
    
    # print(solution)

    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html')