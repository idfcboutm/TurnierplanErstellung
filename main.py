from typing import List, Tuple, Dict
from itertools import combinations


#TODO ungleiche anzahl von teams abfangen: zum Beispiel Fun = 5 Teams und Schwitzer = 6 Teams:  große aufgabe --> done für 2 gruppen mit 2 feldern, fehlt 3 felder, 4 felder
#TODO Anzahl teams eingeben : kleine Aufgabe --> done, testing
#TODO 4 Felder implementieren : große Aufgabe
#TODO Hin und Rückspiel implementieren : kleine Aufgabe
#TODO 1 Gruppe mehrere Felder : große Aufgabe

#TODO zu wenig Teams für anzahl felder filtern oder ist das egal?



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

    def update_field_refs(source_field, target_field, all_teams, referee_dic):
        """
        Überprüft und aktualisiert die Schiedsrichter für die Ziel-Felder basierend auf Konflikten.

        :param source_field: Ursprungsfeld für Konfliktüberprüfung
        :param target_field: Zielfeld, dessen Schiedsrichter angepasst werden sollen
        :param all_teams: Liste der möglichen Schiedsrichterteams
        :param referee_dic: Dictionary, das die Einsätze der Schiedsrichter zählt
        """
        for i in range(len(fields[target_field])):
            if fields[target_field][i][2] in fields[source_field][i]:
                possible_referees = [team for team in all_teams if team not in fields[target_field][i][0] and team not in fields[target_field][i][1] and team not in fields[source_field][i]]
                if possible_referees:
                    selected_team = min(possible_referees, key=lambda x: referee_dic[x])
                    fields[target_field][i] = (fields[target_field][i][0], fields[target_field][i][1], selected_team)
                    referee_dic[selected_team] += 1
                    referee_dic[fields[target_field][i][2]] -= 1
                    break

    def update_field_ref_without_checking(source_field, target_field, all_teams, referee_dic):
        """
        Überprüft und aktualisiert die Schiedsrichter für die Ziel-Felder basierend auf Konflikten.

        :param source_field: Ursprungsfeld für Konfliktüberprüfung
        :param target_field: Zielfeld, dessen Schiedsrichter angepasst werden sollen
        :param all_teams: Liste der möglichen Schiedsrichterteams
        :param referee_dic: Dictionary, das die Einsätze der Schiedsrichter zählt
        """
        for i in range(len(fields[target_field])):
            possible_referees = [team for team in all_teams if team not in fields[target_field][i][0] and team not in fields[target_field][i][1] and team not in fields[source_field][i]]
            if possible_referees:
                selected_team = min(possible_referees, key=lambda x: referee_dic[x])
                fields[target_field][i] = (fields[target_field][i][0], fields[target_field][i][1], selected_team)
                referee_dic[selected_team] += 1
                referee_dic[fields[target_field][i][2]] -= 1
                break



    # Basierend auf der Anzahl der Felder werden die Listen den Feldern zugewiesen
    fields: Dict[int, List[Tuple[str, str, str]]] = {i: [] for i in range(1, num_fields + 1)}



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

        max_len = max(len(fun_matches_with_referees), len(competitive_matches_with_referees))

        for i in range(max_len):
            if fun_matches_with_referees:
                fields[1].append(fun_matches_with_referees.pop())

            if competitive_matches_with_referees:
                fields[2].append(competitive_matches_with_referees.pop())

            if fun_matches_with_referees and not competitive_matches_with_referees:
                fields[2].append(fun_matches_with_referees.pop())

            if competitive_matches_with_referees and not fun_matches_with_referees:
                fields[1].append(competitive_matches_with_referees.pop())


        if len(fun_matches) < len(competitive_matches):
            update_field_ref_without_checking(1, 2, all_teams_competitive, referee_competitive_dic)
            update_field_ref_without_checking(2, 1, all_teams_competitive, referee_competitive_dic)

        if len(fun_matches) > len(competitive_matches):
            update_field_ref_without_checking(1, 2, all_teams_fun, referee_fun_dic)
            update_field_ref_without_checking(2, 1, all_teams_fun, referee_fun_dic)



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


        update_field_ref_without_checking(2,1, all_teams_fun, referee_fun_dic)


        update_field_ref_without_checking(2,3, all_teams_competitive, referee_competitive_dic)



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



