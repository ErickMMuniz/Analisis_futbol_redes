while n <= N:
    # DATA PLAYER
    player = desjoin_player_team(ball_path[n])
    player_pos = player[0]
    player_team = player[1]
    try:
        data_player = team_graph[player_team]["team_data"][player_pos]
    except:
        print(player)
    passing = data_player.stats["passing"]
    shooting = data_player.stats["shooting"]

    cobertura = passing["medium"]["complete"] + passing["large"]["complete"] + shooting["complete"]

    # DECIDIMOS SI PASE O TIRO A GOL
    if random() < shooting["complete"] / cobertura:
        # VAMOS A GOL
        try:
            p = shooting["complete"] / shooting["total"]
            if random() < p:
                # GOL
                goal_node = join_player_team("GOAL", player_team)
                ball_path.append(goal_node)
                team_versus = team_graph[player_team]["versus"]
                next_player = join_player_team(team_graph[team_versus]["init"], team_versus)
                ball_path.append(next_player)
            else:
                # NO GOL
                next_player = join_player_team("GK", team_graph[player_team]["versus"])
                ball_path.append(next_player)
        except:
            # NO HIZO ALGÚN TIRO
            continue
    else:
        # VAMOS A PASE
        medium_pass = passing["medium"]
        large_pass = passing["large"]

        cobertura = medium_pass["complete"] + large_pass["complete"]

        if random() < medium_pass["complete"] / cobertura:
            # AQUÍ HACER UN PASE CORTO MEDIO
            vecinos = get_vecinos_medium(team_graph[player_team]["lineup"], player_pos)
            next_player = choice(vecinos)

            p = medium_pass["complete"] / medium_pass["total"]
            if random() < p:
                # PASE COMPLETADO
                n_player = join_player_team(next_player, player_team)
                ball_path.append(n_player)
            else:
                # INTERCEPCIÓN
                try:
                    versus = get_vecinos_versus(g_v, next_player)
                    next_player = choice(versus)
                    team_versus = team_graph[player_team]["versus"]
                    n_player = join_player_team(next_player, team_versus)
                    ball_path.append(n_player)
                except:
                    continue

        else:
            # AQUÍ HACEMOS PASE LARGO
            vecinos = get_vecinos_large(team_graph[player_team]["lineup"], player_pos)
            next_player = choice(vecinos)

            p = large_pass["complete"] / large_pass["total"]
            if random() < p:
                # PASE COMPLETADO
                n_player = join_player_team(next_player, player_team)
                ball_path.append(n_player)
            else:
                # INTERCEPCIÓN
                try:
                    versus = get_vecinos_versus(g_v, next_player)
                    next_player = choice(versus)
                    team_versus = team_graph[player_team]["versus"]
                    n_player = join_player_team(next_player, team_versus)
                    ball_path.append(n_player)
                except:
                    continue
    n += 1