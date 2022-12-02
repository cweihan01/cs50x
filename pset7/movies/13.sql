SELECT DISTINCT name FROM people
JOIN stars ON stars.person_id = people.id
WHERE stars.movie_id IN(
SELECT DISTINCT stars.movie_id FROM people
JOIN stars ON stars.person_id = people.id
WHERE people.name = 'Kevin Bacon' AND people.birth = 1958)
AND people.name != 'Kevin Bacon';