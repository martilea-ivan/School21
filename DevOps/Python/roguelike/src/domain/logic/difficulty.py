class DifficultyManager:

    @staticmethod
    def get_modifiers(player):

        stats = player.statistics
        hp_lost = stats.hp_lost
        enemies_killed = stats.enemies_killed
        max_hp = player.max_health

        enemy_mod = 1.0
        item_mod = 1.0

        # Слишком тяжело — игрок теряет больше половины HP
        if hp_lost > max_hp * 0.5:
            enemy_mod = 0.7
            item_mod = 1.4

        # Слишком легко — мало урона и много убийств
        elif enemies_killed >= 5 and hp_lost < max_hp * 0.2:
            enemy_mod = 1.3
            item_mod = 1.7

        # Средне — небольшие коррекции
        elif hp_lost < max_hp * 0.1:
            enemy_mod = 1.15

        return enemy_mod, item_mod
