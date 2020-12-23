from validation.AStarValidation import AStarValidation
from model.Node import Node


class ValidateTimes(AStarValidation):

    def test_EnergyCooldown_ShouldRegardCooldownOfFive(self):
        AStarValidation.set_up_test_method('energy', Node((2, 0, 0)))

        # cost 3 through sentinel hallway
        # cost 5 for cooldown (wait)
        # cost 3 through sentinel hallway
        # cost 1 to destroy
        expected = 12
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].g  # get the final cost

        self.assertEqual(expected, actual)

    def test_RegenerationDoor_ShouldReduceRegenerationTimeByTwo(self):
        AStarValidation.set_up_test_method('regeneration_door', Node((2, 0, 0)))

        # regeneration time at 5
        # door takes 2
        # destroy takes 1
        expected = 2
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].regeneration_time  # get the final cost

        self.assertEqual(expected, actual)

    def test_RegenerationOpen_ShouldReduceRegenerationTimeByOne(self):
        AStarValidation.set_up_test_method('regeneration_open', Node((1, 1, 0)))

        # regeneration time at 5
        # open takes 1
        # destroy takes 1
        expected = 3
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].regeneration_time  # get the final cost

        self.assertEqual(expected, actual)

    def test_RegenerationLadderUp_ShouldReduceRegenerationTimeByTwo(self):
        AStarValidation.set_up_test_method('regeneration_ladder_up', Node((1, 0, -1)))

        # regeneration time at 5
        # ladder up takes 2
        # destroy takes 1
        expected = 2
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].regeneration_time  # get the final cost

        self.assertEqual(expected, actual)

    def test_RegenerationLadderDown_ShouldReduceRegenerationTimeByPointFive(self):
        AStarValidation.set_up_test_method('regeneration_ladder_down', Node((1, 0, 1)))

        # regeneration time at 5
        # ladder down takes 0.5
        # destroy takes 1
        expected = 3.5
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].regeneration_time  # get the final cost

        self.assertEqual(expected, actual)

    def test_RegenerationBlastWall_ShouldReduceRegenerationTimeByThree(self):
        AStarValidation.set_up_test_method('blasting', Node((2, 0, 0)))

        # regeneration time at 5
        # blast wall takes 3
        # destroy takes 1
        expected = 1
        result = AStarValidation.astar_controller.search_path()
        actual = result[len(result) - 1].regeneration_time  # get the final cost

        self.assertEqual(expected, actual)