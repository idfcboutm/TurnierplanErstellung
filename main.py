from itertools import permutations
import random


def create_tournament_schedule(fun_teams, competitive_teams, fields, home_and_away=False):
    if len(teams) < 3:
        raise ValueError("Es müssen mindestens drei Teams sein, um einen Turnierplan zu erstellen.")

    # Generiere alle möglichen Spiele (jeder gegen jeden)
    fun_matches = [(team1, team2) for team1, team2 in permutations(fun_teams, 2) if team1 != team2]
    competitive_matches = [(team1, team2) for team1, team2 in permutations(competitive_teams, 2) if team1 != team2]
    schedule = []


    occupied_fun_teams = []
    occupied_competitive_teams = []
    free_fun_teams = fun_teams
    free_competitive_teams = competitive_teams
    occupied_fields = []
    free_fields = [field for field in range(1, fields+1)]
    fun_fields = []
    competitive_fields = []
    mixed_fields = []

    if fields % 2 == 0:
        for i in range (1, int(fields/2) + 1):
            fun_fields.append(i)
            competitive_fields.append(int(i+fields/2))

    if fields % 2 != 0:
        for i in range (1, int(fields/2) + 1):
            fun_fields.append(i)
            competitive_fields.append(int(i+fields/2+1))
        mixed_fields.append(int(fields/2+1))



    print(free_fields)
    print(fun_fields)
    print(competitive_fields)
    print(mixed_fields)

    # Spiele mischen, um die Reihenfolge zu randomisieren
    #TODO nicht random sondern prüfen wer davor gespielt hat und wer nicht
    random.shuffle(fun_matches)
    random.shuffle(competitive_matches)




    # Runde für Runde planen
    while fun_matches:
        round_matches = []
        teams_in_round = set()

        for match in fun_matches[:]:  # Kopiere die Liste, um sie während der Iteration ändern zu können
            if match[0] not in teams_in_round and match[1] not in teams_in_round:
                # Füge das Spiel der Runde hinzu
                possible_refs = [ref for ref in teams if ref not in match]
                ref = random.choice(possible_refs)
                round_matches.append((match[0], match[1], ref))
                teams_in_round.update(match)  # Markiere Teams als beschäftigt
                fun_matches.remove(match)  # Entferne das Spiel aus der Gesamtliste

        for match in round_matches:
            schedule.append(match)  # Hinrunde hinzufügen
            if home_and_away:
                # Rückrunde direkt nach der Hinrunde mit demselben Schiedsrichter
                schedule.append((match[1], match[0], match[2]))

    return schedule




def display_schedule(schedule):
    print("Turnierplan:")
    for i, game in enumerate(schedule, start=1):
        print(f"Spiel {i}: {game[0]} vs {game[1]} (Schiedsrichter: {game[2]})")


# Beispiel-Eingabe
if __name__ == "__main__":
    teams = ["Team A", "Team B", "Team C", "Team D"]

    print("1: Nur Hinrunde\n2: Hin- und Rückrunde")
    choice = input("Wählen Sie den Modus (1 oder 2): ")

    home_and_away = choice == "2"

    try:
        schedule = create_tournament_schedule(teams, teams, 3, home_and_away=home_and_away)
        display_schedule(schedule)
    except ValueError as e:
        print(f"Fehler: {e}")
