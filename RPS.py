import random

class Player:
    def __init__(self):
        self.my_moves = []
        self.opp_moves = []
        self.lose_streak = 0
        self.lose_streak_limit = 3
        self.max_repeat_avoid = 3
        self.window_size = 3  # ventana más pequeña para detectar patrones mejor
        self.explore_chance = 0.5
        self.counter_map = {'R': 'P', 'P': 'S', 'S': 'R'}

    def __call__(self, prev_opponent_play):
        # Esta función es llamada para obtener la jugada actual
        move = self.move()
        return move

    def move(self):
        if len(self.opp_moves) < self.window_size:
            # No hay suficiente historial, juega al azar
            return random.choice(['R', 'P', 'S'])

        prediction = self.predict_opponent_move()

        # El counter para ganarle al movimiento predicho
        predicted_move = self.counter_map.get(prediction, random.choice(['R', 'P', 'S']))

        # Si estás en racha de pérdidas, a veces explora para romper patrones
        if self.lose_streak >= self.lose_streak_limit and random.random() < self.explore_chance:
            move = random.choice(['R', 'P', 'S'])
        else:
            move = predicted_move

        # Evita repetir el mismo movimiento más de max_repeat_avoid veces
        if len(self.my_moves) >= self.max_repeat_avoid:
            if all(m == move for m in self.my_moves[-self.max_repeat_avoid:]):
                alternatives = [m for m in ['R', 'P', 'S'] if m != move]
                move = random.choice(alternatives)

        return move

    def predict_opponent_move(self):
        window = self.window_size
        pattern = ''.join(self.opp_moves[-window:])
        freq = {'R': 0, 'P': 0, 'S': 0}

        # Busca ocurrencias del patrón en el historial y cuenta el movimiento siguiente
        for i in range(len(self.opp_moves) - window):
            if ''.join(self.opp_moves[i:i + window]) == pattern:
                if i + window < len(self.opp_moves):
                    next_move = self.opp_moves[i + window]
                    freq[next_move] += 1

        # Si no encontró patrones, usa frecuencias globales del historial
        if sum(freq.values()) == 0:
            freq = {m: self.opp_moves.count(m) for m in ['R', 'P', 'S']}

        # Predice el movimiento más probable del oponente
        predicted = max(freq, key=freq.get)
        return predicted

    def learn(self, my_move, opp_move, result):
        # Aprende el resultado y actualiza historial
        self.my_moves.append(my_move)
        self.opp_moves.append(opp_move)

        if result == 'loss':
            self.lose_streak += 1
        else:
            self.lose_streak = 0
