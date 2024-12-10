from typing import List, Tuple, Dict

def round_robin_tournament_with_referees(num_teams: int, group_name: str) -> Tuple[List[Tuple[str, str, str]], List[Tuple[str, str, str]], List[Tuple[str, str, str]]]:
    """
    Erstelle ein Round-Robin-Turnier mit Schiedsrichtern.

    :param num_teams: Anzahl der Teams in der Gruppe
    :param group_name: Der Name der Gruppe (z. B. "Fun", "Schwitzer")
    :return: Ein Tuple bestehend aus drei Listen:
             - alle Spiele (alle Runden),
             - jedes zweite Spiel (zweite Runde),
             - alle Spiele ohne jedes zweite Spiel
    """
    # Erstelle eine Liste von Teams (1 bis num_teams) mit den Gruppennamen
    teams: List[str] = [f"{group_name} {i + 1}" for i in range(num_teams)]
    # Listen für alle Spiele, jedes zweite Spiel und alle ohne jedes zweite Spiel
    all_matches: List[Tuple[str, str, str]] = []
    second_round_matches: List[Tuple[str, str, str]] = []
    without_second_round_matches: List[Tuple[str, str, str]] = []

    # Jede Runde hat die Spiele für diese Runde
    for round_num in range(num_teams - 1):
        round_matches: List[Tuple[str, str, str]] = []
        available_referees: List[str] = teams.copy()  # Liste der verfügbaren Schiedsrichter

        for i in range(num_teams // 2):
            team1: str = teams[i]
            team2: str = teams[num_teams - 1 - i]

            # Schiedsrichter auswählen, der nicht an diesem Spiel beteiligt ist
            available_referees.remove(team1)
            available_referees.remove(team2)

            # Wenn weniger als 1 Schiedsrichter übrig ist, müssen wir die Liste der Schiedsrichter neu füllen
            if not available_referees:
                available_referees = [team for team in teams if team != team1 and team != team2]

            referee: str = available_referees.pop(0)  # Der erste verfügbare Schiedsrichter wird gewählt

            # Ein Spiel für die Runde hinzufügen, zusammen mit dem Schiedsrichter
            match: Tuple[str, str, str] = (team1, team2, referee)
            round_matches.append(match)

            # Jedes zweite Spiel zusätzlich in der zweiten Liste speichern
            if (i + 1) % 2 == 0:
                second_round_matches.append(match)

            # Schiedsrichter zurück in die Liste der verfügbaren Schiedsrichter setzen
            available_referees.append(referee)

        all_matches.extend(round_matches)  # Alle Spiele in die "all_matches" Liste einfügen
        without_second_round_matches.extend([match for i, match in enumerate(round_matches) if (i + 1) % 2 != 0])

        # Teams rotieren (der erste spielt gegen den letzten, der zweite gegen den vorletzten usw.)
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]

    return all_matches, second_round_matches, without_second_round_matches, teams


