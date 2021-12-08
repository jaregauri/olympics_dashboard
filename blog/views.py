from django.shortcuts import render
from django.http import HttpResponse
from json import dumps

import simplejson as json
from .models import Medals, City, Country, Events, Games, GamesCity, OlympicEvent, Olympics, Person, PersonCountry, Sport
from django.db import connection
# Create your views here.


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

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def home(request):
    year1 = 2016
    # if request.POST:
    # searchYear = request.POST.get('search','')
    # year = searchYear
    # print(searchYear)

    cursor = connection.cursor()
    sportName1 = 'Swimming'
    # year = 2016
    # if searchYear:
    #     year = searchYear

    # cursor.execute("select * from medals, city")

    cursor.execute("select final_table.sportName, final_table.year, count(if(final_table.gender = 'M', 1, null)) as male, count(if(final_table.gender = 'F', 1, null)) as female, count(if(final_table.gender != 'F' and final_table.gender !='M', 1, null)) as error from (select oly_per_olyeve_eve_game.gender, (select year from games g where oly_per_olyeve_eve_game.game_id = g.ID) as year,  (select s.Name from sport s where s.ID = oly_per_olyeve_eve_game.sport) as sportName from" +
	"(select oly_per_olyeve.Olympics_ID, oly_per_olyeve.event_id, oly_per_olyeve.player_id, oly_per_olyeve.game_id, oly_per_olyeve.gender, e.sport from events e join"+
			"(select oe.Olympics_ID, oe.event_id, op.player_id, op.game_id, op.gender from olympic_event oe join" +
				"(select o.id as oid, p.id as player_id, o.game_id as game_id, p.gender as gender from Olympics o join person p on o.player_id = p.id"+
				") as op on oe.olympics_id = op.oid"+
			") as oly_per_olyeve on oly_per_olyeve.event_id = e.id"+
		") as oly_per_olyeve_eve_game"+
") as final_table group by final_table.sportName, final_table.year having final_table.year = %s and final_table.sportName = %s", (year1, sportName1))
    
    
    # solution = cursor.fetchone()
    r = dictfetchall(cursor)
    # print(solution)
    print("********************")
    print(r)
    male_participation = r[0]['male']
    female_participation = r[0]['female']
    # medalss = Medals.objects.all()
    # cursor.execute("select distinct(name) from sport order by name")
    # sport_solution = dictfetchall(cursor)
    # print(sport_solution)

    # year = cursor.execute("select distinct(year) from games order by year asc")
    # year_solution = dictfetchall(cursor)
    # print(year_solution)
    
    # print(year)
    # city = City.objects.raw("SELECT * FROM city")
    # for i in sport:
    #     print(i)

    # for i in year:
    #     print(i)
   
    # for i in city:
    #     print(i.id, "   " , i.city)
    # print(medalss)
    # print(connection.queries)

    # query2

    country2 = 'USA'
    year2 = []
    total_count2 = []
    cursor.execute("select c.NOC, g.Year, sum(mix.count) as total_count from (select country_ID, Game_Id, count(*) as count from  olympics o Group BY country_ID,Game_Id) mix, country c, games g where mix.country_ID = c.ID and g.ID = mix.Game_Id GROUP BY c.NOC, g.Year HAVING NOC = %s ORDER BY Year", country2)
    r = dictfetchall(cursor)
    # print("88888888888888888")

    # print(r)

    for i in r:
        year2.append(i['Year'])
        # print(i['Year'])
        total_count2.append(i['total_count'])
        # print(i['total_count'])
  

    # query3
    NOC3 = 'IND'
    name3 = []
    medals_won3 = []
    cursor.execute("SELECT c.NOC, g.Name,  count(mix.Medal_ID) as Medals_Won from(Select Medal_ID, Country_ID, Game_ID from olympic_event oe, olympics o where oe.olympics_ID = o.ID) mix, country c, games g where mix.country_ID = c.ID and mix.Game_ID = g.ID GROUP BY c.NOC, g.Name HAVING NOC = %s ORDER BY Name", NOC3)
    r = dictfetchall(cursor)
    for i in r:
        name3.append(i['Name'])
        # print(i['Year'])
        medals_won3.append(i['Medals_Won'])
        # print(i['total_count'])

   
    # query4

    NOC4 = 'USA'
    year4 = 2016
    sport4 = 'Swimming'
    medal4 = []
    medals_won4 = []
    cursor.execute("select distinct(final_table.medal), final_table.year, final_table.noc, final_table.sportName, count(medal_id) over (partition by medal_id, year, noc, sportName) as cnt_medal from (select games_oly_noc_olyeve.medal_id, CASE WHEN games_oly_noc_olyeve.medal_id = 0 THEN %s WHEN games_oly_noc_olyeve.medal_id = 1 THEN %s WHEN games_oly_noc_olyeve.medal_id = 2 THEN %s END medal, games_oly_noc_olyeve.year, games_oly_noc_olyeve.noc, e.sport as sportID, (select s.name from sport s where s.id = e.sport) as sportName from events e join (select games_olympics_country.olympic_id as olympic_id, oe.medal_id as medal_id, oe.event_id as event_id, games_olympics_country.year as year,games_olympics_country.noc as noc from olympic_event oe join (select g.ID as game_id, g.year, o.id as olympic_id, o.country_id, (select noc from country c where c.ID = o.Country_ID) as NOC from games g join olympics o on o.game_id = g.id) as games_olympics_country on oe.olympics_ID = games_olympics_country.olympic_id) as games_oly_noc_olyeve on games_oly_noc_olyeve.event_id = e.id) as final_table having noc = %s and year = %s and sportName = %s", ('Gold', 'Silver', 'Bronze', NOC4, year4, sport4))
    r = dictfetchall(cursor)
    for i in r:
        medal4.append(i['medal'])
        # print(i['Year'])
        medals_won4.append(i['cnt_medal'])
        # print(i['total_count'])


    # query6

    NOC6 = 'USA'
    year6 = []
    medals_won6 = []
    cursor.execute("SELECT Year, count(country_ID) as total_medal From( SELECT DISTINCT g.Year, o.country_ID, Event_ID, medal_id from olympics o, olympic_event oe, games g Where o.Game_Id = g.ID and oe.Olympics_ID = o.ID and Medal_ID != 3 and o.Country_ID in (Select ID from country where NOC=%s))t Group By Year Order By Year" , NOC6)
    r = dictfetchall(cursor)
    for i in r:
        year6.append(i['Year'])
        # print(i['years'])
        medals_won6.append(i['total_medal'])
        # print(i['total_count'])
    

    # query7

    NOC7 = 'USA'
    year7 = []
    male_participants_cnt = []
    female_participants_cnt = []
    cursor.execute("Select m.year, male, female FROM (Select year, count(gender) as male from (Select Distinct year, gender, player_id from player_gender where gender = 'M' and Country_ID in (Select ID from country where NOC=%s))t Group by year order by year) m, (Select year, count(gender) as female from (Select Distinct year, gender, player_id from player_gender where gender = 'F' and Country_ID in (Select ID from country where NOC=%s))t Group by year order by year) f Where m.year = f.year", (NOC7,NOC7))
    # cursor.execute("Select m.year, male, female FROM (Select year, count(gender) as male from ( Select Distinct g.year, p.gender, p.ID from olympics o, games g, person p where  o.Game_Id = g.ID and o.player_id = p.ID and p.gender = 'M' and o.Country_ID in (Select ID from country where NOC='USA'))t Group by year order by year) m , (Select year, count(gender) as female from (Select Distinct g.year, p.gender, p.ID from olympics o, games g, person p where  o.Game_Id = g.ID and o.player_id = p.ID and p.gender = 'F' and o.Country_ID in (Select ID from country where NOC= %s)) t Group by year order by year) f Where m.year = f.year", NOC7)   
    r = dictfetchall(cursor)
    for i in r:
        year7.append(i['year'])
        # print(i['years'])
        male_participants_cnt.append(i['male'])
        # print(i['total_count'])
        female_participants_cnt.append(i['female'])
    

    # query8

    year8 = []
    sportName8 = 'Wrestling'
    male_participants_cnt_8 = []
    female_participants_cnt_8 = []
    cursor.execute("(Select m.year, m.male,f.female From (SELECT year, count(player_id) as male From(Select DISTINCT year, player_id, Event_ID from player_gender where gender = 'M' and Event_ID in (Select e.ID from events e, sport s where e.sport = s.ID and s.Name = %s)) t Group by Year Order by Year ) m LEFT Join (SELECT year, count(player_id) as female From(Select DISTINCT year, player_id, Event_ID from player_gender where gender = 'F' and Event_ID in (Select e.ID from events e, sport s where e.sport = s.ID and s.Name = %s)) t Group by Year Order by Year) f ON m.year = f.year)", (sportName8, sportName8))
    # cursor.execute("(Select m.year, m.male,f.female From (SELECT year, count(player_id) as male From( Select DISTINCT g.year, o.player_id, oe.Event_ID from olympics o, olympic_event oe, person p, games g where o.Game_Id = g.ID and o.ID = oe.Olympics_ID and o.player_id = p.ID and gender = 'M' and oe.Event_ID in (Select e.ID from events e, sport s where e.sport = s.ID and s.Name = %s))t Group by Year Order by Year ) m LEFT Join (SELECT year, count(player_id) as female From( Select DISTINCT g.year, o.player_id, oe.Event_ID from olympics o, olympic_event oe, person p, games g where o.Game_Id = g.ID and o.ID = oe.Olympics_ID and o.player_id = p.ID and gender = 'F' and oe.Event_ID in (Select e.ID from events e, sport s where e.sport = s.ID and s.Name = %s))t Group by Year Order by Year) f ON m.year = f.year)", (sportName8, sportName8))
    r = dictfetchall(cursor)
    for i in r:
        year8.append(i['year'])
        # print(i['years'])
        male_participants_cnt_8.append(i['male'])
        # print(i['total_count'])
        female_participants_cnt_8.append(i['female'])

     # query9

    year9 = []
    NOC9 = 'USA'
    sportName9 = 'Wrestling'
    medal_won9 = []
    
    cursor.execute("SELECT year, count(Medal_ID) as country_medal From( SELECT DISTINCT g.year, oe.event_ID, o.player_ID, oe.Medal_ID from olympics o, olympic_event oe, games g where  o.Game_Id = g.ID and o.ID = oe.olympics_ID and oe.Medal_ID != 3 and o.Country_ID in (Select ID from country where NOC=%s)and oe.Event_ID in (Select e.ID from events e, sport s where e.sport = s.ID and s.Name = %s)) t GROUP BY year Order BY year", (NOC9, sportName9))
    r = dictfetchall(cursor)
    for i in r:
        year9.append(i['year'])
        # print(i['years'])
        medal_won9.append(i['country_medal'])

      # query10

    age10 = []
    sportName10 = 'Wrestling'
    participants_cnt10 = []
    cursor.execute("select age, count(player_id) as total from (Select distinct age, player_id, Event_ID from player_event where Event_ID in (Select e.ID from events e, sport s where e.sport = s.ID and s.Name = %s)) t group by age Having age <> '' order by age" , sportName10)
    # cursor.execute("select age, count(player_id) as total from(Select distinct age, player_id, Event_ID from olympics o, olympic_event oe, person p where o.ID = oe.olympics_ID and o.player_id = p.ID and oe.Event_ID in (Select e.ID from events e, sport s where e.sport = s.ID and s.Name = %s))t group by age Having age <> '' order by age", sportName10)
    r = dictfetchall(cursor)
    for i in r:
        age10.append(i['age'])
        # print(i['years'])
        participants_cnt10.append(i['total'])
        
      # query11

    age11 = []
    NOC11 = 'USA'
    participants_cnt11 = []
    cursor.execute("select age, count(player_id) as total from (Select distinct age, player_id, Event_ID from player_event where Country_ID in (Select ID from country where NOC=%s)) t group by age Having age <> '' order by age", NOC11)
    # cursor.execute("select age, count(player_id) as total from(Select distinct age, player_id, Event_ID from olympics o, olympic_event oe, person p where o.ID = oe.olympics_ID and o.player_id = p.ID and o.Country_ID in (Select ID from country where NOC=%s))t group by age Having age <> '' order by age", NOC11)
    r = dictfetchall(cursor)
    for i in r:
        age11.append(i['age'])
        # print(i['years'])
        participants_cnt11.append(i['total'])
        
      # query12

    age12 = []
    NOC12 = 'USA'
    sportName12 = 'Wrestling'
    participants_cnt12 = []
    cursor.execute("select age, count(player_id) as total from (Select distinct age, player_id, Event_ID from player_event where Country_ID in (Select ID from country where NOC=%s) and Event_ID in (Select e.ID from events e, sport s where e.sport = s.ID and s.Name = %s)) t group by age Having age <> ''  order by age" , (NOC12, sportName12))
    # cursor.execute("select age, count(player_id) as total from(Select distinct age, player_id, Event_ID from olympics o, olympic_event oe, person p where o.ID = oe.olympics_ID and o.player_id = p.ID and o.Country_ID in (Select ID from country where NOC=%s) and oe.Event_ID in (Select e.ID from events e, sport s where e.sport = s.ID and s.Name = %s))t group by age Having age <> '' order by age", (NOC12, sportName12))
    r = dictfetchall(cursor)
    for i in r:
        age12.append(i['age'])
        # print(i['years'])
        participants_cnt12.append(i['total'])
    
    context = {
      
        'male_participation': male_participation,
        'female_participation': female_participation,
        'year1': year1,
        'sportName1': sportName1,
        'year2': year2,
        'country2': country2,
        'total_count2': total_count2,
        'name3': name3,
        'medals_won3': medals_won3,
        'NOC3': NOC3,
        'medal4': medal4,
        'medals_won4': medals_won4,
        'NOC4': NOC4,
        'year4': year4,
        'sport4': sport4,
        'year6': year6,
        'medals_won6': medals_won6,
        'year7': year7,
        'male_participants_cnt': male_participants_cnt,
        'female_participants_cnt': female_participants_cnt,
        'year8': year8,
        'male_participants_cnt_8': male_participants_cnt_8,
        'female_participants_cnt_8': female_participants_cnt_8,
        'year9': year9,
        'medal_won9': medal_won9,
        'age10': age10,
        'participants_cnt10': participants_cnt10,
        'participants_cnt11': participants_cnt11,
        'age11': age11,
        'participants_cnt12': participants_cnt12,
        'age12': age12

    }
    # print('year_solution',year_solution)
    dataJSON = json.dumps(context)
   
    # print("dataJSON", dataJSON)
    
    # print(solution)

    return render(request, 'blog/home.html', {'data': dataJSON , 'year1': year1 , 'sportName1': sportName1, 'sportName8': sportName8 , 'NOC7': NOC7, 'country2': country2, 'NOC3': NOC3, 'NOC4': NOC4,'year4': year4, 'sport4': sport4, 'NOC6': NOC6, 'NOC9': NOC9, 'sportName9': sportName9, 'sportName10': sportName10, 'NOC11': NOC11, 'NOC12': NOC12, 'sportName12':sportName12 })


def about(request):
    return render(request, 'blog/about.html')