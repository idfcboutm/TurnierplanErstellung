from typing import List, Tuple, Dict
from itertools import combinations


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




def get_games_weighted(num_teams: int, group_name: str) -> List[Tuple[str, str]]:
    teams: List[str] = []

    # Initialisiere das Dictionary mit den Teamnamen und der Anzahl der gespielten Spiele
    team_fun_dic: Dict[str, int] = {f"{group_name} {team}": 0 for team in range(1, num_teams + 1)}

    # Generiere alle Teamnamen
    for i in range(1, num_teams + 1):
        teams.append(f"{group_name} {i}")

    # Erzeuge alle Kombinationen von Teams
    all_matches: List[Tuple[int, int]] = list(combinations(range(1, num_teams + 1), 2))

    # Erzeuge die formatted_matches-Liste mit den Teamnamen
    formatted_matches: List[Tuple[str, str]] = [(f"{group_name} {team1}", f"{group_name} {team2}") for (team1, team2) in all_matches]

    matches: List[Tuple[str, str]] = []
    total_games: int = num_teams * (num_teams - 1) // 2

    last_match: Tuple[str, str] | None = None  # Variable, um das letzte Spiel zu speichern

    # Solange noch nicht alle Spiele durchgeführt wurden
    while len(matches) < total_games:
        # Sortiere formatted_matches nach der Anzahl der Spiele der beiden Teams
        formatted_matches.sort(key=lambda x: (team_fun_dic[x[0]], team_fun_dic[x[1]]))

        # Wähle das erste Match aus der sortierten Liste
        team1, team2 = formatted_matches.pop(0)  # Wähle das Match mit den wenigsten Spielen
        new_match: Tuple[str, str] = (team1, team2)

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

    return matches



def distribute_games_to_fields_and_assign_referees(fun_matches: List[Tuple[str, str]], competitive_matches: List[Tuple[str, str]], num_fields: int) -> Dict[int, List[Tuple[str, str, str]]]:
    """
    Weist die Spiele den Feldern zu und weist Schiedsrichter zu.

    :param fun_matches: Alle Spiele der Fun-Gruppe
    :param competitive_matches: Alle Spiele der Competitive-Gruppe
    :param num_fields: Anzahl der Felder (2 oder 3)
    :return: Ein Dictionary, das jedem Feld eine Liste von Spielen zuweist
    """



    # Basierend auf der Anzahl der Felder werden die Listen den Feldern zugewiesen
    fields: Dict[int, List[Tuple[str, str, str]]] = {1: [], 2: [], 3: []}  # Felder 1, 2, 3



    fun_matches_with_referees: List[Tuple[str, str, str]] = []
    all_teams_fun = sorted(set(team for match in fun_matches for team in match))
    referee_fun_dic = {team: 0 for team in all_teams_fun}

    for match_fun in fun_matches:
        team1_fun, team2_fun = match_fun
        possible_referees = [team for team in all_teams_fun if team not in match_fun]
        selected_referee = min(possible_referees, key=lambda x: referee_fun_dic[x])
        fun_matches_with_referees.append((team1_fun, team2_fun, selected_referee))
        referee_fun_dic[selected_referee] += 1


    competitive_matches_with_referees: List[Tuple[str, str, str]] = []
    all_teams_competitive = sorted(set(team for match in competitive_matches for team in match))
    referee_competitive_dic = {team: 0 for team in all_teams_competitive}

    for match_competitive in competitive_matches:
        team1_competitive, team2_competitive = match_competitive
        possible_referees = [team for team in all_teams_competitive if team not in match_competitive]
        selected_referee_competitive = min(possible_referees, key=lambda x: referee_competitive_dic[x])
        competitive_matches_with_referees.append((team1_competitive, team2_competitive, selected_referee_competitive))
        referee_competitive_dic[selected_referee_competitive] += 1



    if num_fields == 2:
        # Feld 1: Alle Spiele Fun-Gruppe, Feld 2: Alle Spiele Competitive-Gruppe
        fields[1] = fun_matches_with_referees
        fields[2] = competitive_matches_with_referees

    elif num_fields == 3:
        max_len = max(len(fun_matches_with_referees), len(competitive_matches_with_referees))
        field_2_free_for_fun = True  # Initialisierung der Umschaltlogik

        for i in range(max_len):
            # Feld 1: Spiel von Fun-Gruppe (falls vorhanden)
            if fun_matches_with_referees:
                fields[1].append(fun_matches_with_referees.pop())

            # Feld 2: Abwechselndes Spiel von Fun- und Competitive-Gruppe
            if field_2_free_for_fun and fun_matches_with_referees:
                fields[2].append(fun_matches_with_referees.pop())
                field_2_free_for_fun = False
            elif not field_2_free_for_fun and competitive_matches:
                fields[2].append(competitive_matches_with_referees.pop())
                field_2_free_for_fun = True

            # Feld 3: Spiel von Competitive-Gruppe (falls vorhanden)
            if competitive_matches_with_referees:
                fields[3].append(competitive_matches_with_referees.pop())


        for i in range(0, len(fields[1])):
            possible_referees = [team for team in all_teams_fun if team not in fields[1][i][0] and team not in fields[1][i][1] and team not in fields[2][i]]
            if possible_referees:
                selected_team = min(possible_referees, key=lambda x: referee_fun_dic[x])
                fields[1][i] = (fields[1][i][0], fields[1][i][1], selected_team)
                referee_fun_dic[selected_team] += 1
                referee_fun_dic[fields[1][i][2]] -= 1
                break


        for i in range(0, len(fields[3])):

            possible_referees = [team for team in all_teams_competitive if
                                 team not in fields[3][i][0] and team not in fields[3][i][1] and team not in fields[2][
                                     i]]
            if possible_referees:
                selected_team = min(possible_referees, key=lambda x: referee_competitive_dic[x])
                fields[3][i] = (fields[3][i][0], fields[3][i][1], selected_team)
                referee_competitive_dic[selected_team] += 1
                referee_competitive_dic[fields[3][i][2]] -= 1
                break


        for i in range(0, len(fields[2])):
            if fields[2][i][2] in fields[1][i]:
                possible_referees = [team for team in all_teams_fun if team not in fields[2][i][0] and team not in fields[2][i][1] and team not in fields[1][i]]
                if possible_referees:
                    selected_team = min(possible_referees, key=lambda x: referee_fun_dic[x])
                    fields[2][i] = (fields[2][i][0], fields[2][i][1], selected_team)
                    referee_fun_dic[selected_team] += 1
                    referee_fun_dic[fields[2][i][2]] -= 1
                    break

            if fields[2][i][2] in fields[3][i]:

                possible_referees = [team for team in all_teams_competitive if team not in fields[2][i][0] and team not in fields[2][i][1] and team not in fields[3][i]]

                if possible_referees:
                    selected_team = min(possible_referees, key=lambda x: referee_competitive_dic[x])
                    fields[2][i] = (fields[2][i][0], fields[2][i][1], selected_team)
                    referee_competitive_dic[selected_team] += 1
                    referee_competitive_dic[fields[2][i][2]] -= 1
                    break



    return fields



