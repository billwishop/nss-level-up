SELECT * FROM levelupapi_game;
SELECT * FROM levelupapi_event;
SELECT * FROM levelupapi_gamer;

SELECT
    g.id,
    g.title,
    g.gametype_id,
    g.number_of_players,
    g.description,
    u.id user_id,
    u.first_name || ' ' || u.last_name AS full_name
FROM
    levelupapi_game g
JOIN 
    levelupapi_gamer gr ON g.gamer_id = gr.id
JOIN 
    auth_user u ON gr.user_id = u.id
;