def assign_matches_to_fields(all_matches_group1: List[Tuple[str, str, str]], second_round_matches_group1: List[Tuple[str, str, str]], without_second_round_matches_group1: List[Tuple[str, str, str]],
                             all_matches_group2: List[Tuple[str, str, str]], second_round_matches_group2: List[Tuple[str, str, str]], without_second_round_matches_group2: List[Tuple[str, str, str]],
                             num_fields: int, fun_team: List[str], competitive_team: List[str]) -> Dict[int, List[Tuple[str, str, str]]]:
    """
    Weist die Spiele den Feldern zu.

    :param all_matches_group1: Alle Spiele der ersten Gruppe
    :param second_round_matches_group1: Alle zweiten Runden der ersten Gruppe
    :param without_second_round_matches_group1: Alle Spiele ohne jedes zweite Spiel der ersten Gruppe
    :param all_matches_group2: Alle Spiele der zweiten Gruppe
    :param second_round_matches_group2: Alle zweiten Runden der zweiten Gruppe
    :param without_second_round_matches_group2: Alle Spiele ohne jedes zweite Spiel der zweiten Gruppe
    :param num_fields: Anzahl der Felder (2 oder 3)
    :return: Ein Dictionary, das jedem Feld eine Liste von Spielen zuweist
    """

    referee_fun_dic = {team: 0 for team in fun_team}  # Initialisiere das Dictionary
    referee_competitive_dic = {team: 0 for team in competitive_team}


    # TODO Dic mit den einzelne teams speichern, und wie oft sie gepfiffen haben
    # TODO abfangen des falles, das die teams nicht die gleiche anzahl haben
    # TODO ungerade teamanzahlen verarbeiten

    # Basierend auf der Anzahl der Felder werden die Listen den Feldern zugewiesen
    fields: Dict[int, List[Tuple[str, str, str]]] = {1: [], 2: [], 3: []}  # Felder 1, 2, 3

    if num_fields == 2:
        # Feld 1: Alle Spiele Gruppe 1, Feld 2: Alle Spiele Gruppe 2
        fields[1] = all_matches_group1
        fields[2] = all_matches_group2
    elif num_fields == 3:
        # Feld 1: Alle Spiele ohne jedes zweite Spiel aus Gruppe 1
        fields[1] = without_second_round_matches_group1

        # Feld 3: Alle Spiele ohne jedes zweite Spiel aus Gruppe 2
        fields[3] = without_second_round_matches_group2

        # Feld 2: Abwechselnd jedes zweite Spiel von Gruppe 1 und Gruppe 2

        alternating_matches: List[Tuple[str, str, str]] = []

        max_len: int = max(len(second_round_matches_group1), len(second_round_matches_group2))

        for i in range(max_len):
            if i < len(second_round_matches_group1):
                alternating_matches.append(second_round_matches_group1[i])
            if i < len(second_round_matches_group2):
                alternating_matches.append(second_round_matches_group2[i])

        fields[2] = alternating_matches

        for i in range(0, len(alternating_matches)):
            # Prüfen, ob der aktuelle Schiedsrichter von Feld 2 auch auf Feld 1 aktiv ist
            if fields[2][i][2] in fields[1][i]:
                # Liste der möglichen Schiedsrichter, die in diesem Spiel pfeifen könnten
                possible_referees = [team for team in fun_team if team not in fields[2][i] and team not in fields[1][i]]

                # Finde das Team mit dem kleinsten Zählerwert im referee_fun_dic
                if possible_referees:  # Sicherstellen, dass es mögliche Schiedsrichter gibt
                    selected_team = min(possible_referees, key=lambda x: referee_fun_dic[x])
                    fields[2][i] = (fields[2][i][0], fields[2][i][1], selected_team)  # Team als Schiedsrichter zuweisen
                    referee_fun_dic[selected_team] += 1  # Zähler für das Team erhöhen

            if fields[2][i][2] in fields[3][i]:
                possible_referees = [team for team in competitive_team if team not in fields[2][i][0] and team not in fields[2][i][1] and team not in fields[3][i]]

                if possible_referees:
                    selected_team = min(possible_referees, key=lambda x: referee_competitive_dic[x])
                    fields[2][i] = (fields[2][i][0], fields[2][i][1], selected_team)
                    referee_competitive_dic[selected_team] += 1


        for i in range(0, len(without_second_round_matches_group1)):
            if fields[1][i][2] in fields[2][i]:
                for team in fun_team:
                    if team not in fields[1][i] and team not in fields[2][i]:
                        fields[1][i] = (fields[1][i][0], fields[1][i][1], team)
                        break

        for i in range(0, len(without_second_round_matches_group2)):

            possible_referees = [team for team in competitive_team if
                                 team not in fields[3][i][0] and team not in fields[3][i][1] and team not in
                                 fields[2][i]]
            print(f"Possible Referees: {possible_referees}")
            if possible_referees:
                selected_team = min(possible_referees, key=lambda x: referee_competitive_dic[x])
                fields[3][i] = (fields[3][i][0], fields[3][i][1], selected_team)
                referee_competitive_dic[selected_team] += 1



    return fields