# Beispiel: Turnier mit 6 Teams für jede Gruppe
num_teams_group1: int = 6
num_teams_group2: int = 6

# Erstelle den Turnierplan für Gruppe 1 (Fun 1-6)
#all_matches_group1, second_round_matches_group1, without_second_round_matches_group1, fun_team = round_robin_tournament_with_referees(num_teams_group1, "Fun")

# Erstelle den Turnierplan für Gruppe 2 (Schwitzer 7-12)
#all_matches_group2, second_round_matches_group2, without_second_round_matches_group2, competitive = round_robin_tournament_with_referees(num_teams_group2, "Schwitzer")

# Benutzer wählt die Anzahl der Felder (2 oder 3)
num_fields: int = int(input("Gib die Anzahl der Felder ein (2 oder 3): "))

# Spiele den Plan den Feldern zuordnen
#fields: Dict[int, List[Tuple[str, str, str]]] = assign_matches_to_fields(all_matches_group1, second_round_matches_group1, without_second_round_matches_group1, all_matches_group2, second_round_matches_group2, without_second_round_matches_group2, num_fields, fun_team, competitive_team=competitive)

fun_matches = get_games_weighted(num_teams_group1, "Fun")
competitive_matches = get_games_weighted(num_teams_group2, "Schwitzer")

fields_new = distribute_games_to_fields_and_assign_referees(fun_matches, competitive_matches, num_fields)

for field, matches in fields_new.items():
    print(f"\nFeld {field}:")
    for match in matches:
        team1, team2, referee = match
        print(f"{team1} vs {team2} - Schiedsrichter: {referee}")

# Ausgabe der Spiele für jedes Feld
#for field, matches in fields.items():
 #   print(f"\nFeld {field}:")
  #  for match in matches:
   #     team1, team2, referee = match
    #    print(f"{team1} vs {team2} - Schiedsrichter: {referee}")
