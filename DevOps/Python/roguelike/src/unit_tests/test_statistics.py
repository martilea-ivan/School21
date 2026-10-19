from domain.objects.statistics import Statistics


class TestStatistics:
    def test_counters(self):
        s = Statistics()
        s.add_enemy_killed()
        s.add_food_eaten()
        s.add_hit_dealt()
        assert s.enemies_killed == 1
        assert s.food_eaten == 1
        assert s.hits_dealt == 1

    def test_to_from_dict(self):
        s = Statistics()
        s.add_enemy_killed()
        s.add_hit_dealt()
        data = s.to_dict()
        s2 = Statistics.from_dict(data)
        assert s2.enemies_killed == 1
        assert s2.hits_dealt == 1