def get_games_weighted(num_teams: int, group_name: str):
    teams = []

    # Initialisiere das Dictionary mit den Teamnamen und der Anzahl der gespielten Spiele
    team_fun_dic = {f"Fun {team}": 0 for team in range(1, num_teams + 1)}

    # Generiere alle Teamnamen
    for i in range(1, num_teams + 1):
        teams.append(f"{group_name} {i}")

    from itertools import combinations

    # Erzeuge alle Kombinationen von Teams
    all_matches = list(combinations(range(1, num_teams + 1), 2))

    # Erzeuge die formatted_matches-Liste mit den Teamnamen
    formatted_matches = [(f"Fun {team1}", f"Fun {team2}") for (team1, team2) in all_matches]
    print(f"Formatted Matches: {formatted_matches}")

    matches = []
    total_games = num_teams * (num_teams - 1) // 2

    last_match = None  # Variable, um das letzte Spiel zu speichern

    # Solange noch nicht alle Spiele durchgeführt wurden
    while len(matches) < total_games:
        # Sortiere formatted_matches nach der Anzahl der Spiele der beiden Teams
        formatted_matches.sort(key=lambda x: (team_fun_dic[x[0]], team_fun_dic[x[1]]))
        print(f"Formatted Matches: {formatted_matches}")

        # Wähle das erste Match aus der sortierten Liste
        team1, team2 = formatted_matches.pop(0)  # Wähle das Match mit den wenigsten Spielen
        new_match = (team1, team2)

        # Überprüfe, ob eines der Teams im letzten Spiel war
        if last_match and (team1 in last_match or team2 in last_match):
            # Wenn eines der Teams im letzten Spiel war, überspringe dieses Spiel und wähle das nächste
            formatted_matches.append((team1, team2))
            continue

        # Füge das Match der Liste hinzu
        matches.append(new_match)

        # Erhöhe die Anzahl der Spiele für beide Teams
        team_fun_dic[team1] += 1
        team_fun_dic[team2] += 1

        # Speichere das aktuelle Match als das letzte Spiel
        last_match = new_match

    print(f"Matches: {matches}")
    for match in matches:
        print(f"Match: {match}")




# Beispiel: Turnier mit 6 Teams für jede Gruppe
num_teams_group1: int = 6
num_teams_group2: int = 6

# Erstelle den Turnierplan für Gruppe 1 (Fun 1-6)
all_matches_group1, second_round_matches_group1, without_second_round_matches_group1, fun_team = round_robin_tournament_with_referees(num_teams_group1, "Fun")

# Erstelle den Turnierplan für Gruppe 2 (Schwitzer 7-12)
all_matches_group2, second_round_matches_group2, without_second_round_matches_group2, competitive = round_robin_tournament_with_referees(num_teams_group2, "Schwitzer")

# Benutzer wählt die Anzahl der Felder (2 oder 3)
num_fields: int = int(input("Gib die Anzahl der Felder ein (2 oder 3): "))

# Spiele den Plan den Feldern zuordnen
fields: Dict[int, List[Tuple[str, str, str]]] = assign_matches_to_fields(all_matches_group1, second_round_matches_group1, without_second_round_matches_group1,
                                                                            all_matches_group2, second_round_matches_group2, without_second_round_matches_group2, num_fields, fun_team, competitive_team=competitive)

get_games_weighted(num_teams_group1, "Fun")

# Ausgabe der Spiele für jedes Feld
#for field, matches in fields.items():
 #   print(f"\nFeld {field}:")
  #  for match in matches:
   #     team1, team2, referee = match
    #    print(f"{team1} vs {team2} - Schiedsrichter: {referee}")