def distribute_games_to_fields_with_one_group(only_team_matches: List[Tuple[str, str]], num_fields: int) -> Dict[int, List[Tuple[str, str, str]]]:
    """
    Weist die Spiele einer Gruppe den Feldern zu und weist Schiedsrichter zu.

    :param only_team_matches: Alle Spiele einer Gruppe (Fun oder Competitive)
    :param num_fields: Anzahl der Felder (2, 3 oder 4)
    :return: Ein Dictionary, das jedem Feld eine Liste von Spielen zuweist
    :raises ValueError: Wenn nicht genügend Teams für die Anzahl der Felder vorhanden sind.
    """
    # Mindestanzahl an Teams basierend auf der Anzahl der Felder
    required_teams = {2: 6, 3: 8, 4: 10}
    all_teams = sorted(set(team for match in only_team_matches for team in match))

    if num_fields in required_teams and len(all_teams) < required_teams[num_fields]:
        raise ValueError(f"Nicht genügend Teams vorhanden: Für {num_fields} Felder werden mindestens {required_teams[num_fields]} Teams benötigt, aber es sind nur {len(all_teams)} Teams vorhanden.")

    # Initialisierung der Felder
    fields: Dict[int, List[Tuple[str, str, str]]] = {i: [] for i in range(1, num_fields + 1)}

    # Zuweisung der Spiele mit Schiedsrichtern
    only_team_matches_with_referees: List[Tuple[str, str, str]] = []
    referee_dic = {team: 0 for team in all_teams}

    for match in only_team_matches:
        team1, team2 = match
        possible_referees = [team for team in all_teams if team not in match]
        selected_referee = min(possible_referees, key=lambda x: referee_dic[x])
        only_team_matches_with_referees.append((team1, team2, selected_referee))
        referee_dic[selected_referee] += 1

    if num_fields == 2:
        # Feld 1: Erste Hälfte der Spiele, Feld 2: Zweite Hälfte der Spiele
        mid_index = len(only_team_matches_with_referees) // 2
        fields[1] = only_team_matches_with_referees[:mid_index]
        fields[2] = only_team_matches_with_referees[mid_index:]

    elif num_fields == 3:
        max_len = len(only_team_matches_with_referees)

        for i in range(max_len):
            # Feld 1: Spiele werden nacheinander zugewiesen
            if only_team_matches_with_referees:
                fields[1].append(only_team_matches_with_referees.pop())

            # Feld 2: Abwechselndes Spiel
            if only_team_matches_with_referees:
                fields[2].append(only_team_matches_with_referees.pop())

            # Feld 3: Restliche Spiele
            if only_team_matches_with_referees:
                fields[3].append(only_team_matches_with_referees.pop())


    elif num_fields == 4:
        max_len = len(only_team_matches_with_referees)
        field_rotation = [1, 2, 3, 4]  # Rotationslogik für die Felder
        current_field_index = 0

        for i in range(max_len):
            # Spiele nacheinander auf die Felder 1-4 verteilen
            if only_team_matches_with_referees:
                current_field = field_rotation[current_field_index]
                fields[current_field].append(only_team_matches_with_referees.pop())
                current_field_index = (current_field_index + 1) % len(field_rotation)



    return fields




# Beispiel: Turnier mit 6 Teams für jede Gruppe
num_teams_group1: int = 5
num_teams_group2: int = 6

# Benutzer wählt die Anzahl der Felder (2 oder 3)

count_groups: int = int(input("Gib die Anzahl an Leistungsgruppen an (1 oder 2): "))
num_fields: int = int(input("Gib die Anzahl der Felder ein (2 oder 3): "))
hin_und_rueck: str = str(input("Hin- und Rückspiel? (j oder n): ")).lower()
hin_und_rueck_bool: bool = False

if hin_und_rueck == "j":
    hin_und_rueck_bool = True
elif hin_und_rueck == "n":
    hin_und_rueck_bool = False


#num_teams_group1: int = int(input("Wie viele Teams in Gruppe Fun: "))

#if count_groups == 2:
#    num_teams_group2: int = int(input("Wie viele Teams in Gruppe Schwitzer: "))




fun_matches = get_games_weighted(num_teams_group1, "Fun")
competitive_matches = get_games_weighted(num_teams_group2, "Schwitzer")

if count_groups == 2:
    fields_new = distribute_games_to_fields_and_assign_referees(fun_matches, competitive_matches, num_fields)

if count_groups == 1:
    fields_new = distribute_games_to_fields_with_one_group(fun_matches, num_fields)

for field, matches in fields_new.items():
    print(f"\nFeld {field}:")
    for match in matches:
        team1, team2, referee = match
        print(f"{team1} vs {team2} - Schiedsrichter: {referee}")

